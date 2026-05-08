# Copyright (C) 2013 Lukas Lalinsky
# Distributed under the MIT license, see the LICENSE file for details.

import re
import sqlparse
from sqlparse import tokens as T
from sqlparse.sql import Token, TokenList, Parenthesis, Statement


def group_parentheses(tokens):
    stack = [[]]
    for token in tokens:
        if token.is_whitespace:
            continue
        if token.match(T.Punctuation, '('):
            stack.append([token])
        else:
            stack[-1].append(token)
            if token.match(T.Punctuation, ')'):
                group = stack.pop()
                stack[-1].append(Parenthesis(group))
    return TokenList(stack[0])


class Set(Statement):

    def get_name(self):
        idx, set_token = self.token_next_by(m=(T.Keyword, 'SET'))
        if set_token is None:
            raise ValueError('unknown format - missing SET')
        idx, token = self.token_next(idx)
        if token is None:
            raise ValueError('unknown format - missing SET name')
        return token.value

    def _find_value(self):
        idx, comparison = self.token_next_by(m=(T.Comparison, '='))
        if comparison is None:
            idx, comparison = self.token_next_by(m=(T.Keyword, 'TO'))
            if comparison is None:
                raise ValueError('unknown format')
        return idx, comparison

    def get_value(self):
        idx, token = self.token_next(self._find_value()[0])
        if token is None or token.match(T.Punctuation, ';'):
            return None
        if token.ttype == T.String.Single:
            return token.value[1:-1]
        if token.ttype == T.Name:
            return token.value
        raise ValueError('unknown format')


class CreateTable(Statement):

    def __init__(self, tokens):
        Statement.__init__(self, tokens)
        self._group_columns()

    def _group_columns(self):
        idx, body_token = self.token_next_by(Parenthesis)
        if body_token is None:
            raise ValueError('unknown format - missing TABLE body')

        start = 1
        end = len(body_token.tokens) - 1

        groups = []

        while start < end:
            group_start = start
            while group_start <= end and body_token.tokens[group_start].value.startswith('--'):
                group_start += 1

            group_end = group_start
            while group_end < end:
                group_end += 1
                if body_token.tokens[group_end].match(T.Punctuation, ','):
                    break
            while group_end < end:
                group_end += 1
                if not body_token.tokens[group_end].value.startswith('--'):
                    break

            start = group_end

            if body_token.tokens[group_start].value not in ('CONSTRAINT', 'CHECK'):
                groups.insert(0, (group_start, group_end))

        for group_start, group_end in groups:
            body_token.group_tokens(CreateTableColumn, group_start, group_end, include_end=0)

    def get_name(self):
        idx, table_token = self.token_next_by(m=(T.Keyword, 'TABLE'))
        if table_token is None:
            raise ValueError('unknown format - missing TABLE')

        idx, token = self.token_next(idx)
        if token is None:
            raise ValueError('unknown format - missing TABLE name')

        return token.value

    def is_partition_of(self):
        idx, partition_token = self.token_next_by(m=(T.Keyword, 'PARTITION'))
        if partition_token is None:
            return False

        idx, token = self.token_next(idx)
        if token is None:
            return False

        return token.value == 'OF'

    def get_columns(self):
        for token in self.tokens:
            if isinstance(token, Parenthesis):
                for sub_token in token.tokens:
                    if isinstance(sub_token, CreateTableColumn):
                        yield sub_token


class CreateTableColumnCheckConstraint(TokenList):

    def get_name(self):
        idx, constraint_token = self.token_next_by(m=(T.Keyword, 'CONSTRAINT'))
        if constraint_token is not None:
            idx, name_token = self.token_next(idx)
            if name_token is not None:
                return name_token.value

    def _get_body_tokens(self):
        idx, body_token = self.token_next_by(i=Parenthesis)
        if body_token is not None:
            return TokenList(body_token.tokens[1:-1])

    def get_body(self):
        tokens = []
        for token in self._get_body_tokens().flatten():
            if token.is_whitespace:
                continue
            if token.ttype == T.Comment.Single:
                continue
            # if tokens and not tokens[-1].match(T.Punctuation, '(') and not token.match(T.Punctuation, ')') and not tokens[-1].value == 'E':
            #     tokens.append(Token(T.Whitespace, ' '))
            tokens.append(token)
        return group_parentheses(tokens)


class CreateTableColumn(TokenList):

    def get_name(self):
        name_token = self.token_first()

        return name_token.value

    def get_type(self):
        idx, name_token = self.token_next(-1)

        idx, token = self.token_next(idx)
        type = token.value

        idx, token = self.token_next(idx)
        if token and isinstance(token, Parenthesis):
            type += token.value
            idx, token = self.token_next(idx)

        if token and token.normalized == 'WITH':
            idx2, t = self.token_next(idx)
            if t and t.normalized == 'TIME':
                idx2, t = self.token_next(idx2)
                if t and t.normalized == 'ZONE':
                    type += ' WITH TIME ZONE'
                    idx2, token = self.token_next(idx2)

        if token and token.normalized == 'WITHOUT':
            idx2, t = self.token_next(idx)
            if t and t.normalized == 'TIME':
                idx2, t = self.token_next(idx2)
                if t and t.normalized == 'ZONE':
                    type += ' WITHOUT TIME ZONE'
                    idx2, token = self.token_next(idx2)

        return type

    def get_default_value(self):
        idx, token = self.token_next_by(m=(T.Keyword, 'DEFAULT'))
        if token is None:
            return None

        idx, token = self.token_next(idx)
        default = token.value

        idx, token = self.token_next(idx)
        if token and isinstance(token, Parenthesis):
            default += token.value
            idx, token = self.token_next(idx)

        return default

    def get_comments(self):
        comments = []
        idx, token = self.token_next_by(t=T.Comment.Single)

        while token is not None:
            comments.append(token.value.strip())
            idx += 1
            idx, token = self.token_next_by(t=T.Comment.Single, idx=idx)

        return comments

    def is_not_null(self):
        idx, token = self.token_next_by(m=(T.Keyword, 'NOT NULL'))
        if token is None:
            return False
        return True

    def get_check_constraint(self):
        idx, check_token = self.token_next_by(m=(T.Keyword, 'CHECK'))
        if check_token is None:
            return None

        tokens = []

        idx2, constraint_name_token = self.token_prev(idx)
        if constraint_name_token is not None:
            idx2, constraint_token = self.token_prev(idx2)
            if constraint_token is not None and constraint_token.normalized == 'CONSTRAINT':
                tokens.append(constraint_token)
                tokens.append(constraint_name_token)

        tokens.append(check_token)

        idx, body_token = self.token_next(idx)
        tokens.append(body_token)

        return CreateTableColumnCheckConstraint(tokens)


class CreateType(Statement):

    def get_name(self):
        idx, token = self.token_next_by(t=T.Name)
        if token is None:
            raise ValueError('unknown format')

        return token.value

    def get_enum_labels(self):
        idx, enum_token = self.token_next_by(m=(T.Keyword, 'ENUM'))
        if enum_token is None:
            raise ValueError('unknown format - missing ENUM')

        idx, parentheses_tokens = self.token_next(idx)
        if parentheses_tokens is None or not isinstance(parentheses_tokens, Parenthesis):
            raise ValueError('unknown format - missing parentheses after ENUM')

        labels = []
        for token in parentheses_tokens.tokens:
            if token.ttype == T.String.Single:
                labels.append(token.value[1:-1])
        return labels


class CreateIndex(Statement):

    def get_name(self):
        idx, token = self.token_next_by(m=(T.Keyword, 'INDEX'))
        if token is None:
            raise ValueError('unknown format - missing INDEX')

        idx, token = self.token_next(idx)
        if token is None:
            raise ValueError('unknown format')

        return token.value

    def is_unique(self):
        idx, token = self.token_next_by(m=(T.Keyword, 'INDEX'))
        if token is None:
            raise ValueError('unknown format - missing INDEX')

        idx, token = self.token_prev(idx)
        if token is None:
            raise ValueError('unknown format')

        return token.normalized == 'UNIQUE'

    def get_table(self):
        idx, token = self.token_next_by(m=(T.Keyword, 'ON'))
        if token is None:
            raise ValueError('unknown format - missing ON')

        idx, token = self.token_next(idx)
        if token is None:
            raise ValueError('unknown format')

        return token.value

    def get_columns(self):
        idx, parens_token = self.token_next_by(i=Parenthesis)
        if parens_token is None:
            raise ValueError('unknown format - missing ON')

        columns = []
        for token in parens_token.tokens:
            if token.ttype != T.Punctuation:
                columns.append(token.value)
        return columns


def parse_statements(statements):
    for statement in statements:
        clean_tokens = group_parentheses(statement.flatten())
        idx, token = statement.token_next(-1)
        if token is None:
            continue
        if token.normalized == 'SET':
            statement = Set(clean_tokens.tokens)
        elif token.normalized == 'CREATE':
            idx, token = statement.token_next(idx)
            if token is not None:
                if token.normalized == 'TABLE':
                    statement = CreateTable(clean_tokens.tokens)
                elif token.normalized == 'TYPE':
                    statement = CreateType(clean_tokens.tokens)
                elif token.normalized == 'INDEX':
                    statement = CreateIndex(clean_tokens.tokens)
                elif token.normalized == 'UNIQUE':
                    idx, token = statement.token_next(idx)
                    if token is not None:
                        if token.normalized == 'INDEX':
                            statement = CreateIndex(clean_tokens.tokens)
        yield statement

