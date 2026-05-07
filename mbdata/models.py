# Automatically generated, do not edit

# pylint: disable=C0103
# pylint: disable=C0302
# pylint: disable=W0232

from sqlalchemy import Column, Index, Integer, String, Text, ForeignKey, Boolean, DateTime, Time, Date, Enum, Interval, CHAR, CheckConstraint, sql
try:
    from sqlalchemy.orm import declarative_base
except ImportError:
    from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, composite, backref
from mbdata.types import PartialDate, Point, Cube as _Cube, regexp, UUID, SMALLINT, BIGINT, JSONB
from typing import Any, Union

import mbdata.config
mbdata.config.freeze()

Base = None  # type: Any

if mbdata.config.Base is not None:
    Base = mbdata.config.Base
elif mbdata.config.metadata is not None:
    Base = declarative_base(metadata=mbdata.config.metadata)
else:
    Base = declarative_base()

if mbdata.config.use_cube:
    Cube = _Cube  # type: Union[_Cube, Text]
else:
    Cube = Text


def apply_schema(name, schema):
    schema = mbdata.config.schemas.get(schema, schema)
    if schema:
        name = "{}.{}".format(schema, name)
    return name


class AlternativeRelease(Base):
    __tablename__ = 'alternative_release'
    __table_args__ = (
        Index('alternative_release_idx_name', 'name'),
        Index('alternative_release_idx_artist_credit', 'artist_credit'),
        Index('alternative_release_idx_language_script', 'language', 'script'),
        Index('alternative_release_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='alternative_release_fk_release'), nullable=False)
    name = Column(String)
    artist_credit_id = Column('artist_credit', Integer, ForeignKey(apply_schema('artist_credit.id', 'musicbrainz'), name='alternative_release_fk_artist_credit'))
    type_id = Column('type', Integer, ForeignKey(apply_schema('alternative_release_type.id', 'musicbrainz'), name='alternative_release_fk_type'), nullable=False)
    language_id = Column('language', Integer, ForeignKey(apply_schema('language.id', 'musicbrainz'), name='alternative_release_fk_language'), nullable=False)
    script_id = Column('script', Integer, ForeignKey(apply_schema('script.id', 'musicbrainz'), name='alternative_release_fk_script'), nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))

    release = relationship('Release', foreign_keys=[release_id], innerjoin=True)
    artist_credit = relationship('ArtistCredit', foreign_keys=[artist_credit_id])
    type = relationship('AlternativeReleaseType', foreign_keys=[type_id], innerjoin=True)
    language = relationship('Language', foreign_keys=[language_id], innerjoin=True)
    script = relationship('Script', foreign_keys=[script_id], innerjoin=True)


class AlternativeReleaseType(Base):
    __tablename__ = 'alternative_release_type'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('alternative_release_type.id', 'musicbrainz'), name='alternative_release_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('AlternativeReleaseType', foreign_keys=[parent_id])


class AlternativeMedium(Base):
    __tablename__ = 'alternative_medium'
    __table_args__ = (
        Index('alternative_medium_idx_alternative_release', 'alternative_release'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    medium_id = Column('medium', Integer, ForeignKey(apply_schema('medium.id', 'musicbrainz'), name='alternative_medium_fk_medium'), nullable=False)
    alternative_release_id = Column('alternative_release', Integer, ForeignKey(apply_schema('alternative_release.id', 'musicbrainz'), name='alternative_medium_fk_alternative_release'), nullable=False)
    name = Column(String)

    medium = relationship('Medium', foreign_keys=[medium_id], innerjoin=True)
    alternative_release = relationship('AlternativeRelease', foreign_keys=[alternative_release_id], innerjoin=True)


class AlternativeTrack(Base):
    __tablename__ = 'alternative_track'
    __table_args__ = (
        Index('alternative_track_idx_name', 'name'),
        Index('alternative_track_idx_artist_credit', 'artist_credit'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String)
    artist_credit_id = Column('artist_credit', Integer, ForeignKey(apply_schema('artist_credit.id', 'musicbrainz'), name='alternative_track_fk_artist_credit'))
    ref_count = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))

    artist_credit = relationship('ArtistCredit', foreign_keys=[artist_credit_id])


class AlternativeMediumTrack(Base):
    __tablename__ = 'alternative_medium_track'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    alternative_medium_id = Column('alternative_medium', Integer, ForeignKey(apply_schema('alternative_medium.id', 'musicbrainz'), name='alternative_medium_track_fk_alternative_medium'), nullable=False, primary_key=True)
    track_id = Column('track', Integer, ForeignKey(apply_schema('track.id', 'musicbrainz'), name='alternative_medium_track_fk_track'), nullable=False, primary_key=True)
    alternative_track_id = Column('alternative_track', Integer, ForeignKey(apply_schema('alternative_track.id', 'musicbrainz'), name='alternative_medium_track_fk_alternative_track'), nullable=False)

    alternative_medium = relationship('AlternativeMedium', foreign_keys=[alternative_medium_id], innerjoin=True)
    track = relationship('Track', foreign_keys=[track_id], innerjoin=True)
    alternative_track = relationship('AlternativeTrack', foreign_keys=[alternative_track_id], innerjoin=True)


class Annotation(Base):
    __tablename__ = 'annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='annotation_fk_editor'), nullable=False)
    text = Column(String)
    changelog = Column(String(255))
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)


class Application(Base):
    __tablename__ = 'application'
    __table_args__ = (
        Index('application_idx_owner', 'owner'),
        Index('application_idx_oauth_id', 'oauth_id', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    owner_id = Column('owner', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='application_fk_owner'), nullable=False)
    name = Column(String, nullable=False)
    oauth_id = Column(String, nullable=False)
    oauth_secret = Column(String, nullable=False)
    oauth_redirect_uri = Column(String)

    owner = relationship('Editor', foreign_keys=[owner_id], innerjoin=True)


class AreaType(Base):
    __tablename__ = 'area_type'
    __table_args__ = (
        Index('area_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('area_type.id', 'musicbrainz'), name='area_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('AreaType', foreign_keys=[parent_id])


class Area(Base):
    __tablename__ = 'area'
    __table_args__ = (
        Index('area_idx_gid', 'gid', unique=True),
        Index('area_idx_name', 'name'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    type_id = Column('type', Integer, ForeignKey(apply_schema('area_type.id', 'musicbrainz'), name='area_fk_type'))
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))

    type = relationship('AreaType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class AreaGIDRedirect(Base):
    __tablename__ = 'area_gid_redirect'
    __table_args__ = (
        Index('area_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='area_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('Area', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def area(self):
        return self.redirect


class AreaAliasType(Base):
    __tablename__ = 'area_alias_type'
    __table_args__ = (
        Index('area_alias_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('area_alias_type.id', 'musicbrainz'), name='area_alias_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('AreaAliasType', foreign_keys=[parent_id])


class AreaAlias(Base):
    __tablename__ = 'area_alias'
    __table_args__ = (
        Index('area_alias_idx_area', 'area'),
        Index('area_alias_idx_primary', 'area', 'locale', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='area_alias_fk_area'), nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    type_id = Column('type', Integer, ForeignKey(apply_schema('area_alias_type.id', 'musicbrainz'), name='area_alias_fk_type'))
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    primary_for_locale = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    area = relationship('Area', foreign_keys=[area_id], innerjoin=True)
    type = relationship('AreaAliasType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class AreaAnnotation(Base):
    __tablename__ = 'area_annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='area_annotation_fk_area'), nullable=False, primary_key=True)
    annotation_id = Column('annotation', Integer, ForeignKey(apply_schema('annotation.id', 'musicbrainz'), name='area_annotation_fk_annotation'), nullable=False, primary_key=True)

    area = relationship('Area', foreign_keys=[area_id], innerjoin=True)
    annotation = relationship('Annotation', foreign_keys=[annotation_id], innerjoin=True)


class AreaAttributeType(Base):
    __tablename__ = 'area_attribute_type'
    __table_args__ = (
        Index('area_attribute_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    free_text = Column(Boolean, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('area_attribute_type.id', 'musicbrainz'), name='area_attribute_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('AreaAttributeType', foreign_keys=[parent_id])


class AreaAttributeTypeAllowedValue(Base):
    __tablename__ = 'area_attribute_type_allowed_value'
    __table_args__ = (
        Index('area_attribute_type_allowed_value_idx_name', 'area_attribute_type'),
        Index('area_attribute_type_allowed_value_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    area_attribute_type_id = Column('area_attribute_type', Integer, ForeignKey(apply_schema('area_attribute_type.id', 'musicbrainz'), name='area_attribute_type_allowed_value_fk_area_attribute_type'), nullable=False)
    value = Column(String)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('area_attribute_type_allowed_value.id', 'musicbrainz'), name='area_attribute_type_allowed_value_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    area_attribute_type = relationship('AreaAttributeType', foreign_keys=[area_attribute_type_id], innerjoin=True)
    parent = relationship('AreaAttributeTypeAllowedValue', foreign_keys=[parent_id])


class AreaAttribute(Base):
    __tablename__ = 'area_attribute'
    __table_args__ = (
        Index('area_attribute_idx_area', 'area'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='area_attribute_fk_area'), nullable=False)
    area_attribute_type_id = Column('area_attribute_type', Integer, ForeignKey(apply_schema('area_attribute_type.id', 'musicbrainz'), name='area_attribute_fk_area_attribute_type'), nullable=False)
    area_attribute_type_allowed_value_id = Column('area_attribute_type_allowed_value', Integer, ForeignKey(apply_schema('area_attribute_type_allowed_value.id', 'musicbrainz'), name='area_attribute_fk_area_attribute_type_allowed_value'))
    area_attribute_text = Column(String)

    area = relationship('Area', foreign_keys=[area_id], innerjoin=True)
    area_attribute_type = relationship('AreaAttributeType', foreign_keys=[area_attribute_type_id], innerjoin=True)
    area_attribute_type_allowed_value = relationship('AreaAttributeTypeAllowedValue', foreign_keys=[area_attribute_type_allowed_value_id])


class AreaContainment(Base):
    __tablename__ = 'area_containment'
    __table_args__ = (
        Index('area_containment_idx_parent', 'parent'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    descendant_id = Column('descendant', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='area_containment_fk_descendant'), nullable=False, primary_key=True)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='area_containment_fk_parent'), nullable=False, primary_key=True)
    depth = Column(SMALLINT, nullable=False)

    descendant = relationship('Area', foreign_keys=[descendant_id], innerjoin=True)
    parent = relationship('Area', foreign_keys=[parent_id], innerjoin=True)


class AreaTag(Base):
    __tablename__ = 'area_tag'
    __table_args__ = (
        Index('area_tag_idx_tag', 'tag'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='area_tag_fk_area'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='area_tag_fk_tag'), nullable=False, primary_key=True)
    count = Column(Integer, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    area = relationship('Area', foreign_keys=[area_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class AreaTagRaw(Base):
    __tablename__ = 'area_tag_raw'
    __table_args__ = (
        Index('area_tag_raw_idx_area', 'area'),
        Index('area_tag_raw_idx_tag', 'tag'),
        Index('area_tag_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='area_tag_raw_fk_area'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='area_tag_raw_fk_editor'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='area_tag_raw_fk_tag'), nullable=False, primary_key=True)
    is_upvote = Column(Boolean, nullable=False, default=True, server_default=sql.true())

    area = relationship('Area', foreign_keys=[area_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class Artist(Base):
    __tablename__ = 'artist'
    __table_args__ = (
        Index('artist_idx_gid', 'gid', unique=True),
        Index('artist_idx_name', 'name'),
        Index('artist_idx_sort_name', 'sort_name'),
        Index('artist_idx_area', 'area'),
        Index('artist_idx_begin_area', 'begin_area'),
        Index('artist_idx_end_area', 'end_area'),
        Index('artist_idx_null_comment', 'name', unique=True),
        Index('artist_idx_uniq_name_comment', 'name', 'comment', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    type_id = Column('type', Integer, ForeignKey(apply_schema('artist_type.id', 'musicbrainz'), name='artist_fk_type'))
    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='artist_fk_area'))
    gender_id = Column('gender', Integer, ForeignKey(apply_schema('gender.id', 'musicbrainz'), name='artist_fk_gender'))
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    begin_area_id = Column('begin_area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='artist_fk_begin_area'))
    end_area_id = Column('end_area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='artist_fk_end_area'))

    type = relationship('ArtistType', foreign_keys=[type_id])
    area = relationship('Area', foreign_keys=[area_id])
    gender = relationship('Gender', foreign_keys=[gender_id])
    begin_area = relationship('Area', foreign_keys=[begin_area_id])
    end_area = relationship('Area', foreign_keys=[end_area_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class ArtistAliasType(Base):
    __tablename__ = 'artist_alias_type'
    __table_args__ = (
        Index('artist_alias_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('artist_alias_type.id', 'musicbrainz'), name='artist_alias_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('ArtistAliasType', foreign_keys=[parent_id])


class ArtistAlias(Base):
    __tablename__ = 'artist_alias'
    __table_args__ = (
        Index('artist_alias_idx_artist', 'artist'),
        Index('artist_alias_idx_primary', 'artist', 'locale', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_alias_fk_artist'), nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    type_id = Column('type', Integer, ForeignKey(apply_schema('artist_alias_type.id', 'musicbrainz'), name='artist_alias_fk_type'))
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    primary_for_locale = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    type = relationship('ArtistAliasType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class ArtistAnnotation(Base):
    __tablename__ = 'artist_annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_annotation_fk_artist'), nullable=False, primary_key=True)
    annotation_id = Column('annotation', Integer, ForeignKey(apply_schema('annotation.id', 'musicbrainz'), name='artist_annotation_fk_annotation'), nullable=False, primary_key=True)

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    annotation = relationship('Annotation', foreign_keys=[annotation_id], innerjoin=True)


class ArtistAttributeType(Base):
    __tablename__ = 'artist_attribute_type'
    __table_args__ = (
        Index('artist_attribute_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    free_text = Column(Boolean, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('artist_attribute_type.id', 'musicbrainz'), name='artist_attribute_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('ArtistAttributeType', foreign_keys=[parent_id])


class ArtistAttributeTypeAllowedValue(Base):
    __tablename__ = 'artist_attribute_type_allowed_value'
    __table_args__ = (
        Index('artist_attribute_type_allowed_value_idx_name', 'artist_attribute_type'),
        Index('artist_attribute_type_allowed_value_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    artist_attribute_type_id = Column('artist_attribute_type', Integer, ForeignKey(apply_schema('artist_attribute_type.id', 'musicbrainz'), name='artist_attribute_type_allowed_value_fk_artist_attribute_type'), nullable=False)
    value = Column(String)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('artist_attribute_type_allowed_value.id', 'musicbrainz'), name='artist_attribute_type_allowed_value_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    artist_attribute_type = relationship('ArtistAttributeType', foreign_keys=[artist_attribute_type_id], innerjoin=True)
    parent = relationship('ArtistAttributeTypeAllowedValue', foreign_keys=[parent_id])


class ArtistAttribute(Base):
    __tablename__ = 'artist_attribute'
    __table_args__ = (
        Index('artist_attribute_idx_artist', 'artist'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_attribute_fk_artist'), nullable=False)
    artist_attribute_type_id = Column('artist_attribute_type', Integer, ForeignKey(apply_schema('artist_attribute_type.id', 'musicbrainz'), name='artist_attribute_fk_artist_attribute_type'), nullable=False)
    artist_attribute_type_allowed_value_id = Column('artist_attribute_type_allowed_value', Integer, ForeignKey(apply_schema('artist_attribute_type_allowed_value.id', 'musicbrainz'), name='artist_attribute_fk_artist_attribute_type_allowed_value'))
    artist_attribute_text = Column(String)

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    artist_attribute_type = relationship('ArtistAttributeType', foreign_keys=[artist_attribute_type_id], innerjoin=True)
    artist_attribute_type_allowed_value = relationship('ArtistAttributeTypeAllowedValue', foreign_keys=[artist_attribute_type_allowed_value_id])


class ArtistIPI(Base):
    __tablename__ = 'artist_ipi'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_ipi_fk_artist'), nullable=False, primary_key=True)
    ipi = Column(CHAR(11), nullable=False, primary_key=True)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True, backref=backref('ipis'))


class ArtistISNI(Base):
    __tablename__ = 'artist_isni'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_isni_fk_artist'), nullable=False, primary_key=True)
    isni = Column(CHAR(16), nullable=False, primary_key=True)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True, backref=backref('isnis'))


class ArtistMeta(Base):
    __tablename__ = 'artist_meta'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_meta_fk_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    rating = Column(SMALLINT)
    rating_count = Column(Integer)

    artist = relationship('Artist', foreign_keys=[id], innerjoin=True, backref=backref('meta', uselist=False))


class ArtistTag(Base):
    __tablename__ = 'artist_tag'
    __table_args__ = (
        Index('artist_tag_idx_tag', 'tag'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_tag_fk_artist'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='artist_tag_fk_tag'), nullable=False, primary_key=True)
    count = Column(Integer, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class ArtistRatingRaw(Base):
    __tablename__ = 'artist_rating_raw'
    __table_args__ = (
        Index('artist_rating_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_rating_raw_fk_artist'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='artist_rating_raw_fk_editor'), nullable=False, primary_key=True)
    rating = Column(SMALLINT, nullable=False)

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)


class ArtistTagRaw(Base):
    __tablename__ = 'artist_tag_raw'
    __table_args__ = (
        Index('artist_tag_raw_idx_tag', 'tag'),
        Index('artist_tag_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_tag_raw_fk_artist'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='artist_tag_raw_fk_editor'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='artist_tag_raw_fk_tag'), nullable=False, primary_key=True)
    is_upvote = Column(Boolean, nullable=False, default=True, server_default=sql.true())

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class ArtistCredit(Base):
    __tablename__ = 'artist_credit'
    __table_args__ = (
        Index('artist_credit_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    artist_count = Column(SMALLINT, nullable=False)
    ref_count = Column(Integer, default=0, server_default=sql.text('0'))
    created = Column(DateTime(timezone=True), server_default=sql.func.now())
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    gid = Column(UUID, nullable=False)


class ArtistCreditGIDRedirect(Base):
    __tablename__ = 'artist_credit_gid_redirect'
    __table_args__ = (
        Index('artist_credit_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('artist_credit.id', 'musicbrainz'), name='artist_credit_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('ArtistCredit', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def artist_credit(self):
        return self.redirect


class ArtistCreditName(Base):
    __tablename__ = 'artist_credit_name'
    __table_args__ = (
        Index('artist_credit_name_idx_artist', 'artist'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    artist_credit_id = Column('artist_credit', Integer, ForeignKey(apply_schema('artist_credit.id', 'musicbrainz'), name='artist_credit_name_fk_artist_credit', ondelete='CASCADE'), nullable=False, primary_key=True)
    position = Column(SMALLINT, nullable=False, primary_key=True)
    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_credit_name_fk_artist', ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    join_phrase = Column(String, nullable=False, default='', server_default=sql.text("''"))

    artist_credit = relationship('ArtistCredit', foreign_keys=[artist_credit_id], innerjoin=True, backref=backref('artists', order_by="ArtistCreditName.position"))
    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)


class ArtistGIDRedirect(Base):
    __tablename__ = 'artist_gid_redirect'
    __table_args__ = (
        Index('artist_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('Artist', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def artist(self):
        return self.redirect


class ArtistType(Base):
    __tablename__ = 'artist_type'
    __table_args__ = (
        Index('artist_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('artist_type.id', 'musicbrainz'), name='artist_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('ArtistType', foreign_keys=[parent_id])


class ArtistRelease(Base):
    __tablename__ = 'artist_release'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    is_track_artist = Column(Boolean, nullable=False)
    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_release_fk_artist'), nullable=False, primary_key=True)
    first_release_date = Column(Integer)
    catalog_numbers = Column(String)
    country_code = Column(CHAR(2))
    barcode = Column(BIGINT)
    name = Column(String, nullable=False)
    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='artist_release_fk_release'), nullable=False, primary_key=True)

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    release = relationship('Release', foreign_keys=[release_id], innerjoin=True)


class ArtistReleaseGroup(Base):
    __tablename__ = 'artist_release_group'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    is_track_artist = Column(Boolean, nullable=False)
    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_release_group_fk_artist'), nullable=False, primary_key=True)
    unofficial = Column(Boolean, nullable=False)
    primary_type_child_order = Column(SMALLINT)
    primary_type = Column(SMALLINT)
    secondary_type_child_orders = Column(SMALLINT)
    secondary_types = Column(SMALLINT)
    first_release_date = Column(Integer)
    name = Column(String, nullable=False)
    release_group_id = Column('release_group', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='artist_release_group_fk_release_group'), nullable=False, primary_key=True)

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    release_group = relationship('ReleaseGroup', foreign_keys=[release_group_id], innerjoin=True)


class AutoeditorElection(Base):
    __tablename__ = 'autoeditor_election'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    candidate_id = Column('candidate', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='autoeditor_election_fk_candidate'), nullable=False)
    proposer_id = Column('proposer', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='autoeditor_election_fk_proposer'), nullable=False)
    seconder_1_id = Column('seconder_1', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='autoeditor_election_fk_seconder_1'))
    seconder_2_id = Column('seconder_2', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='autoeditor_election_fk_seconder_2'))
    status = Column(Integer, nullable=False, default=1, server_default=sql.text('1'))
    yes_votes = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    no_votes = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    propose_time = Column(DateTime(timezone=True), nullable=False, server_default=sql.func.now())
    open_time = Column(DateTime(timezone=True))
    close_time = Column(DateTime(timezone=True))

    candidate = relationship('Editor', foreign_keys=[candidate_id], innerjoin=True)
    proposer = relationship('Editor', foreign_keys=[proposer_id], innerjoin=True)
    seconder_1 = relationship('Editor', foreign_keys=[seconder_1_id])
    seconder_2 = relationship('Editor', foreign_keys=[seconder_2_id])


class AutoeditorElectionVote(Base):
    __tablename__ = 'autoeditor_election_vote'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    autoeditor_election_id = Column('autoeditor_election', Integer, ForeignKey(apply_schema('autoeditor_election.id', 'musicbrainz'), name='autoeditor_election_vote_fk_autoeditor_election'), nullable=False)
    voter_id = Column('voter', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='autoeditor_election_vote_fk_voter'), nullable=False)
    vote = Column(Integer, nullable=False)
    vote_time = Column(DateTime(timezone=True), nullable=False, server_default=sql.func.now())

    autoeditor_election = relationship('AutoeditorElection', foreign_keys=[autoeditor_election_id], innerjoin=True)
    voter = relationship('Editor', foreign_keys=[voter_id], innerjoin=True)


class CDTOC(Base):
    __tablename__ = 'cdtoc'
    __table_args__ = (
        Index('cdtoc_idx_discid', 'discid', unique=True),
        Index('cdtoc_idx_freedb_id', 'freedb_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    discid = Column(CHAR(28), nullable=False)
    freedb_id = Column(CHAR(8), nullable=False)
    track_count = Column(Integer, nullable=False)
    leadout_offset = Column(Integer, nullable=False)
    track_offset = Column(Integer, nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())


class CDTOCRaw(Base):
    __tablename__ = 'cdtoc_raw'
    __table_args__ = (
        Index('cdtoc_raw_discid', 'discid'),
        Index('cdtoc_raw_toc', 'track_count', 'leadout_offset', 'track_offset', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    release_id = Column('release', Integer, ForeignKey(apply_schema('release_raw.id', 'musicbrainz'), name='cdtoc_raw_fk_release'), nullable=False)
    discid = Column(CHAR(28), nullable=False)
    track_count = Column(Integer, nullable=False)
    leadout_offset = Column(Integer, nullable=False)
    track_offset = Column(Integer, nullable=False)

    release = relationship('ReleaseRaw', foreign_keys=[release_id], innerjoin=True)


class CountryArea(Base):
    __tablename__ = 'country_area'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='country_area_fk_area'), primary_key=True)

    area = relationship('Area', foreign_keys=[area_id])


class DeletedEntity(Base):
    __tablename__ = 'deleted_entity'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    data = Column(JSONB, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=False, server_default=sql.func.now())


class Edit(Base):
    __tablename__ = 'edit'
    __table_args__ = (
        Index('edit_idx_type_id', 'type', 'id'),
        Index('edit_idx_open_time', 'open_time'),
        Index('edit_idx_close_time', 'close_time'),
        Index('edit_idx_expire_time', 'expire_time'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='edit_fk_editor'), nullable=False)
    type = Column(SMALLINT, nullable=False)
    status = Column(SMALLINT, nullable=False)
    autoedit = Column(SMALLINT, nullable=False, default=0, server_default=sql.text('0'))
    open_time = Column(DateTime(timezone=True), server_default=sql.func.now())
    close_time = Column(DateTime(timezone=True))
    expire_time = Column(DateTime(timezone=True), nullable=False)
    language_id = Column('language', Integer, ForeignKey(apply_schema('language.id', 'musicbrainz'), name='edit_fk_language'))
    quality = Column(SMALLINT, nullable=False, default=1, server_default=sql.text('1'))

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    language = relationship('Language', foreign_keys=[language_id])


class EditData(Base):
    __tablename__ = 'edit_data'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_data_fk_edit'), nullable=False, primary_key=True)
    data = Column(JSONB, nullable=False)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)


class EditNote(Base):
    __tablename__ = 'edit_note'
    __table_args__ = (
        Index('edit_note_idx_edit', 'edit'),
        Index('edit_note_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='edit_note_fk_editor'), nullable=False)
    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_note_fk_edit'), nullable=False)
    text = Column(String, nullable=False)
    post_time = Column(DateTime(timezone=True), server_default=sql.func.now())

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)


class EditNoteChange(Base):
    __tablename__ = 'edit_note_change'
    __table_args__ = (
        Index('edit_note_change_idx_edit_note', 'edit_note'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    status = Column(Enum('deleted', 'edited', name='EDIT_NOTE_STATUS', schema=mbdata.config.schemas.get('musicbrainz', 'musicbrainz')))
    edit_note_id = Column('edit_note', Integer, ForeignKey(apply_schema('edit_note.id', 'musicbrainz'), name='edit_note_change_fk_edit_note'), nullable=False)
    change_editor_id = Column('change_editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='edit_note_change_fk_change_editor'), nullable=False)
    change_time = Column(DateTime(timezone=True), server_default=sql.func.now())
    old_note = Column(String, nullable=False)
    new_note = Column(String, nullable=False)
    reason = Column(String, nullable=False, default='', server_default=sql.text("''"))

    edit_note = relationship('EditNote', foreign_keys=[edit_note_id], innerjoin=True)
    change_editor = relationship('Editor', foreign_keys=[change_editor_id], innerjoin=True)


class EditNoteRecipient(Base):
    __tablename__ = 'edit_note_recipient'
    __table_args__ = (
        Index('edit_note_recipient_idx_recipient', 'recipient'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    recipient_id = Column('recipient', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='edit_note_recipient_fk_recipient'), nullable=False, primary_key=True)
    edit_note_id = Column('edit_note', Integer, ForeignKey(apply_schema('edit_note.id', 'musicbrainz'), name='edit_note_recipient_fk_edit_note'), nullable=False, primary_key=True)

    recipient = relationship('Editor', foreign_keys=[recipient_id], innerjoin=True)
    edit_note = relationship('EditNote', foreign_keys=[edit_note_id], innerjoin=True)


class EditArea(Base):
    __tablename__ = 'edit_area'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_area_fk_edit'), nullable=False, primary_key=True)
    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='edit_area_fk_area', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    area = relationship('Area', foreign_keys=[area_id], innerjoin=True)


class EditArtist(Base):
    __tablename__ = 'edit_artist'
    __table_args__ = (
        Index('edit_artist_idx', 'artist'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_artist_fk_edit'), nullable=False, primary_key=True)
    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='edit_artist_fk_artist', ondelete='CASCADE'), nullable=False, primary_key=True)
    status = Column(SMALLINT, nullable=False)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)


class EditEvent(Base):
    __tablename__ = 'edit_event'
    __table_args__ = (
        Index('edit_event_idx', 'event'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_event_fk_edit'), nullable=False, primary_key=True)
    event_id = Column('event', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='edit_event_fk_event', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    event = relationship('Event', foreign_keys=[event_id], innerjoin=True)


class EditGenre(Base):
    __tablename__ = 'edit_genre'
    __table_args__ = (
        Index('edit_genre_idx', 'genre'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_genre_fk_edit'), nullable=False, primary_key=True)
    genre_id = Column('genre', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='edit_genre_fk_genre', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    genre = relationship('Genre', foreign_keys=[genre_id], innerjoin=True)


class EditInstrument(Base):
    __tablename__ = 'edit_instrument'
    __table_args__ = (
        Index('edit_instrument_idx', 'instrument'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_instrument_fk_edit'), nullable=False, primary_key=True)
    instrument_id = Column('instrument', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='edit_instrument_fk_instrument', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    instrument = relationship('Instrument', foreign_keys=[instrument_id], innerjoin=True)


class EditLabel(Base):
    __tablename__ = 'edit_label'
    __table_args__ = (
        Index('edit_label_idx_status', 'status'),
        Index('edit_label_idx', 'label'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_label_fk_edit'), nullable=False, primary_key=True)
    label_id = Column('label', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='edit_label_fk_label', ondelete='CASCADE'), nullable=False, primary_key=True)
    status = Column(SMALLINT, nullable=False)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    label = relationship('Label', foreign_keys=[label_id], innerjoin=True)


class EditMood(Base):
    __tablename__ = 'edit_mood'
    __table_args__ = (
        Index('edit_mood_idx', 'mood'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_mood_fk_edit'), nullable=False, primary_key=True)
    mood_id = Column('mood', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='edit_mood_fk_mood', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    mood = relationship('Mood', foreign_keys=[mood_id], innerjoin=True)


class EditPlace(Base):
    __tablename__ = 'edit_place'
    __table_args__ = (
        Index('edit_place_idx', 'place'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_place_fk_edit'), nullable=False, primary_key=True)
    place_id = Column('place', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='edit_place_fk_place', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    place = relationship('Place', foreign_keys=[place_id], innerjoin=True)


class EditRelease(Base):
    __tablename__ = 'edit_release'
    __table_args__ = (
        Index('edit_release_idx', 'release'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_release_fk_edit'), nullable=False, primary_key=True)
    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='edit_release_fk_release', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    release = relationship('Release', foreign_keys=[release_id], innerjoin=True)


class EditReleaseGroup(Base):
    __tablename__ = 'edit_release_group'
    __table_args__ = (
        Index('edit_release_group_idx', 'release_group'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_release_group_fk_edit'), nullable=False, primary_key=True)
    release_group_id = Column('release_group', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='edit_release_group_fk_release_group', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    release_group = relationship('ReleaseGroup', foreign_keys=[release_group_id], innerjoin=True)


class EditRecording(Base):
    __tablename__ = 'edit_recording'
    __table_args__ = (
        Index('edit_recording_idx', 'recording'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_recording_fk_edit'), nullable=False, primary_key=True)
    recording_id = Column('recording', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='edit_recording_fk_recording', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    recording = relationship('Recording', foreign_keys=[recording_id], innerjoin=True)


class EditSeries(Base):
    __tablename__ = 'edit_series'
    __table_args__ = (
        Index('edit_series_idx', 'series'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_series_fk_edit'), nullable=False, primary_key=True)
    series_id = Column('series', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='edit_series_fk_series', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    series = relationship('Series', foreign_keys=[series_id], innerjoin=True)


class EditWork(Base):
    __tablename__ = 'edit_work'
    __table_args__ = (
        Index('edit_work_idx', 'work'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_work_fk_edit'), nullable=False, primary_key=True)
    work_id = Column('work', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='edit_work_fk_work', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    work = relationship('Work', foreign_keys=[work_id], innerjoin=True)


class EditURL(Base):
    __tablename__ = 'edit_url'
    __table_args__ = (
        Index('edit_url_idx', 'url'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_url_fk_edit'), nullable=False, primary_key=True)
    url_id = Column('url', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='edit_url_fk_url', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    url = relationship('URL', foreign_keys=[url_id], innerjoin=True)


class Editor(Base):
    __tablename__ = 'editor'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    privs = Column(Integer, default=0, server_default=sql.text('0'))
    email = Column(String(64))
    website = Column(String(255))
    bio = Column(String)
    member_since = Column(DateTime(timezone=True), server_default=sql.func.now())
    email_confirm_date = Column(DateTime(timezone=True))
    last_login_date = Column(DateTime(timezone=True), server_default=sql.func.now())
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    birth_date = Column(Date)
    gender_id = Column('gender', Integer, ForeignKey(apply_schema('gender.id', 'musicbrainz'), name='editor_fk_gender'))
    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='editor_fk_area'))
    password = Column(String(128), nullable=False)
    ha1 = Column(CHAR(32), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    gender = relationship('Gender', foreign_keys=[gender_id])
    area = relationship('Area', foreign_keys=[area_id])


class EditorLanguage(Base):
    __tablename__ = 'editor_language'
    __table_args__ = (
        Index('editor_language_idx_language', 'language'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='editor_language_fk_editor'), nullable=False, primary_key=True)
    language_id = Column('language', Integer, ForeignKey(apply_schema('language.id', 'musicbrainz'), name='editor_language_fk_language'), nullable=False, primary_key=True)
    fluency = Column(Enum('basic', 'intermediate', 'advanced', 'native', name='FLUENCY', schema=mbdata.config.schemas.get('musicbrainz', 'musicbrainz')), nullable=False)

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    language = relationship('Language', foreign_keys=[language_id], innerjoin=True)


class EditorPreference(Base):
    __tablename__ = 'editor_preference'
    __table_args__ = (
        Index('editor_preference_idx_editor_name', 'editor', 'name', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='editor_preference_fk_editor'), nullable=False)
    name = Column(String(50), nullable=False)
    value = Column(String(100), nullable=False)

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)


class EditorSubscribeArtist(Base):
    __tablename__ = 'editor_subscribe_artist'
    __table_args__ = (
        Index('editor_subscribe_artist_idx_uniq', 'editor', 'artist', unique=True),
        Index('editor_subscribe_artist_idx_artist', 'artist'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='editor_subscribe_artist_fk_editor'), nullable=False)
    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='editor_subscribe_artist_fk_artist'), nullable=False)
    last_edit_sent_id = Column('last_edit_sent', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='editor_subscribe_artist_fk_last_edit_sent'), nullable=False)

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    last_edit_sent = relationship('Edit', foreign_keys=[last_edit_sent_id], innerjoin=True)


class EditorSubscribeArtistDeleted(Base):
    __tablename__ = 'editor_subscribe_artist_deleted'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='editor_subscribe_artist_deleted_fk_editor'), nullable=False, primary_key=True)
    gid = Column(UUID, ForeignKey(apply_schema('deleted_entity.gid', 'musicbrainz'), name='editor_subscribe_artist_deleted_fk_gid'), nullable=False, primary_key=True)
    deleted_by_id = Column('deleted_by', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='editor_subscribe_artist_deleted_fk_deleted_by'), nullable=False)

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    deleted_by = relationship('Edit', foreign_keys=[deleted_by_id], innerjoin=True)


class EditorSubscribeCollection(Base):
    __tablename__ = 'editor_subscribe_collection'
    __table_args__ = (
        Index('editor_subscribe_collection_idx_uniq', 'editor', 'collection', unique=True),
        Index('editor_subscribe_collection_idx_collection', 'collection'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='editor_subscribe_collection_fk_editor'), nullable=False)
    collection = Column(Integer, nullable=False)
    last_edit_sent = Column(Integer, nullable=False)
    available = Column(Boolean, nullable=False, default=True, server_default=sql.true())
    last_seen_name = Column(String(255))

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)


class EditorSubscribeLabel(Base):
    __tablename__ = 'editor_subscribe_label'
    __table_args__ = (
        Index('editor_subscribe_label_idx_uniq', 'editor', 'label', unique=True),
        Index('editor_subscribe_label_idx_label', 'label'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='editor_subscribe_label_fk_editor'), nullable=False)
    label_id = Column('label', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='editor_subscribe_label_fk_label'), nullable=False)
    last_edit_sent_id = Column('last_edit_sent', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='editor_subscribe_label_fk_last_edit_sent'), nullable=False)

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    label = relationship('Label', foreign_keys=[label_id], innerjoin=True)
    last_edit_sent = relationship('Edit', foreign_keys=[last_edit_sent_id], innerjoin=True)


class EditorSubscribeLabelDeleted(Base):
    __tablename__ = 'editor_subscribe_label_deleted'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='editor_subscribe_label_deleted_fk_editor'), nullable=False, primary_key=True)
    gid = Column(UUID, ForeignKey(apply_schema('deleted_entity.gid', 'musicbrainz'), name='editor_subscribe_label_deleted_fk_gid'), nullable=False, primary_key=True)
    deleted_by_id = Column('deleted_by', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='editor_subscribe_label_deleted_fk_deleted_by'), nullable=False)

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    deleted_by = relationship('Edit', foreign_keys=[deleted_by_id], innerjoin=True)


class EditorSubscribeEditor(Base):
    __tablename__ = 'editor_subscribe_editor'
    __table_args__ = (
        Index('editor_subscribe_editor_idx_uniq', 'editor', 'subscribed_editor', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='editor_subscribe_editor_fk_editor'), nullable=False)
    subscribed_editor_id = Column('subscribed_editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='editor_subscribe_editor_fk_subscribed_editor'), nullable=False)
    last_edit_sent = Column(Integer, nullable=False)

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    subscribed_editor = relationship('Editor', foreign_keys=[subscribed_editor_id], innerjoin=True)


class EditorSubscribeSeries(Base):
    __tablename__ = 'editor_subscribe_series'
    __table_args__ = (
        Index('editor_subscribe_series_idx_uniq', 'editor', 'series', unique=True),
        Index('editor_subscribe_series_idx_series', 'series'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='editor_subscribe_series_fk_editor'), nullable=False)
    series_id = Column('series', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='editor_subscribe_series_fk_series'), nullable=False)
    last_edit_sent_id = Column('last_edit_sent', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='editor_subscribe_series_fk_last_edit_sent'), nullable=False)

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    series = relationship('Series', foreign_keys=[series_id], innerjoin=True)
    last_edit_sent = relationship('Edit', foreign_keys=[last_edit_sent_id], innerjoin=True)


class EditorSubscribeSeriesDeleted(Base):
    __tablename__ = 'editor_subscribe_series_deleted'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='editor_subscribe_series_deleted_fk_editor'), nullable=False, primary_key=True)
    gid = Column(UUID, ForeignKey(apply_schema('deleted_entity.gid', 'musicbrainz'), name='editor_subscribe_series_deleted_fk_gid'), nullable=False, primary_key=True)
    deleted_by_id = Column('deleted_by', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='editor_subscribe_series_deleted_fk_deleted_by'), nullable=False)

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    deleted_by = relationship('Edit', foreign_keys=[deleted_by_id], innerjoin=True)


class Event(Base):
    __tablename__ = 'event'
    __table_args__ = (
        Index('event_idx_gid', 'gid', unique=True),
        Index('event_idx_name', 'name'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    time = Column(Time(timezone=False))
    type_id = Column('type', Integer, ForeignKey(apply_schema('event_type.id', 'musicbrainz'), name='event_fk_type'))
    cancelled = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    setlist = Column(String)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    type = relationship('EventType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class EventMeta(Base):
    __tablename__ = 'event_meta'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='event_meta_fk_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    rating = Column(SMALLINT)
    rating_count = Column(Integer)
    event_art_presence = Column(Enum('absent', 'present', 'darkened', name='EVENT_ART_PRESENCE', schema=mbdata.config.schemas.get('musicbrainz', 'musicbrainz')), nullable=False, default='absent', server_default=sql.text("'absent'"))

    event = relationship('Event', foreign_keys=[id], innerjoin=True, backref=backref('meta', uselist=False))


class EventRatingRaw(Base):
    __tablename__ = 'event_rating_raw'
    __table_args__ = (
        Index('event_rating_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    event_id = Column('event', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='event_rating_raw_fk_event'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='event_rating_raw_fk_editor'), nullable=False, primary_key=True)
    rating = Column(SMALLINT, nullable=False)

    event = relationship('Event', foreign_keys=[event_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)


class EventTagRaw(Base):
    __tablename__ = 'event_tag_raw'
    __table_args__ = (
        Index('event_tag_raw_idx_tag', 'tag'),
        Index('event_tag_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    event_id = Column('event', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='event_tag_raw_fk_event'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='event_tag_raw_fk_editor'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='event_tag_raw_fk_tag'), nullable=False, primary_key=True)
    is_upvote = Column(Boolean, nullable=False, default=True, server_default=sql.true())

    event = relationship('Event', foreign_keys=[event_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class EventAliasType(Base):
    __tablename__ = 'event_alias_type'
    __table_args__ = (
        Index('event_alias_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('event_alias_type.id', 'musicbrainz'), name='event_alias_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('EventAliasType', foreign_keys=[parent_id])


class EventAlias(Base):
    __tablename__ = 'event_alias'
    __table_args__ = (
        Index('event_alias_idx_event', 'event'),
        Index('event_alias_idx_primary', 'event', 'locale', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    event_id = Column('event', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='event_alias_fk_event'), nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    type_id = Column('type', Integer, ForeignKey(apply_schema('event_alias_type.id', 'musicbrainz'), name='event_alias_fk_type'))
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    primary_for_locale = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    event = relationship('Event', foreign_keys=[event_id], innerjoin=True)
    type = relationship('EventAliasType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class EventAnnotation(Base):
    __tablename__ = 'event_annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    event_id = Column('event', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='event_annotation_fk_event'), nullable=False, primary_key=True)
    annotation_id = Column('annotation', Integer, ForeignKey(apply_schema('annotation.id', 'musicbrainz'), name='event_annotation_fk_annotation'), nullable=False, primary_key=True)

    event = relationship('Event', foreign_keys=[event_id], innerjoin=True)
    annotation = relationship('Annotation', foreign_keys=[annotation_id], innerjoin=True)


class EventAttributeType(Base):
    __tablename__ = 'event_attribute_type'
    __table_args__ = (
        Index('event_attribute_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    free_text = Column(Boolean, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('event_attribute_type.id', 'musicbrainz'), name='event_attribute_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('EventAttributeType', foreign_keys=[parent_id])


class EventAttributeTypeAllowedValue(Base):
    __tablename__ = 'event_attribute_type_allowed_value'
    __table_args__ = (
        Index('event_attribute_type_allowed_value_idx_name', 'event_attribute_type'),
        Index('event_attribute_type_allowed_value_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    event_attribute_type_id = Column('event_attribute_type', Integer, ForeignKey(apply_schema('event_attribute_type.id', 'musicbrainz'), name='event_attribute_type_allowed_value_fk_event_attribute_type'), nullable=False)
    value = Column(String)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('event_attribute_type_allowed_value.id', 'musicbrainz'), name='event_attribute_type_allowed_value_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    event_attribute_type = relationship('EventAttributeType', foreign_keys=[event_attribute_type_id], innerjoin=True)
    parent = relationship('EventAttributeTypeAllowedValue', foreign_keys=[parent_id])


class EventAttribute(Base):
    __tablename__ = 'event_attribute'
    __table_args__ = (
        Index('event_attribute_idx_event', 'event'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    event_id = Column('event', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='event_attribute_fk_event'), nullable=False)
    event_attribute_type_id = Column('event_attribute_type', Integer, ForeignKey(apply_schema('event_attribute_type.id', 'musicbrainz'), name='event_attribute_fk_event_attribute_type'), nullable=False)
    event_attribute_type_allowed_value_id = Column('event_attribute_type_allowed_value', Integer, ForeignKey(apply_schema('event_attribute_type_allowed_value.id', 'musicbrainz'), name='event_attribute_fk_event_attribute_type_allowed_value'))
    event_attribute_text = Column(String)

    event = relationship('Event', foreign_keys=[event_id], innerjoin=True)
    event_attribute_type = relationship('EventAttributeType', foreign_keys=[event_attribute_type_id], innerjoin=True)
    event_attribute_type_allowed_value = relationship('EventAttributeTypeAllowedValue', foreign_keys=[event_attribute_type_allowed_value_id])


class EventGIDRedirect(Base):
    __tablename__ = 'event_gid_redirect'
    __table_args__ = (
        Index('event_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='event_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('Event', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def event(self):
        return self.redirect


class EventTag(Base):
    __tablename__ = 'event_tag'
    __table_args__ = (
        Index('event_tag_idx_tag', 'tag'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    event_id = Column('event', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='event_tag_fk_event'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='event_tag_fk_tag'), nullable=False, primary_key=True)
    count = Column(Integer, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    event = relationship('Event', foreign_keys=[event_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class EventType(Base):
    __tablename__ = 'event_type'
    __table_args__ = (
        Index('event_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('event_type.id', 'musicbrainz'), name='event_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('EventType', foreign_keys=[parent_id])


class ReleaseFirstReleaseDate(Base):
    __tablename__ = 'release_first_release_date'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='release_first_release_date_fk_release', ondelete='CASCADE'), nullable=False, primary_key=True)
    year = Column(SMALLINT)
    month = Column(SMALLINT)
    day = Column(SMALLINT)

    release = relationship('Release', foreign_keys=[release_id], innerjoin=True, backref=backref('first_release', uselist=False))

    date = composite(PartialDate, year, month, day)


class RecordingFirstReleaseDate(Base):
    __tablename__ = 'recording_first_release_date'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    recording_id = Column('recording', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='recording_first_release_date_fk_recording', ondelete='CASCADE'), nullable=False, primary_key=True)
    year = Column(SMALLINT)
    month = Column(SMALLINT)
    day = Column(SMALLINT)

    recording = relationship('Recording', foreign_keys=[recording_id], innerjoin=True, backref=backref('first_release', uselist=False))

    date = composite(PartialDate, year, month, day)


class Gender(Base):
    __tablename__ = 'gender'
    __table_args__ = (
        Index('gender_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('gender.id', 'musicbrainz'), name='gender_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('Gender', foreign_keys=[parent_id])


class Genre(Base):
    __tablename__ = 'genre'
    __table_args__ = (
        Index('genre_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())


class GenreAliasType(Base):
    __tablename__ = 'genre_alias_type'
    __table_args__ = (
        Index('genre_alias_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('genre_alias_type.id', 'musicbrainz'), name='genre_alias_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('GenreAliasType', foreign_keys=[parent_id])


class GenreAlias(Base):
    __tablename__ = 'genre_alias'
    __table_args__ = (
        Index('genre_alias_idx_genre', 'genre'),
        Index('genre_alias_idx_primary', 'genre', 'locale', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    genre_id = Column('genre', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='genre_alias_fk_genre'), nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    type_id = Column('type', Integer, ForeignKey(apply_schema('genre_alias_type.id', 'musicbrainz'), name='genre_alias_fk_type'))
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    primary_for_locale = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    genre = relationship('Genre', foreign_keys=[genre_id], innerjoin=True)
    type = relationship('GenreAliasType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class GenreAnnotation(Base):
    __tablename__ = 'genre_annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    genre_id = Column('genre', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='genre_annotation_fk_genre'), nullable=False, primary_key=True)
    annotation_id = Column('annotation', Integer, ForeignKey(apply_schema('annotation.id', 'musicbrainz'), name='genre_annotation_fk_annotation'), nullable=False, primary_key=True)

    genre = relationship('Genre', foreign_keys=[genre_id], innerjoin=True)
    annotation = relationship('Annotation', foreign_keys=[annotation_id], innerjoin=True)


class InstrumentType(Base):
    __tablename__ = 'instrument_type'
    __table_args__ = (
        Index('instrument_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('instrument_type.id', 'musicbrainz'), name='instrument_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('InstrumentType', foreign_keys=[parent_id])


class Instrument(Base):
    __tablename__ = 'instrument'
    __table_args__ = (
        Index('instrument_idx_gid', 'gid', unique=True),
        Index('instrument_idx_name', 'name'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    type_id = Column('type', Integer, ForeignKey(apply_schema('instrument_type.id', 'musicbrainz'), name='instrument_fk_type'))
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    description = Column(String, nullable=False, default='', server_default=sql.text("''"))

    type = relationship('InstrumentType', foreign_keys=[type_id])


class InstrumentGIDRedirect(Base):
    __tablename__ = 'instrument_gid_redirect'
    __table_args__ = (
        Index('instrument_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='instrument_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('Instrument', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def instrument(self):
        return self.redirect


class InstrumentAliasType(Base):
    __tablename__ = 'instrument_alias_type'
    __table_args__ = (
        Index('instrument_alias_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('instrument_alias_type.id', 'musicbrainz'), name='instrument_alias_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('InstrumentAliasType', foreign_keys=[parent_id])


class InstrumentAlias(Base):
    __tablename__ = 'instrument_alias'
    __table_args__ = (
        Index('instrument_alias_idx_instrument', 'instrument'),
        Index('instrument_alias_idx_primary', 'instrument', 'locale', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    instrument_id = Column('instrument', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='instrument_alias_fk_instrument'), nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    type_id = Column('type', Integer, ForeignKey(apply_schema('instrument_alias_type.id', 'musicbrainz'), name='instrument_alias_fk_type'))
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    primary_for_locale = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    instrument = relationship('Instrument', foreign_keys=[instrument_id], innerjoin=True)
    type = relationship('InstrumentAliasType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class InstrumentAnnotation(Base):
    __tablename__ = 'instrument_annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    instrument_id = Column('instrument', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='instrument_annotation_fk_instrument'), nullable=False, primary_key=True)
    annotation_id = Column('annotation', Integer, ForeignKey(apply_schema('annotation.id', 'musicbrainz'), name='instrument_annotation_fk_annotation'), nullable=False, primary_key=True)

    instrument = relationship('Instrument', foreign_keys=[instrument_id], innerjoin=True)
    annotation = relationship('Annotation', foreign_keys=[annotation_id], innerjoin=True)


class InstrumentAttributeType(Base):
    __tablename__ = 'instrument_attribute_type'
    __table_args__ = (
        Index('instrument_attribute_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    free_text = Column(Boolean, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('instrument_attribute_type.id', 'musicbrainz'), name='instrument_attribute_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('InstrumentAttributeType', foreign_keys=[parent_id])


class InstrumentAttributeTypeAllowedValue(Base):
    __tablename__ = 'instrument_attribute_type_allowed_value'
    __table_args__ = (
        Index('instrument_attribute_type_allowed_value_idx_name', 'instrument_attribute_type'),
        Index('instrument_attribute_type_allowed_value_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    instrument_attribute_type_id = Column('instrument_attribute_type', Integer, ForeignKey(apply_schema('instrument_attribute_type.id', 'musicbrainz'), name='instrument_attribute_type_allowed_value_fk_instrument_attribute'), nullable=False)
    value = Column(String)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('instrument_attribute_type_allowed_value.id', 'musicbrainz'), name='instrument_attribute_type_allowed_value_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    instrument_attribute_type = relationship('InstrumentAttributeType', foreign_keys=[instrument_attribute_type_id], innerjoin=True)
    parent = relationship('InstrumentAttributeTypeAllowedValue', foreign_keys=[parent_id])


class InstrumentAttribute(Base):
    __tablename__ = 'instrument_attribute'
    __table_args__ = (
        Index('instrument_attribute_idx_instrument', 'instrument'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    instrument_id = Column('instrument', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='instrument_attribute_fk_instrument'), nullable=False)
    instrument_attribute_type_id = Column('instrument_attribute_type', Integer, ForeignKey(apply_schema('instrument_attribute_type.id', 'musicbrainz'), name='instrument_attribute_fk_instrument_attribute_type'), nullable=False)
    instrument_attribute_type_allowed_value_id = Column('instrument_attribute_type_allowed_value', Integer, ForeignKey(apply_schema('instrument_attribute_type_allowed_value.id', 'musicbrainz'), name='instrument_attribute_fk_instrument_attribute_type_allowed_value'))
    instrument_attribute_text = Column(String)

    instrument = relationship('Instrument', foreign_keys=[instrument_id], innerjoin=True)
    instrument_attribute_type = relationship('InstrumentAttributeType', foreign_keys=[instrument_attribute_type_id], innerjoin=True)
    instrument_attribute_type_allowed_value = relationship('InstrumentAttributeTypeAllowedValue', foreign_keys=[instrument_attribute_type_allowed_value_id])


class InstrumentTag(Base):
    __tablename__ = 'instrument_tag'
    __table_args__ = (
        Index('instrument_tag_idx_tag', 'tag'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    instrument_id = Column('instrument', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='instrument_tag_fk_instrument'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='instrument_tag_fk_tag'), nullable=False, primary_key=True)
    count = Column(Integer, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    instrument = relationship('Instrument', foreign_keys=[instrument_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class InstrumentTagRaw(Base):
    __tablename__ = 'instrument_tag_raw'
    __table_args__ = (
        Index('instrument_tag_raw_idx_instrument', 'instrument'),
        Index('instrument_tag_raw_idx_tag', 'tag'),
        Index('instrument_tag_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    instrument_id = Column('instrument', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='instrument_tag_raw_fk_instrument'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='instrument_tag_raw_fk_editor'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='instrument_tag_raw_fk_tag'), nullable=False, primary_key=True)
    is_upvote = Column(Boolean, nullable=False, default=True, server_default=sql.true())

    instrument = relationship('Instrument', foreign_keys=[instrument_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class ISO31661(Base):
    __tablename__ = 'iso_3166_1'
    __table_args__ = (
        Index('iso_3166_1_idx_area', 'area'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='iso_3166_1_fk_area'), nullable=False)
    code = Column(CHAR(2), primary_key=True)

    area = relationship('Area', foreign_keys=[area_id], innerjoin=True, backref=backref('iso_3166_1_codes'))


class ISO31662(Base):
    __tablename__ = 'iso_3166_2'
    __table_args__ = (
        Index('iso_3166_2_idx_area', 'area'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='iso_3166_2_fk_area'), nullable=False)
    code = Column(String(10), primary_key=True)

    area = relationship('Area', foreign_keys=[area_id], innerjoin=True, backref=backref('iso_3166_2_codes'))


class ISO31663(Base):
    __tablename__ = 'iso_3166_3'
    __table_args__ = (
        Index('iso_3166_3_idx_area', 'area'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='iso_3166_3_fk_area'), nullable=False)
    code = Column(CHAR(4), primary_key=True)

    area = relationship('Area', foreign_keys=[area_id], innerjoin=True, backref=backref('iso_3166_3_codes'))


class ISRC(Base):
    __tablename__ = 'isrc'
    __table_args__ = (
        Index('isrc_idx_isrc', 'isrc'),
        Index('isrc_idx_recording', 'recording'),
        Index('isrc_idx_isrc_recording', 'isrc', 'recording', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    recording_id = Column('recording', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='isrc_fk_recording'), nullable=False)
    isrc = Column(CHAR(12), nullable=False)
    source = Column(SMALLINT)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    recording = relationship('Recording', foreign_keys=[recording_id], innerjoin=True, backref=backref('isrcs'))


class ISWC(Base):
    __tablename__ = 'iswc'
    __table_args__ = (
        Index('iswc_idx_work', 'work'),
        Index('iswc_idx_iswc', 'iswc', 'work', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, nullable=False, primary_key=True)
    work_id = Column('work', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='iswc_fk_work'), nullable=False)
    iswc = Column(CHAR(15))
    source = Column(SMALLINT)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    created = Column(DateTime(timezone=True), nullable=False, server_default=sql.func.now())

    work = relationship('Work', foreign_keys=[work_id], innerjoin=True, backref=backref('iswcs'))


class LinkAreaArea(Base):
    __tablename__ = 'l_area_area'
    __table_args__ = (
        Index('l_area_area_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_area_area_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_area_area_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='l_area_area_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='l_area_area_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Area', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Area', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def area0(self):
        return self.entity0

    @hybrid_property
    def area0_id(self):
        return self.entity0_id

    @hybrid_property
    def area1(self):
        return self.entity1

    @hybrid_property
    def area1_id(self):
        return self.entity1_id


class LinkAreaArtist(Base):
    __tablename__ = 'l_area_artist'
    __table_args__ = (
        Index('l_area_artist_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_area_artist_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_area_artist_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='l_area_artist_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='l_area_artist_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Area', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Artist', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def area(self):
        return self.entity0

    @hybrid_property
    def area_id(self):
        return self.entity0_id

    @hybrid_property
    def artist(self):
        return self.entity1

    @hybrid_property
    def artist_id(self):
        return self.entity1_id


class LinkAreaEvent(Base):
    __tablename__ = 'l_area_event'
    __table_args__ = (
        Index('l_area_event_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_area_event_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_area_event_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='l_area_event_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='l_area_event_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Area', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Event', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def area(self):
        return self.entity0

    @hybrid_property
    def area_id(self):
        return self.entity0_id

    @hybrid_property
    def event(self):
        return self.entity1

    @hybrid_property
    def event_id(self):
        return self.entity1_id


class LinkAreaGenre(Base):
    __tablename__ = 'l_area_genre'
    __table_args__ = (
        Index('l_area_genre_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_area_genre_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_area_genre_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='l_area_genre_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='l_area_genre_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Area', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Genre', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def area(self):
        return self.entity0

    @hybrid_property
    def area_id(self):
        return self.entity0_id

    @hybrid_property
    def genre(self):
        return self.entity1

    @hybrid_property
    def genre_id(self):
        return self.entity1_id


class LinkAreaInstrument(Base):
    __tablename__ = 'l_area_instrument'
    __table_args__ = (
        Index('l_area_instrument_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_area_instrument_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_area_instrument_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='l_area_instrument_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='l_area_instrument_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Area', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Instrument', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def area(self):
        return self.entity0

    @hybrid_property
    def area_id(self):
        return self.entity0_id

    @hybrid_property
    def instrument(self):
        return self.entity1

    @hybrid_property
    def instrument_id(self):
        return self.entity1_id


class LinkAreaLabel(Base):
    __tablename__ = 'l_area_label'
    __table_args__ = (
        Index('l_area_label_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_area_label_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_area_label_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='l_area_label_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='l_area_label_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Area', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Label', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def area(self):
        return self.entity0

    @hybrid_property
    def area_id(self):
        return self.entity0_id

    @hybrid_property
    def label(self):
        return self.entity1

    @hybrid_property
    def label_id(self):
        return self.entity1_id


class LinkAreaMood(Base):
    __tablename__ = 'l_area_mood'
    __table_args__ = (
        Index('l_area_mood_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_area_mood_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_area_mood_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='l_area_mood_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='l_area_mood_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Area', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Mood', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def area(self):
        return self.entity0

    @hybrid_property
    def area_id(self):
        return self.entity0_id

    @hybrid_property
    def mood(self):
        return self.entity1

    @hybrid_property
    def mood_id(self):
        return self.entity1_id


class LinkAreaPlace(Base):
    __tablename__ = 'l_area_place'
    __table_args__ = (
        Index('l_area_place_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_area_place_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_area_place_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='l_area_place_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='l_area_place_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Area', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Place', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def area(self):
        return self.entity0

    @hybrid_property
    def area_id(self):
        return self.entity0_id

    @hybrid_property
    def place(self):
        return self.entity1

    @hybrid_property
    def place_id(self):
        return self.entity1_id


class LinkAreaRecording(Base):
    __tablename__ = 'l_area_recording'
    __table_args__ = (
        Index('l_area_recording_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_area_recording_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_area_recording_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='l_area_recording_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='l_area_recording_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Area', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Recording', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def area(self):
        return self.entity0

    @hybrid_property
    def area_id(self):
        return self.entity0_id

    @hybrid_property
    def recording(self):
        return self.entity1

    @hybrid_property
    def recording_id(self):
        return self.entity1_id


class LinkAreaRelease(Base):
    __tablename__ = 'l_area_release'
    __table_args__ = (
        Index('l_area_release_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_area_release_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_area_release_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='l_area_release_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='l_area_release_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Area', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Release', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def area(self):
        return self.entity0

    @hybrid_property
    def area_id(self):
        return self.entity0_id

    @hybrid_property
    def release(self):
        return self.entity1

    @hybrid_property
    def release_id(self):
        return self.entity1_id


class LinkAreaReleaseGroup(Base):
    __tablename__ = 'l_area_release_group'
    __table_args__ = (
        Index('l_area_release_group_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_area_release_group_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_area_release_group_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='l_area_release_group_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='l_area_release_group_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Area', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('ReleaseGroup', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def area(self):
        return self.entity0

    @hybrid_property
    def area_id(self):
        return self.entity0_id

    @hybrid_property
    def release_group(self):
        return self.entity1

    @hybrid_property
    def release_group_id(self):
        return self.entity1_id


class LinkAreaSeries(Base):
    __tablename__ = 'l_area_series'
    __table_args__ = (
        Index('l_area_series_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_area_series_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_area_series_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='l_area_series_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='l_area_series_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Area', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Series', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def area(self):
        return self.entity0

    @hybrid_property
    def area_id(self):
        return self.entity0_id

    @hybrid_property
    def series(self):
        return self.entity1

    @hybrid_property
    def series_id(self):
        return self.entity1_id


class LinkAreaURL(Base):
    __tablename__ = 'l_area_url'
    __table_args__ = (
        Index('l_area_url_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_area_url_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_area_url_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='l_area_url_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='l_area_url_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Area', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('URL', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def area(self):
        return self.entity0

    @hybrid_property
    def area_id(self):
        return self.entity0_id

    @hybrid_property
    def url(self):
        return self.entity1

    @hybrid_property
    def url_id(self):
        return self.entity1_id


class LinkAreaWork(Base):
    __tablename__ = 'l_area_work'
    __table_args__ = (
        Index('l_area_work_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_area_work_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_area_work_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='l_area_work_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='l_area_work_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Area', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Work', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def area(self):
        return self.entity0

    @hybrid_property
    def area_id(self):
        return self.entity0_id

    @hybrid_property
    def work(self):
        return self.entity1

    @hybrid_property
    def work_id(self):
        return self.entity1_id


class LinkArtistArtist(Base):
    __tablename__ = 'l_artist_artist'
    __table_args__ = (
        Index('l_artist_artist_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_artist_artist_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_artist_artist_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='l_artist_artist_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='l_artist_artist_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Artist', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Artist', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def artist0(self):
        return self.entity0

    @hybrid_property
    def artist0_id(self):
        return self.entity0_id

    @hybrid_property
    def artist1(self):
        return self.entity1

    @hybrid_property
    def artist1_id(self):
        return self.entity1_id


class LinkArtistEvent(Base):
    __tablename__ = 'l_artist_event'
    __table_args__ = (
        Index('l_artist_event_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_artist_event_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_artist_event_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='l_artist_event_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='l_artist_event_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Artist', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Event', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def artist(self):
        return self.entity0

    @hybrid_property
    def artist_id(self):
        return self.entity0_id

    @hybrid_property
    def event(self):
        return self.entity1

    @hybrid_property
    def event_id(self):
        return self.entity1_id


class LinkArtistGenre(Base):
    __tablename__ = 'l_artist_genre'
    __table_args__ = (
        Index('l_artist_genre_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_artist_genre_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_artist_genre_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='l_artist_genre_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='l_artist_genre_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Artist', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Genre', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def artist(self):
        return self.entity0

    @hybrid_property
    def artist_id(self):
        return self.entity0_id

    @hybrid_property
    def genre(self):
        return self.entity1

    @hybrid_property
    def genre_id(self):
        return self.entity1_id


class LinkArtistInstrument(Base):
    __tablename__ = 'l_artist_instrument'
    __table_args__ = (
        Index('l_artist_instrument_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_artist_instrument_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_artist_instrument_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='l_artist_instrument_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='l_artist_instrument_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Artist', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Instrument', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def artist(self):
        return self.entity0

    @hybrid_property
    def artist_id(self):
        return self.entity0_id

    @hybrid_property
    def instrument(self):
        return self.entity1

    @hybrid_property
    def instrument_id(self):
        return self.entity1_id


class LinkArtistLabel(Base):
    __tablename__ = 'l_artist_label'
    __table_args__ = (
        Index('l_artist_label_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_artist_label_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_artist_label_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='l_artist_label_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='l_artist_label_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Artist', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Label', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def artist(self):
        return self.entity0

    @hybrid_property
    def artist_id(self):
        return self.entity0_id

    @hybrid_property
    def label(self):
        return self.entity1

    @hybrid_property
    def label_id(self):
        return self.entity1_id


class LinkArtistMood(Base):
    __tablename__ = 'l_artist_mood'
    __table_args__ = (
        Index('l_artist_mood_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_artist_mood_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_artist_mood_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='l_artist_mood_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='l_artist_mood_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Artist', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Mood', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def artist(self):
        return self.entity0

    @hybrid_property
    def artist_id(self):
        return self.entity0_id

    @hybrid_property
    def mood(self):
        return self.entity1

    @hybrid_property
    def mood_id(self):
        return self.entity1_id


class LinkArtistPlace(Base):
    __tablename__ = 'l_artist_place'
    __table_args__ = (
        Index('l_artist_place_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_artist_place_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_artist_place_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='l_artist_place_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='l_artist_place_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Artist', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Place', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def artist(self):
        return self.entity0

    @hybrid_property
    def artist_id(self):
        return self.entity0_id

    @hybrid_property
    def place(self):
        return self.entity1

    @hybrid_property
    def place_id(self):
        return self.entity1_id


class LinkArtistRecording(Base):
    __tablename__ = 'l_artist_recording'
    __table_args__ = (
        Index('l_artist_recording_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_artist_recording_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_artist_recording_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='l_artist_recording_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='l_artist_recording_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Artist', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Recording', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def artist(self):
        return self.entity0

    @hybrid_property
    def artist_id(self):
        return self.entity0_id

    @hybrid_property
    def recording(self):
        return self.entity1

    @hybrid_property
    def recording_id(self):
        return self.entity1_id


class LinkArtistRelease(Base):
    __tablename__ = 'l_artist_release'
    __table_args__ = (
        Index('l_artist_release_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_artist_release_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_artist_release_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='l_artist_release_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='l_artist_release_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Artist', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Release', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def artist(self):
        return self.entity0

    @hybrid_property
    def artist_id(self):
        return self.entity0_id

    @hybrid_property
    def release(self):
        return self.entity1

    @hybrid_property
    def release_id(self):
        return self.entity1_id


class LinkArtistReleaseGroup(Base):
    __tablename__ = 'l_artist_release_group'
    __table_args__ = (
        Index('l_artist_release_group_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_artist_release_group_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_artist_release_group_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='l_artist_release_group_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='l_artist_release_group_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Artist', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('ReleaseGroup', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def artist(self):
        return self.entity0

    @hybrid_property
    def artist_id(self):
        return self.entity0_id

    @hybrid_property
    def release_group(self):
        return self.entity1

    @hybrid_property
    def release_group_id(self):
        return self.entity1_id


class LinkArtistSeries(Base):
    __tablename__ = 'l_artist_series'
    __table_args__ = (
        Index('l_artist_series_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_artist_series_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_artist_series_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='l_artist_series_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='l_artist_series_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Artist', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Series', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def artist(self):
        return self.entity0

    @hybrid_property
    def artist_id(self):
        return self.entity0_id

    @hybrid_property
    def series(self):
        return self.entity1

    @hybrid_property
    def series_id(self):
        return self.entity1_id


class LinkArtistURL(Base):
    __tablename__ = 'l_artist_url'
    __table_args__ = (
        Index('l_artist_url_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_artist_url_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_artist_url_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='l_artist_url_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='l_artist_url_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Artist', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('URL', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def artist(self):
        return self.entity0

    @hybrid_property
    def artist_id(self):
        return self.entity0_id

    @hybrid_property
    def url(self):
        return self.entity1

    @hybrid_property
    def url_id(self):
        return self.entity1_id


class LinkArtistWork(Base):
    __tablename__ = 'l_artist_work'
    __table_args__ = (
        Index('l_artist_work_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_artist_work_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_artist_work_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='l_artist_work_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='l_artist_work_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Artist', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Work', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def artist(self):
        return self.entity0

    @hybrid_property
    def artist_id(self):
        return self.entity0_id

    @hybrid_property
    def work(self):
        return self.entity1

    @hybrid_property
    def work_id(self):
        return self.entity1_id


class LinkEventEvent(Base):
    __tablename__ = 'l_event_event'
    __table_args__ = (
        Index('l_event_event_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_event_event_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_event_event_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='l_event_event_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='l_event_event_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Event', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Event', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def event0(self):
        return self.entity0

    @hybrid_property
    def event0_id(self):
        return self.entity0_id

    @hybrid_property
    def event1(self):
        return self.entity1

    @hybrid_property
    def event1_id(self):
        return self.entity1_id


class LinkEventGenre(Base):
    __tablename__ = 'l_event_genre'
    __table_args__ = (
        Index('l_event_genre_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_event_genre_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_event_genre_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='l_event_genre_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='l_event_genre_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Event', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Genre', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def event(self):
        return self.entity0

    @hybrid_property
    def event_id(self):
        return self.entity0_id

    @hybrid_property
    def genre(self):
        return self.entity1

    @hybrid_property
    def genre_id(self):
        return self.entity1_id


class LinkEventInstrument(Base):
    __tablename__ = 'l_event_instrument'
    __table_args__ = (
        Index('l_event_instrument_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_event_instrument_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_event_instrument_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='l_event_instrument_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='l_event_instrument_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Event', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Instrument', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def event(self):
        return self.entity0

    @hybrid_property
    def event_id(self):
        return self.entity0_id

    @hybrid_property
    def instrument(self):
        return self.entity1

    @hybrid_property
    def instrument_id(self):
        return self.entity1_id


class LinkEventLabel(Base):
    __tablename__ = 'l_event_label'
    __table_args__ = (
        Index('l_event_label_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_event_label_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_event_label_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='l_event_label_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='l_event_label_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Event', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Label', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def event(self):
        return self.entity0

    @hybrid_property
    def event_id(self):
        return self.entity0_id

    @hybrid_property
    def label(self):
        return self.entity1

    @hybrid_property
    def label_id(self):
        return self.entity1_id


class LinkEventMood(Base):
    __tablename__ = 'l_event_mood'
    __table_args__ = (
        Index('l_event_mood_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_event_mood_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_event_mood_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='l_event_mood_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='l_event_mood_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Event', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Mood', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def event(self):
        return self.entity0

    @hybrid_property
    def event_id(self):
        return self.entity0_id

    @hybrid_property
    def mood(self):
        return self.entity1

    @hybrid_property
    def mood_id(self):
        return self.entity1_id


class LinkEventPlace(Base):
    __tablename__ = 'l_event_place'
    __table_args__ = (
        Index('l_event_place_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_event_place_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_event_place_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='l_event_place_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='l_event_place_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Event', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Place', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def event(self):
        return self.entity0

    @hybrid_property
    def event_id(self):
        return self.entity0_id

    @hybrid_property
    def place(self):
        return self.entity1

    @hybrid_property
    def place_id(self):
        return self.entity1_id


class LinkEventRecording(Base):
    __tablename__ = 'l_event_recording'
    __table_args__ = (
        Index('l_event_recording_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_event_recording_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_event_recording_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='l_event_recording_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='l_event_recording_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Event', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Recording', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def event(self):
        return self.entity0

    @hybrid_property
    def event_id(self):
        return self.entity0_id

    @hybrid_property
    def recording(self):
        return self.entity1

    @hybrid_property
    def recording_id(self):
        return self.entity1_id


class LinkEventRelease(Base):
    __tablename__ = 'l_event_release'
    __table_args__ = (
        Index('l_event_release_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_event_release_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_event_release_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='l_event_release_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='l_event_release_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Event', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Release', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def event(self):
        return self.entity0

    @hybrid_property
    def event_id(self):
        return self.entity0_id

    @hybrid_property
    def release(self):
        return self.entity1

    @hybrid_property
    def release_id(self):
        return self.entity1_id


class LinkEventReleaseGroup(Base):
    __tablename__ = 'l_event_release_group'
    __table_args__ = (
        Index('l_event_release_group_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_event_release_group_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_event_release_group_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='l_event_release_group_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='l_event_release_group_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Event', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('ReleaseGroup', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def event(self):
        return self.entity0

    @hybrid_property
    def event_id(self):
        return self.entity0_id

    @hybrid_property
    def release_group(self):
        return self.entity1

    @hybrid_property
    def release_group_id(self):
        return self.entity1_id


class LinkEventSeries(Base):
    __tablename__ = 'l_event_series'
    __table_args__ = (
        Index('l_event_series_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_event_series_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_event_series_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='l_event_series_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='l_event_series_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Event', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Series', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def event(self):
        return self.entity0

    @hybrid_property
    def event_id(self):
        return self.entity0_id

    @hybrid_property
    def series(self):
        return self.entity1

    @hybrid_property
    def series_id(self):
        return self.entity1_id


class LinkEventURL(Base):
    __tablename__ = 'l_event_url'
    __table_args__ = (
        Index('l_event_url_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_event_url_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_event_url_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='l_event_url_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='l_event_url_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Event', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('URL', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def event(self):
        return self.entity0

    @hybrid_property
    def event_id(self):
        return self.entity0_id

    @hybrid_property
    def url(self):
        return self.entity1

    @hybrid_property
    def url_id(self):
        return self.entity1_id


class LinkEventWork(Base):
    __tablename__ = 'l_event_work'
    __table_args__ = (
        Index('l_event_work_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_event_work_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_event_work_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='l_event_work_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='l_event_work_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Event', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Work', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def event(self):
        return self.entity0

    @hybrid_property
    def event_id(self):
        return self.entity0_id

    @hybrid_property
    def work(self):
        return self.entity1

    @hybrid_property
    def work_id(self):
        return self.entity1_id


class LinkLabelLabel(Base):
    __tablename__ = 'l_label_label'
    __table_args__ = (
        Index('l_label_label_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_label_label_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_label_label_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='l_label_label_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='l_label_label_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Label', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Label', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def label0(self):
        return self.entity0

    @hybrid_property
    def label0_id(self):
        return self.entity0_id

    @hybrid_property
    def label1(self):
        return self.entity1

    @hybrid_property
    def label1_id(self):
        return self.entity1_id


class LinkGenreGenre(Base):
    __tablename__ = 'l_genre_genre'
    __table_args__ = (
        Index('l_genre_genre_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_genre_genre_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_genre_genre_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='l_genre_genre_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='l_genre_genre_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Genre', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Genre', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def genre0(self):
        return self.entity0

    @hybrid_property
    def genre0_id(self):
        return self.entity0_id

    @hybrid_property
    def genre1(self):
        return self.entity1

    @hybrid_property
    def genre1_id(self):
        return self.entity1_id


class LinkGenreInstrument(Base):
    __tablename__ = 'l_genre_instrument'
    __table_args__ = (
        Index('l_genre_instrument_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_genre_instrument_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_genre_instrument_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='l_genre_instrument_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='l_genre_instrument_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Genre', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Instrument', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def genre(self):
        return self.entity0

    @hybrid_property
    def genre_id(self):
        return self.entity0_id

    @hybrid_property
    def instrument(self):
        return self.entity1

    @hybrid_property
    def instrument_id(self):
        return self.entity1_id


class LinkGenreLabel(Base):
    __tablename__ = 'l_genre_label'
    __table_args__ = (
        Index('l_genre_label_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_genre_label_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_genre_label_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='l_genre_label_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='l_genre_label_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Genre', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Label', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def genre(self):
        return self.entity0

    @hybrid_property
    def genre_id(self):
        return self.entity0_id

    @hybrid_property
    def label(self):
        return self.entity1

    @hybrid_property
    def label_id(self):
        return self.entity1_id


class LinkGenreMood(Base):
    __tablename__ = 'l_genre_mood'
    __table_args__ = (
        Index('l_genre_mood_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_genre_mood_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_genre_mood_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='l_genre_mood_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='l_genre_mood_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Genre', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Mood', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def genre(self):
        return self.entity0

    @hybrid_property
    def genre_id(self):
        return self.entity0_id

    @hybrid_property
    def mood(self):
        return self.entity1

    @hybrid_property
    def mood_id(self):
        return self.entity1_id


class LinkGenrePlace(Base):
    __tablename__ = 'l_genre_place'
    __table_args__ = (
        Index('l_genre_place_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_genre_place_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_genre_place_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='l_genre_place_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='l_genre_place_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Genre', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Place', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def genre(self):
        return self.entity0

    @hybrid_property
    def genre_id(self):
        return self.entity0_id

    @hybrid_property
    def place(self):
        return self.entity1

    @hybrid_property
    def place_id(self):
        return self.entity1_id


class LinkGenreRecording(Base):
    __tablename__ = 'l_genre_recording'
    __table_args__ = (
        Index('l_genre_recording_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_genre_recording_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_genre_recording_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='l_genre_recording_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='l_genre_recording_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Genre', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Recording', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def genre(self):
        return self.entity0

    @hybrid_property
    def genre_id(self):
        return self.entity0_id

    @hybrid_property
    def recording(self):
        return self.entity1

    @hybrid_property
    def recording_id(self):
        return self.entity1_id


class LinkGenreRelease(Base):
    __tablename__ = 'l_genre_release'
    __table_args__ = (
        Index('l_genre_release_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_genre_release_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_genre_release_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='l_genre_release_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='l_genre_release_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Genre', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Release', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def genre(self):
        return self.entity0

    @hybrid_property
    def genre_id(self):
        return self.entity0_id

    @hybrid_property
    def release(self):
        return self.entity1

    @hybrid_property
    def release_id(self):
        return self.entity1_id


class LinkGenreReleaseGroup(Base):
    __tablename__ = 'l_genre_release_group'
    __table_args__ = (
        Index('l_genre_release_group_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_genre_release_group_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_genre_release_group_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='l_genre_release_group_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='l_genre_release_group_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Genre', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('ReleaseGroup', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def genre(self):
        return self.entity0

    @hybrid_property
    def genre_id(self):
        return self.entity0_id

    @hybrid_property
    def release_group(self):
        return self.entity1

    @hybrid_property
    def release_group_id(self):
        return self.entity1_id


class LinkGenreSeries(Base):
    __tablename__ = 'l_genre_series'
    __table_args__ = (
        Index('l_genre_series_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_genre_series_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_genre_series_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='l_genre_series_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='l_genre_series_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Genre', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Series', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def genre(self):
        return self.entity0

    @hybrid_property
    def genre_id(self):
        return self.entity0_id

    @hybrid_property
    def series(self):
        return self.entity1

    @hybrid_property
    def series_id(self):
        return self.entity1_id


class LinkGenreURL(Base):
    __tablename__ = 'l_genre_url'
    __table_args__ = (
        Index('l_genre_url_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_genre_url_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_genre_url_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='l_genre_url_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='l_genre_url_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Genre', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('URL', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def genre(self):
        return self.entity0

    @hybrid_property
    def genre_id(self):
        return self.entity0_id

    @hybrid_property
    def url(self):
        return self.entity1

    @hybrid_property
    def url_id(self):
        return self.entity1_id


class LinkGenreWork(Base):
    __tablename__ = 'l_genre_work'
    __table_args__ = (
        Index('l_genre_work_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_genre_work_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_genre_work_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='l_genre_work_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='l_genre_work_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Genre', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Work', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def genre(self):
        return self.entity0

    @hybrid_property
    def genre_id(self):
        return self.entity0_id

    @hybrid_property
    def work(self):
        return self.entity1

    @hybrid_property
    def work_id(self):
        return self.entity1_id


class LinkInstrumentInstrument(Base):
    __tablename__ = 'l_instrument_instrument'
    __table_args__ = (
        Index('l_instrument_instrument_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_instrument_instrument_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_instrument_instrument_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='l_instrument_instrument_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='l_instrument_instrument_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Instrument', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Instrument', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def instrument0(self):
        return self.entity0

    @hybrid_property
    def instrument0_id(self):
        return self.entity0_id

    @hybrid_property
    def instrument1(self):
        return self.entity1

    @hybrid_property
    def instrument1_id(self):
        return self.entity1_id


class LinkInstrumentLabel(Base):
    __tablename__ = 'l_instrument_label'
    __table_args__ = (
        Index('l_instrument_label_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_instrument_label_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_instrument_label_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='l_instrument_label_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='l_instrument_label_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Instrument', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Label', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def instrument(self):
        return self.entity0

    @hybrid_property
    def instrument_id(self):
        return self.entity0_id

    @hybrid_property
    def label(self):
        return self.entity1

    @hybrid_property
    def label_id(self):
        return self.entity1_id


class LinkInstrumentMood(Base):
    __tablename__ = 'l_instrument_mood'
    __table_args__ = (
        Index('l_instrument_mood_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_instrument_mood_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_instrument_mood_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='l_instrument_mood_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='l_instrument_mood_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Instrument', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Mood', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def instrument(self):
        return self.entity0

    @hybrid_property
    def instrument_id(self):
        return self.entity0_id

    @hybrid_property
    def mood(self):
        return self.entity1

    @hybrid_property
    def mood_id(self):
        return self.entity1_id


class LinkInstrumentPlace(Base):
    __tablename__ = 'l_instrument_place'
    __table_args__ = (
        Index('l_instrument_place_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_instrument_place_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_instrument_place_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='l_instrument_place_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='l_instrument_place_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Instrument', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Place', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def instrument(self):
        return self.entity0

    @hybrid_property
    def instrument_id(self):
        return self.entity0_id

    @hybrid_property
    def place(self):
        return self.entity1

    @hybrid_property
    def place_id(self):
        return self.entity1_id


class LinkInstrumentRecording(Base):
    __tablename__ = 'l_instrument_recording'
    __table_args__ = (
        Index('l_instrument_recording_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_instrument_recording_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_instrument_recording_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='l_instrument_recording_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='l_instrument_recording_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Instrument', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Recording', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def instrument(self):
        return self.entity0

    @hybrid_property
    def instrument_id(self):
        return self.entity0_id

    @hybrid_property
    def recording(self):
        return self.entity1

    @hybrid_property
    def recording_id(self):
        return self.entity1_id


class LinkInstrumentRelease(Base):
    __tablename__ = 'l_instrument_release'
    __table_args__ = (
        Index('l_instrument_release_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_instrument_release_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_instrument_release_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='l_instrument_release_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='l_instrument_release_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Instrument', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Release', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def instrument(self):
        return self.entity0

    @hybrid_property
    def instrument_id(self):
        return self.entity0_id

    @hybrid_property
    def release(self):
        return self.entity1

    @hybrid_property
    def release_id(self):
        return self.entity1_id


class LinkInstrumentReleaseGroup(Base):
    __tablename__ = 'l_instrument_release_group'
    __table_args__ = (
        Index('l_instrument_release_group_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_instrument_release_group_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_instrument_release_group_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='l_instrument_release_group_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='l_instrument_release_group_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Instrument', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('ReleaseGroup', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def instrument(self):
        return self.entity0

    @hybrid_property
    def instrument_id(self):
        return self.entity0_id

    @hybrid_property
    def release_group(self):
        return self.entity1

    @hybrid_property
    def release_group_id(self):
        return self.entity1_id


class LinkInstrumentSeries(Base):
    __tablename__ = 'l_instrument_series'
    __table_args__ = (
        Index('l_instrument_series_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_instrument_series_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_instrument_series_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='l_instrument_series_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='l_instrument_series_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Instrument', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Series', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def instrument(self):
        return self.entity0

    @hybrid_property
    def instrument_id(self):
        return self.entity0_id

    @hybrid_property
    def series(self):
        return self.entity1

    @hybrid_property
    def series_id(self):
        return self.entity1_id


class LinkInstrumentURL(Base):
    __tablename__ = 'l_instrument_url'
    __table_args__ = (
        Index('l_instrument_url_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_instrument_url_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_instrument_url_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='l_instrument_url_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='l_instrument_url_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Instrument', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('URL', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def instrument(self):
        return self.entity0

    @hybrid_property
    def instrument_id(self):
        return self.entity0_id

    @hybrid_property
    def url(self):
        return self.entity1

    @hybrid_property
    def url_id(self):
        return self.entity1_id


class LinkInstrumentWork(Base):
    __tablename__ = 'l_instrument_work'
    __table_args__ = (
        Index('l_instrument_work_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_instrument_work_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_instrument_work_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='l_instrument_work_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='l_instrument_work_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Instrument', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Work', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def instrument(self):
        return self.entity0

    @hybrid_property
    def instrument_id(self):
        return self.entity0_id

    @hybrid_property
    def work(self):
        return self.entity1

    @hybrid_property
    def work_id(self):
        return self.entity1_id


class LinkLabelMood(Base):
    __tablename__ = 'l_label_mood'
    __table_args__ = (
        Index('l_label_mood_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_label_mood_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_label_mood_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='l_label_mood_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='l_label_mood_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Label', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Mood', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def label(self):
        return self.entity0

    @hybrid_property
    def label_id(self):
        return self.entity0_id

    @hybrid_property
    def mood(self):
        return self.entity1

    @hybrid_property
    def mood_id(self):
        return self.entity1_id


class LinkLabelPlace(Base):
    __tablename__ = 'l_label_place'
    __table_args__ = (
        Index('l_label_place_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_label_place_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_label_place_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='l_label_place_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='l_label_place_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Label', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Place', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def label(self):
        return self.entity0

    @hybrid_property
    def label_id(self):
        return self.entity0_id

    @hybrid_property
    def place(self):
        return self.entity1

    @hybrid_property
    def place_id(self):
        return self.entity1_id


class LinkLabelRecording(Base):
    __tablename__ = 'l_label_recording'
    __table_args__ = (
        Index('l_label_recording_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_label_recording_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_label_recording_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='l_label_recording_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='l_label_recording_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Label', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Recording', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def label(self):
        return self.entity0

    @hybrid_property
    def label_id(self):
        return self.entity0_id

    @hybrid_property
    def recording(self):
        return self.entity1

    @hybrid_property
    def recording_id(self):
        return self.entity1_id


class LinkLabelRelease(Base):
    __tablename__ = 'l_label_release'
    __table_args__ = (
        Index('l_label_release_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_label_release_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_label_release_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='l_label_release_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='l_label_release_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Label', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Release', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def label(self):
        return self.entity0

    @hybrid_property
    def label_id(self):
        return self.entity0_id

    @hybrid_property
    def release(self):
        return self.entity1

    @hybrid_property
    def release_id(self):
        return self.entity1_id


class LinkLabelReleaseGroup(Base):
    __tablename__ = 'l_label_release_group'
    __table_args__ = (
        Index('l_label_release_group_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_label_release_group_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_label_release_group_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='l_label_release_group_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='l_label_release_group_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Label', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('ReleaseGroup', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def label(self):
        return self.entity0

    @hybrid_property
    def label_id(self):
        return self.entity0_id

    @hybrid_property
    def release_group(self):
        return self.entity1

    @hybrid_property
    def release_group_id(self):
        return self.entity1_id


class LinkLabelSeries(Base):
    __tablename__ = 'l_label_series'
    __table_args__ = (
        Index('l_label_series_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_label_series_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_label_series_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='l_label_series_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='l_label_series_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Label', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Series', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def label(self):
        return self.entity0

    @hybrid_property
    def label_id(self):
        return self.entity0_id

    @hybrid_property
    def series(self):
        return self.entity1

    @hybrid_property
    def series_id(self):
        return self.entity1_id


class LinkLabelURL(Base):
    __tablename__ = 'l_label_url'
    __table_args__ = (
        Index('l_label_url_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_label_url_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_label_url_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='l_label_url_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='l_label_url_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Label', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('URL', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def label(self):
        return self.entity0

    @hybrid_property
    def label_id(self):
        return self.entity0_id

    @hybrid_property
    def url(self):
        return self.entity1

    @hybrid_property
    def url_id(self):
        return self.entity1_id


class LinkLabelWork(Base):
    __tablename__ = 'l_label_work'
    __table_args__ = (
        Index('l_label_work_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_label_work_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_label_work_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='l_label_work_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='l_label_work_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Label', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Work', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def label(self):
        return self.entity0

    @hybrid_property
    def label_id(self):
        return self.entity0_id

    @hybrid_property
    def work(self):
        return self.entity1

    @hybrid_property
    def work_id(self):
        return self.entity1_id


class LinkMoodMood(Base):
    __tablename__ = 'l_mood_mood'
    __table_args__ = (
        Index('l_mood_mood_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_mood_mood_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_mood_mood_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='l_mood_mood_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='l_mood_mood_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Mood', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Mood', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def mood0(self):
        return self.entity0

    @hybrid_property
    def mood0_id(self):
        return self.entity0_id

    @hybrid_property
    def mood1(self):
        return self.entity1

    @hybrid_property
    def mood1_id(self):
        return self.entity1_id


class LinkMoodPlace(Base):
    __tablename__ = 'l_mood_place'
    __table_args__ = (
        Index('l_mood_place_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_mood_place_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_mood_place_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='l_mood_place_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='l_mood_place_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Mood', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Place', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def mood(self):
        return self.entity0

    @hybrid_property
    def mood_id(self):
        return self.entity0_id

    @hybrid_property
    def place(self):
        return self.entity1

    @hybrid_property
    def place_id(self):
        return self.entity1_id


class LinkMoodRecording(Base):
    __tablename__ = 'l_mood_recording'
    __table_args__ = (
        Index('l_mood_recording_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_mood_recording_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_mood_recording_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='l_mood_recording_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='l_mood_recording_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Mood', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Recording', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def mood(self):
        return self.entity0

    @hybrid_property
    def mood_id(self):
        return self.entity0_id

    @hybrid_property
    def recording(self):
        return self.entity1

    @hybrid_property
    def recording_id(self):
        return self.entity1_id


class LinkMoodRelease(Base):
    __tablename__ = 'l_mood_release'
    __table_args__ = (
        Index('l_mood_release_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_mood_release_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_mood_release_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='l_mood_release_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='l_mood_release_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Mood', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Release', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def mood(self):
        return self.entity0

    @hybrid_property
    def mood_id(self):
        return self.entity0_id

    @hybrid_property
    def release(self):
        return self.entity1

    @hybrid_property
    def release_id(self):
        return self.entity1_id


class LinkMoodReleaseGroup(Base):
    __tablename__ = 'l_mood_release_group'
    __table_args__ = (
        Index('l_mood_release_group_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_mood_release_group_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_mood_release_group_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='l_mood_release_group_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='l_mood_release_group_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Mood', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('ReleaseGroup', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def mood(self):
        return self.entity0

    @hybrid_property
    def mood_id(self):
        return self.entity0_id

    @hybrid_property
    def release_group(self):
        return self.entity1

    @hybrid_property
    def release_group_id(self):
        return self.entity1_id


class LinkMoodSeries(Base):
    __tablename__ = 'l_mood_series'
    __table_args__ = (
        Index('l_mood_series_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_mood_series_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_mood_series_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='l_mood_series_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='l_mood_series_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Mood', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Series', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def mood(self):
        return self.entity0

    @hybrid_property
    def mood_id(self):
        return self.entity0_id

    @hybrid_property
    def series(self):
        return self.entity1

    @hybrid_property
    def series_id(self):
        return self.entity1_id


class LinkMoodURL(Base):
    __tablename__ = 'l_mood_url'
    __table_args__ = (
        Index('l_mood_url_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_mood_url_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_mood_url_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='l_mood_url_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='l_mood_url_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Mood', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('URL', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def mood(self):
        return self.entity0

    @hybrid_property
    def mood_id(self):
        return self.entity0_id

    @hybrid_property
    def url(self):
        return self.entity1

    @hybrid_property
    def url_id(self):
        return self.entity1_id


class LinkMoodWork(Base):
    __tablename__ = 'l_mood_work'
    __table_args__ = (
        Index('l_mood_work_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_mood_work_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_mood_work_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='l_mood_work_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='l_mood_work_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Mood', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Work', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def mood(self):
        return self.entity0

    @hybrid_property
    def mood_id(self):
        return self.entity0_id

    @hybrid_property
    def work(self):
        return self.entity1

    @hybrid_property
    def work_id(self):
        return self.entity1_id


class LinkPlacePlace(Base):
    __tablename__ = 'l_place_place'
    __table_args__ = (
        Index('l_place_place_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_place_place_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_place_place_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='l_place_place_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='l_place_place_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Place', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Place', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def place0(self):
        return self.entity0

    @hybrid_property
    def place0_id(self):
        return self.entity0_id

    @hybrid_property
    def place1(self):
        return self.entity1

    @hybrid_property
    def place1_id(self):
        return self.entity1_id


class LinkPlaceRecording(Base):
    __tablename__ = 'l_place_recording'
    __table_args__ = (
        Index('l_place_recording_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_place_recording_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_place_recording_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='l_place_recording_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='l_place_recording_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Place', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Recording', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def place(self):
        return self.entity0

    @hybrid_property
    def place_id(self):
        return self.entity0_id

    @hybrid_property
    def recording(self):
        return self.entity1

    @hybrid_property
    def recording_id(self):
        return self.entity1_id


class LinkPlaceRelease(Base):
    __tablename__ = 'l_place_release'
    __table_args__ = (
        Index('l_place_release_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_place_release_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_place_release_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='l_place_release_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='l_place_release_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Place', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Release', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def place(self):
        return self.entity0

    @hybrid_property
    def place_id(self):
        return self.entity0_id

    @hybrid_property
    def release(self):
        return self.entity1

    @hybrid_property
    def release_id(self):
        return self.entity1_id


class LinkPlaceReleaseGroup(Base):
    __tablename__ = 'l_place_release_group'
    __table_args__ = (
        Index('l_place_release_group_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_place_release_group_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_place_release_group_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='l_place_release_group_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='l_place_release_group_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Place', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('ReleaseGroup', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def place(self):
        return self.entity0

    @hybrid_property
    def place_id(self):
        return self.entity0_id

    @hybrid_property
    def release_group(self):
        return self.entity1

    @hybrid_property
    def release_group_id(self):
        return self.entity1_id


class LinkPlaceSeries(Base):
    __tablename__ = 'l_place_series'
    __table_args__ = (
        Index('l_place_series_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_place_series_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_place_series_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='l_place_series_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='l_place_series_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Place', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Series', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def place(self):
        return self.entity0

    @hybrid_property
    def place_id(self):
        return self.entity0_id

    @hybrid_property
    def series(self):
        return self.entity1

    @hybrid_property
    def series_id(self):
        return self.entity1_id


class LinkPlaceURL(Base):
    __tablename__ = 'l_place_url'
    __table_args__ = (
        Index('l_place_url_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_place_url_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_place_url_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='l_place_url_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='l_place_url_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Place', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('URL', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def place(self):
        return self.entity0

    @hybrid_property
    def place_id(self):
        return self.entity0_id

    @hybrid_property
    def url(self):
        return self.entity1

    @hybrid_property
    def url_id(self):
        return self.entity1_id


class LinkPlaceWork(Base):
    __tablename__ = 'l_place_work'
    __table_args__ = (
        Index('l_place_work_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_place_work_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_place_work_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='l_place_work_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='l_place_work_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Place', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Work', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def place(self):
        return self.entity0

    @hybrid_property
    def place_id(self):
        return self.entity0_id

    @hybrid_property
    def work(self):
        return self.entity1

    @hybrid_property
    def work_id(self):
        return self.entity1_id


class LinkRecordingRecording(Base):
    __tablename__ = 'l_recording_recording'
    __table_args__ = (
        Index('l_recording_recording_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_recording_recording_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_recording_recording_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='l_recording_recording_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='l_recording_recording_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Recording', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Recording', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def recording0(self):
        return self.entity0

    @hybrid_property
    def recording0_id(self):
        return self.entity0_id

    @hybrid_property
    def recording1(self):
        return self.entity1

    @hybrid_property
    def recording1_id(self):
        return self.entity1_id


class LinkRecordingRelease(Base):
    __tablename__ = 'l_recording_release'
    __table_args__ = (
        Index('l_recording_release_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_recording_release_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_recording_release_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='l_recording_release_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='l_recording_release_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Recording', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Release', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def recording(self):
        return self.entity0

    @hybrid_property
    def recording_id(self):
        return self.entity0_id

    @hybrid_property
    def release(self):
        return self.entity1

    @hybrid_property
    def release_id(self):
        return self.entity1_id


class LinkRecordingReleaseGroup(Base):
    __tablename__ = 'l_recording_release_group'
    __table_args__ = (
        Index('l_recording_release_group_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_recording_release_group_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_recording_release_group_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='l_recording_release_group_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='l_recording_release_group_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Recording', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('ReleaseGroup', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def recording(self):
        return self.entity0

    @hybrid_property
    def recording_id(self):
        return self.entity0_id

    @hybrid_property
    def release_group(self):
        return self.entity1

    @hybrid_property
    def release_group_id(self):
        return self.entity1_id


class LinkRecordingSeries(Base):
    __tablename__ = 'l_recording_series'
    __table_args__ = (
        Index('l_recording_series_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_recording_series_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_recording_series_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='l_recording_series_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='l_recording_series_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Recording', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Series', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def recording(self):
        return self.entity0

    @hybrid_property
    def recording_id(self):
        return self.entity0_id

    @hybrid_property
    def series(self):
        return self.entity1

    @hybrid_property
    def series_id(self):
        return self.entity1_id


class LinkRecordingURL(Base):
    __tablename__ = 'l_recording_url'
    __table_args__ = (
        Index('l_recording_url_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_recording_url_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_recording_url_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='l_recording_url_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='l_recording_url_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Recording', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('URL', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def recording(self):
        return self.entity0

    @hybrid_property
    def recording_id(self):
        return self.entity0_id

    @hybrid_property
    def url(self):
        return self.entity1

    @hybrid_property
    def url_id(self):
        return self.entity1_id


class LinkRecordingWork(Base):
    __tablename__ = 'l_recording_work'
    __table_args__ = (
        Index('l_recording_work_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_recording_work_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_recording_work_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='l_recording_work_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='l_recording_work_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Recording', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Work', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def recording(self):
        return self.entity0

    @hybrid_property
    def recording_id(self):
        return self.entity0_id

    @hybrid_property
    def work(self):
        return self.entity1

    @hybrid_property
    def work_id(self):
        return self.entity1_id


class LinkReleaseRelease(Base):
    __tablename__ = 'l_release_release'
    __table_args__ = (
        Index('l_release_release_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_release_release_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_release_release_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='l_release_release_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='l_release_release_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Release', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Release', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def release0(self):
        return self.entity0

    @hybrid_property
    def release0_id(self):
        return self.entity0_id

    @hybrid_property
    def release1(self):
        return self.entity1

    @hybrid_property
    def release1_id(self):
        return self.entity1_id


class LinkReleaseReleaseGroup(Base):
    __tablename__ = 'l_release_release_group'
    __table_args__ = (
        Index('l_release_release_group_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_release_release_group_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_release_release_group_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='l_release_release_group_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='l_release_release_group_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Release', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('ReleaseGroup', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def release(self):
        return self.entity0

    @hybrid_property
    def release_id(self):
        return self.entity0_id

    @hybrid_property
    def release_group(self):
        return self.entity1

    @hybrid_property
    def release_group_id(self):
        return self.entity1_id


class LinkReleaseSeries(Base):
    __tablename__ = 'l_release_series'
    __table_args__ = (
        Index('l_release_series_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_release_series_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_release_series_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='l_release_series_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='l_release_series_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Release', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Series', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def release(self):
        return self.entity0

    @hybrid_property
    def release_id(self):
        return self.entity0_id

    @hybrid_property
    def series(self):
        return self.entity1

    @hybrid_property
    def series_id(self):
        return self.entity1_id


class LinkReleaseURL(Base):
    __tablename__ = 'l_release_url'
    __table_args__ = (
        Index('l_release_url_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_release_url_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_release_url_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='l_release_url_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='l_release_url_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Release', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('URL', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def release(self):
        return self.entity0

    @hybrid_property
    def release_id(self):
        return self.entity0_id

    @hybrid_property
    def url(self):
        return self.entity1

    @hybrid_property
    def url_id(self):
        return self.entity1_id


class LinkReleaseWork(Base):
    __tablename__ = 'l_release_work'
    __table_args__ = (
        Index('l_release_work_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_release_work_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_release_work_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='l_release_work_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='l_release_work_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Release', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Work', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def release(self):
        return self.entity0

    @hybrid_property
    def release_id(self):
        return self.entity0_id

    @hybrid_property
    def work(self):
        return self.entity1

    @hybrid_property
    def work_id(self):
        return self.entity1_id


class LinkReleaseGroupReleaseGroup(Base):
    __tablename__ = 'l_release_group_release_group'
    __table_args__ = (
        Index('l_release_group_release_group_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_release_group_release_group_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_release_group_release_group_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='l_release_group_release_group_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='l_release_group_release_group_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('ReleaseGroup', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('ReleaseGroup', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def release_group0(self):
        return self.entity0

    @hybrid_property
    def release_group0_id(self):
        return self.entity0_id

    @hybrid_property
    def release_group1(self):
        return self.entity1

    @hybrid_property
    def release_group1_id(self):
        return self.entity1_id


class LinkReleaseGroupSeries(Base):
    __tablename__ = 'l_release_group_series'
    __table_args__ = (
        Index('l_release_group_series_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_release_group_series_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_release_group_series_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='l_release_group_series_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='l_release_group_series_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('ReleaseGroup', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Series', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def release_group(self):
        return self.entity0

    @hybrid_property
    def release_group_id(self):
        return self.entity0_id

    @hybrid_property
    def series(self):
        return self.entity1

    @hybrid_property
    def series_id(self):
        return self.entity1_id


class LinkReleaseGroupURL(Base):
    __tablename__ = 'l_release_group_url'
    __table_args__ = (
        Index('l_release_group_url_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_release_group_url_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_release_group_url_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='l_release_group_url_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='l_release_group_url_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('ReleaseGroup', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('URL', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def release_group(self):
        return self.entity0

    @hybrid_property
    def release_group_id(self):
        return self.entity0_id

    @hybrid_property
    def url(self):
        return self.entity1

    @hybrid_property
    def url_id(self):
        return self.entity1_id


class LinkReleaseGroupWork(Base):
    __tablename__ = 'l_release_group_work'
    __table_args__ = (
        Index('l_release_group_work_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_release_group_work_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_release_group_work_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='l_release_group_work_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='l_release_group_work_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('ReleaseGroup', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Work', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def release_group(self):
        return self.entity0

    @hybrid_property
    def release_group_id(self):
        return self.entity0_id

    @hybrid_property
    def work(self):
        return self.entity1

    @hybrid_property
    def work_id(self):
        return self.entity1_id


class LinkSeriesSeries(Base):
    __tablename__ = 'l_series_series'
    __table_args__ = (
        Index('l_series_series_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_series_series_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_series_series_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='l_series_series_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='l_series_series_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Series', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Series', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def series0(self):
        return self.entity0

    @hybrid_property
    def series0_id(self):
        return self.entity0_id

    @hybrid_property
    def series1(self):
        return self.entity1

    @hybrid_property
    def series1_id(self):
        return self.entity1_id


class LinkSeriesURL(Base):
    __tablename__ = 'l_series_url'
    __table_args__ = (
        Index('l_series_url_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_series_url_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_series_url_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='l_series_url_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='l_series_url_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Series', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('URL', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def series(self):
        return self.entity0

    @hybrid_property
    def series_id(self):
        return self.entity0_id

    @hybrid_property
    def url(self):
        return self.entity1

    @hybrid_property
    def url_id(self):
        return self.entity1_id


class LinkSeriesWork(Base):
    __tablename__ = 'l_series_work'
    __table_args__ = (
        Index('l_series_work_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_series_work_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_series_work_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='l_series_work_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='l_series_work_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Series', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Work', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def series(self):
        return self.entity0

    @hybrid_property
    def series_id(self):
        return self.entity0_id

    @hybrid_property
    def work(self):
        return self.entity1

    @hybrid_property
    def work_id(self):
        return self.entity1_id


class LinkURLURL(Base):
    __tablename__ = 'l_url_url'
    __table_args__ = (
        Index('l_url_url_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_url_url_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_url_url_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='l_url_url_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='l_url_url_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('URL', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('URL', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def url0(self):
        return self.entity0

    @hybrid_property
    def url0_id(self):
        return self.entity0_id

    @hybrid_property
    def url1(self):
        return self.entity1

    @hybrid_property
    def url1_id(self):
        return self.entity1_id


class LinkURLWork(Base):
    __tablename__ = 'l_url_work'
    __table_args__ = (
        Index('l_url_work_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_url_work_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_url_work_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='l_url_work_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='l_url_work_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('URL', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Work', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def url(self):
        return self.entity0

    @hybrid_property
    def url_id(self):
        return self.entity0_id

    @hybrid_property
    def work(self):
        return self.entity1

    @hybrid_property
    def work_id(self):
        return self.entity1_id


class LinkWorkWork(Base):
    __tablename__ = 'l_work_work'
    __table_args__ = (
        Index('l_work_work_idx_uniq', 'entity0', 'entity1', 'link', 'link_order', unique=True),
        Index('l_work_work_idx_entity1', 'entity1'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='l_work_work_fk_link'), nullable=False)
    entity0_id = Column('entity0', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='l_work_work_fk_entity0'), nullable=False)
    entity1_id = Column('entity1', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='l_work_work_fk_entity1'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    link_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    entity0_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))
    entity1_credit = Column(String, nullable=False, default='', server_default=sql.text("''"))

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    entity0 = relationship('Work', foreign_keys=[entity0_id], innerjoin=True)
    entity1 = relationship('Work', foreign_keys=[entity1_id], innerjoin=True)

    @hybrid_property
    def work0(self):
        return self.entity0

    @hybrid_property
    def work0_id(self):
        return self.entity0_id

    @hybrid_property
    def work1(self):
        return self.entity1

    @hybrid_property
    def work1_id(self):
        return self.entity1_id


class Label(Base):
    __tablename__ = 'label'
    __table_args__ = (
        Index('label_idx_gid', 'gid', unique=True),
        Index('label_idx_name', 'name'),
        Index('label_idx_area', 'area'),
        Index('label_idx_null_comment', 'name', unique=True),
        Index('label_idx_uniq_name_comment', 'name', 'comment', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    label_code = Column(Integer)
    type_id = Column('type', Integer, ForeignKey(apply_schema('label_type.id', 'musicbrainz'), name='label_fk_type'))
    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='label_fk_area'))
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    type = relationship('LabelType', foreign_keys=[type_id])
    area = relationship('Area', foreign_keys=[area_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class LabelRatingRaw(Base):
    __tablename__ = 'label_rating_raw'
    __table_args__ = (
        Index('label_rating_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    label_id = Column('label', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='label_rating_raw_fk_label'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='label_rating_raw_fk_editor'), nullable=False, primary_key=True)
    rating = Column(SMALLINT, nullable=False)

    label = relationship('Label', foreign_keys=[label_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)


class LabelTagRaw(Base):
    __tablename__ = 'label_tag_raw'
    __table_args__ = (
        Index('label_tag_raw_idx_tag', 'tag'),
        Index('label_tag_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    label_id = Column('label', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='label_tag_raw_fk_label'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='label_tag_raw_fk_editor'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='label_tag_raw_fk_tag'), nullable=False, primary_key=True)
    is_upvote = Column(Boolean, nullable=False, default=True, server_default=sql.true())

    label = relationship('Label', foreign_keys=[label_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class LabelAliasType(Base):
    __tablename__ = 'label_alias_type'
    __table_args__ = (
        Index('label_alias_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('label_alias_type.id', 'musicbrainz'), name='label_alias_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('LabelAliasType', foreign_keys=[parent_id])


class LabelAlias(Base):
    __tablename__ = 'label_alias'
    __table_args__ = (
        Index('label_alias_idx_label', 'label'),
        Index('label_alias_idx_primary', 'label', 'locale', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    label_id = Column('label', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='label_alias_fk_label'), nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    type_id = Column('type', Integer, ForeignKey(apply_schema('label_alias_type.id', 'musicbrainz'), name='label_alias_fk_type'))
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    primary_for_locale = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    label = relationship('Label', foreign_keys=[label_id], innerjoin=True)
    type = relationship('LabelAliasType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class LabelAnnotation(Base):
    __tablename__ = 'label_annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    label_id = Column('label', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='label_annotation_fk_label'), nullable=False, primary_key=True)
    annotation_id = Column('annotation', Integer, ForeignKey(apply_schema('annotation.id', 'musicbrainz'), name='label_annotation_fk_annotation'), nullable=False, primary_key=True)

    label = relationship('Label', foreign_keys=[label_id], innerjoin=True)
    annotation = relationship('Annotation', foreign_keys=[annotation_id], innerjoin=True)


class LabelAttributeType(Base):
    __tablename__ = 'label_attribute_type'
    __table_args__ = (
        Index('label_attribute_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    free_text = Column(Boolean, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('label_attribute_type.id', 'musicbrainz'), name='label_attribute_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('LabelAttributeType', foreign_keys=[parent_id])


class LabelAttributeTypeAllowedValue(Base):
    __tablename__ = 'label_attribute_type_allowed_value'
    __table_args__ = (
        Index('label_attribute_type_allowed_value_idx_name', 'label_attribute_type'),
        Index('label_attribute_type_allowed_value_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    label_attribute_type_id = Column('label_attribute_type', Integer, ForeignKey(apply_schema('label_attribute_type.id', 'musicbrainz'), name='label_attribute_type_allowed_value_fk_label_attribute_type'), nullable=False)
    value = Column(String)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('label_attribute_type_allowed_value.id', 'musicbrainz'), name='label_attribute_type_allowed_value_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    label_attribute_type = relationship('LabelAttributeType', foreign_keys=[label_attribute_type_id], innerjoin=True)
    parent = relationship('LabelAttributeTypeAllowedValue', foreign_keys=[parent_id])


class LabelAttribute(Base):
    __tablename__ = 'label_attribute'
    __table_args__ = (
        Index('label_attribute_idx_label', 'label'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    label_id = Column('label', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='label_attribute_fk_label'), nullable=False)
    label_attribute_type_id = Column('label_attribute_type', Integer, ForeignKey(apply_schema('label_attribute_type.id', 'musicbrainz'), name='label_attribute_fk_label_attribute_type'), nullable=False)
    label_attribute_type_allowed_value_id = Column('label_attribute_type_allowed_value', Integer, ForeignKey(apply_schema('label_attribute_type_allowed_value.id', 'musicbrainz'), name='label_attribute_fk_label_attribute_type_allowed_value'))
    label_attribute_text = Column(String)

    label = relationship('Label', foreign_keys=[label_id], innerjoin=True)
    label_attribute_type = relationship('LabelAttributeType', foreign_keys=[label_attribute_type_id], innerjoin=True)
    label_attribute_type_allowed_value = relationship('LabelAttributeTypeAllowedValue', foreign_keys=[label_attribute_type_allowed_value_id])


class LabelIPI(Base):
    __tablename__ = 'label_ipi'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    label_id = Column('label', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='label_ipi_fk_label'), nullable=False, primary_key=True)
    ipi = Column(CHAR(11), nullable=False, primary_key=True)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    label = relationship('Label', foreign_keys=[label_id], innerjoin=True, backref=backref('ipis'))


class LabelISNI(Base):
    __tablename__ = 'label_isni'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    label_id = Column('label', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='label_isni_fk_label'), nullable=False, primary_key=True)
    isni = Column(CHAR(16), nullable=False, primary_key=True)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    label = relationship('Label', foreign_keys=[label_id], innerjoin=True, backref=backref('isnis'))


class LabelMeta(Base):
    __tablename__ = 'label_meta'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='label_meta_fk_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    rating = Column(SMALLINT)
    rating_count = Column(Integer)

    label = relationship('Label', foreign_keys=[id], innerjoin=True, backref=backref('meta', uselist=False))


class LabelGIDRedirect(Base):
    __tablename__ = 'label_gid_redirect'
    __table_args__ = (
        Index('label_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='label_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('Label', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def label(self):
        return self.redirect


class LabelTag(Base):
    __tablename__ = 'label_tag'
    __table_args__ = (
        Index('label_tag_idx_tag', 'tag'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    label_id = Column('label', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='label_tag_fk_label'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='label_tag_fk_tag'), nullable=False, primary_key=True)
    count = Column(Integer, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    label = relationship('Label', foreign_keys=[label_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class LabelType(Base):
    __tablename__ = 'label_type'
    __table_args__ = (
        Index('label_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('label_type.id', 'musicbrainz'), name='label_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('LabelType', foreign_keys=[parent_id])


class Language(Base):
    __tablename__ = 'language'
    __table_args__ = (
        Index('language_idx_iso_code_2b', 'iso_code_2b', unique=True),
        Index('language_idx_iso_code_2t', 'iso_code_2t', unique=True),
        Index('language_idx_iso_code_1', 'iso_code_1', unique=True),
        Index('language_idx_iso_code_3', 'iso_code_3', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    iso_code_2t = Column(CHAR(3))
    iso_code_2b = Column(CHAR(3))
    iso_code_1 = Column(CHAR(2))
    name = Column(String(100), nullable=False)
    frequency = Column(SMALLINT, nullable=False, default=0, server_default=sql.text('0'))
    iso_code_3 = Column(CHAR(3))


class Link(Base):
    __tablename__ = 'link'
    __table_args__ = (
        Index('link_idx_type_attr', 'link_type', 'attribute_count'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    link_type_id = Column('link_type', Integer, ForeignKey(apply_schema('link_type.id', 'musicbrainz'), name='link_fk_link_type'), nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    attribute_count = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    created = Column(DateTime(timezone=True), server_default=sql.func.now())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    link_type = relationship('LinkType', foreign_keys=[link_type_id], innerjoin=True)

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class LinkAttribute(Base):
    __tablename__ = 'link_attribute'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='link_attribute_fk_link'), nullable=False, primary_key=True)
    attribute_type_id = Column('attribute_type', Integer, ForeignKey(apply_schema('link_attribute_type.id', 'musicbrainz'), name='link_attribute_fk_attribute_type'), nullable=False, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)
    attribute_type = relationship('LinkAttributeType', foreign_keys=[attribute_type_id], innerjoin=True)


class LinkAttributeType(Base):
    __tablename__ = 'link_attribute_type'
    __table_args__ = (
        Index('link_attribute_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('link_attribute_type.id', 'musicbrainz'), name='link_attribute_type_fk_parent'))
    root_id = Column('root', Integer, ForeignKey(apply_schema('link_attribute_type.id', 'musicbrainz'), name='link_attribute_type_fk_root'), nullable=False)
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    gid = Column(UUID, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    parent = relationship('LinkAttributeType', foreign_keys=[parent_id])
    root = relationship('LinkAttributeType', foreign_keys=[root_id], innerjoin=True)


class LinkCreditableAttributeType(Base):
    __tablename__ = 'link_creditable_attribute_type'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    attribute_type_id = Column('attribute_type', Integer, ForeignKey(apply_schema('link_attribute_type.id', 'musicbrainz'), name='link_creditable_attribute_type_fk_attribute_type', ondelete='CASCADE'), nullable=False, primary_key=True)

    attribute_type = relationship('LinkAttributeType', foreign_keys=[attribute_type_id], innerjoin=True)


class LinkAttributeCredit(Base):
    __tablename__ = 'link_attribute_credit'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='link_attribute_credit_fk_link'), nullable=False, primary_key=True)
    attribute_type = Column(Integer, ForeignKey(apply_schema('link_creditable_attribute_type.attribute_type', 'musicbrainz'), name='link_attribute_credit_fk_attribute_type'), nullable=False, primary_key=True)
    credited_as = Column(String, nullable=False)

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)


class LinkTextAttributeType(Base):
    __tablename__ = 'link_text_attribute_type'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    attribute_type_id = Column('attribute_type', Integer, ForeignKey(apply_schema('link_attribute_type.id', 'musicbrainz'), name='link_text_attribute_type_fk_attribute_type', ondelete='CASCADE'), nullable=False, primary_key=True)

    attribute_type = relationship('LinkAttributeType', foreign_keys=[attribute_type_id], innerjoin=True)


class LinkAttributeTextValue(Base):
    __tablename__ = 'link_attribute_text_value'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    link_id = Column('link', Integer, ForeignKey(apply_schema('link.id', 'musicbrainz'), name='link_attribute_text_value_fk_link'), nullable=False, primary_key=True)
    attribute_type = Column(Integer, ForeignKey(apply_schema('link_text_attribute_type.attribute_type', 'musicbrainz'), name='link_attribute_text_value_fk_attribute_type'), nullable=False, primary_key=True)
    text_value = Column(String, nullable=False)

    link = relationship('Link', foreign_keys=[link_id], innerjoin=True)


class LinkType(Base):
    __tablename__ = 'link_type'
    __table_args__ = (
        Index('link_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('link_type.id', 'musicbrainz'), name='link_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    gid = Column(UUID, nullable=False)
    entity_type0 = Column(String(50), nullable=False)
    entity_type1 = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String)
    link_phrase = Column(String(255), nullable=False)
    reverse_link_phrase = Column(String(255), nullable=False)
    long_link_phrase = Column(String(255), nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    is_deprecated = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    has_dates = Column(Boolean, nullable=False, default=True, server_default=sql.true())
    entity0_cardinality = Column(SMALLINT, nullable=False, default=0, server_default=sql.text('0'))
    entity1_cardinality = Column(SMALLINT, nullable=False, default=0, server_default=sql.text('0'))

    parent = relationship('LinkType', foreign_keys=[parent_id])


class LinkTypeAttributeType(Base):
    __tablename__ = 'link_type_attribute_type'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    link_type_id = Column('link_type', Integer, ForeignKey(apply_schema('link_type.id', 'musicbrainz'), name='link_type_attribute_type_fk_link_type'), nullable=False, primary_key=True)
    attribute_type_id = Column('attribute_type', Integer, ForeignKey(apply_schema('link_attribute_type.id', 'musicbrainz'), name='link_type_attribute_type_fk_attribute_type'), nullable=False, primary_key=True)
    min = Column(SMALLINT)
    max = Column(SMALLINT)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    link_type = relationship('LinkType', foreign_keys=[link_type_id], innerjoin=True)
    attribute_type = relationship('LinkAttributeType', foreign_keys=[attribute_type_id], innerjoin=True)


class EditorCollection(Base):
    __tablename__ = 'editor_collection'
    __table_args__ = (
        Index('editor_collection_idx_gid', 'gid', unique=True),
        Index('editor_collection_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='editor_collection_fk_editor'), nullable=False)
    name = Column(String, nullable=False)
    public = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    description = Column(String, nullable=False, default='', server_default=sql.text("''"))
    type_id = Column('type', Integer, ForeignKey(apply_schema('editor_collection_type.id', 'musicbrainz'), name='editor_collection_fk_type'), nullable=False)

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    type = relationship('EditorCollectionType', foreign_keys=[type_id], innerjoin=True)


class EditorCollectionGIDRedirect(Base):
    __tablename__ = 'editor_collection_gid_redirect'
    __table_args__ = (
        Index('editor_collection_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('editor_collection.id', 'musicbrainz'), name='editor_collection_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('EditorCollection', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def editor_collection(self):
        return self.redirect


class EditorCollectionType(Base):
    __tablename__ = 'editor_collection_type'
    __table_args__ = (
        Index('editor_collection_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    entity_type = Column(String(50), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('editor_collection_type.id', 'musicbrainz'), name='editor_collection_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('EditorCollectionType', foreign_keys=[parent_id])


class EditorCollectionCollaborator(Base):
    __tablename__ = 'editor_collection_collaborator'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    collection_id = Column('collection', Integer, ForeignKey(apply_schema('editor_collection.id', 'musicbrainz'), name='editor_collection_collaborator_fk_collection'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='editor_collection_collaborator_fk_editor'), nullable=False, primary_key=True)

    collection = relationship('EditorCollection', foreign_keys=[collection_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)


class EditorCollectionArea(Base):
    __tablename__ = 'editor_collection_area'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    collection_id = Column('collection', Integer, ForeignKey(apply_schema('editor_collection.id', 'musicbrainz'), name='editor_collection_area_fk_collection'), nullable=False, primary_key=True)
    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='editor_collection_area_fk_area'), nullable=False, primary_key=True)
    added = Column(DateTime(timezone=True), server_default=sql.func.now())
    position = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    comment = Column(String, nullable=False, default='', server_default=sql.text("''"))

    collection = relationship('EditorCollection', foreign_keys=[collection_id], innerjoin=True)
    area = relationship('Area', foreign_keys=[area_id], innerjoin=True)


class EditorCollectionArtist(Base):
    __tablename__ = 'editor_collection_artist'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    collection_id = Column('collection', Integer, ForeignKey(apply_schema('editor_collection.id', 'musicbrainz'), name='editor_collection_artist_fk_collection'), nullable=False, primary_key=True)
    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='editor_collection_artist_fk_artist'), nullable=False, primary_key=True)
    added = Column(DateTime(timezone=True), server_default=sql.func.now())
    position = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    comment = Column(String, nullable=False, default='', server_default=sql.text("''"))

    collection = relationship('EditorCollection', foreign_keys=[collection_id], innerjoin=True)
    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)


class EditorCollectionEvent(Base):
    __tablename__ = 'editor_collection_event'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    collection_id = Column('collection', Integer, ForeignKey(apply_schema('editor_collection.id', 'musicbrainz'), name='editor_collection_event_fk_collection'), nullable=False, primary_key=True)
    event_id = Column('event', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='editor_collection_event_fk_event'), nullable=False, primary_key=True)
    added = Column(DateTime(timezone=True), server_default=sql.func.now())
    position = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    comment = Column(String, nullable=False, default='', server_default=sql.text("''"))

    collection = relationship('EditorCollection', foreign_keys=[collection_id], innerjoin=True)
    event = relationship('Event', foreign_keys=[event_id], innerjoin=True)


class EditorCollectionGenre(Base):
    __tablename__ = 'editor_collection_genre'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    collection_id = Column('collection', Integer, ForeignKey(apply_schema('editor_collection.id', 'musicbrainz'), name='editor_collection_genre_fk_collection'), nullable=False, primary_key=True)
    genre_id = Column('genre', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='editor_collection_genre_fk_genre'), nullable=False, primary_key=True)
    added = Column(DateTime(timezone=True), server_default=sql.func.now())
    position = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    comment = Column(String, nullable=False, default='', server_default=sql.text("''"))

    collection = relationship('EditorCollection', foreign_keys=[collection_id], innerjoin=True)
    genre = relationship('Genre', foreign_keys=[genre_id], innerjoin=True)


class EditorCollectionInstrument(Base):
    __tablename__ = 'editor_collection_instrument'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    collection_id = Column('collection', Integer, ForeignKey(apply_schema('editor_collection.id', 'musicbrainz'), name='editor_collection_instrument_fk_collection'), nullable=False, primary_key=True)
    instrument_id = Column('instrument', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='editor_collection_instrument_fk_instrument'), nullable=False, primary_key=True)
    added = Column(DateTime(timezone=True), server_default=sql.func.now())
    position = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    comment = Column(String, nullable=False, default='', server_default=sql.text("''"))

    collection = relationship('EditorCollection', foreign_keys=[collection_id], innerjoin=True)
    instrument = relationship('Instrument', foreign_keys=[instrument_id], innerjoin=True)


class EditorCollectionLabel(Base):
    __tablename__ = 'editor_collection_label'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    collection_id = Column('collection', Integer, ForeignKey(apply_schema('editor_collection.id', 'musicbrainz'), name='editor_collection_label_fk_collection'), nullable=False, primary_key=True)
    label_id = Column('label', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='editor_collection_label_fk_label'), nullable=False, primary_key=True)
    added = Column(DateTime(timezone=True), server_default=sql.func.now())
    position = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    comment = Column(String, nullable=False, default='', server_default=sql.text("''"))

    collection = relationship('EditorCollection', foreign_keys=[collection_id], innerjoin=True)
    label = relationship('Label', foreign_keys=[label_id], innerjoin=True)


class EditorCollectionPlace(Base):
    __tablename__ = 'editor_collection_place'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    collection_id = Column('collection', Integer, ForeignKey(apply_schema('editor_collection.id', 'musicbrainz'), name='editor_collection_place_fk_collection'), nullable=False, primary_key=True)
    place_id = Column('place', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='editor_collection_place_fk_place'), nullable=False, primary_key=True)
    added = Column(DateTime(timezone=True), server_default=sql.func.now())
    position = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    comment = Column(String, nullable=False, default='', server_default=sql.text("''"))

    collection = relationship('EditorCollection', foreign_keys=[collection_id], innerjoin=True)
    place = relationship('Place', foreign_keys=[place_id], innerjoin=True)


class EditorCollectionRecording(Base):
    __tablename__ = 'editor_collection_recording'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    collection_id = Column('collection', Integer, ForeignKey(apply_schema('editor_collection.id', 'musicbrainz'), name='editor_collection_recording_fk_collection'), nullable=False, primary_key=True)
    recording_id = Column('recording', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='editor_collection_recording_fk_recording'), nullable=False, primary_key=True)
    added = Column(DateTime(timezone=True), server_default=sql.func.now())
    position = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    comment = Column(String, nullable=False, default='', server_default=sql.text("''"))

    collection = relationship('EditorCollection', foreign_keys=[collection_id], innerjoin=True)
    recording = relationship('Recording', foreign_keys=[recording_id], innerjoin=True)


class EditorCollectionRelease(Base):
    __tablename__ = 'editor_collection_release'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    collection_id = Column('collection', Integer, ForeignKey(apply_schema('editor_collection.id', 'musicbrainz'), name='editor_collection_release_fk_collection'), nullable=False, primary_key=True)
    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='editor_collection_release_fk_release'), nullable=False, primary_key=True)
    added = Column(DateTime(timezone=True), server_default=sql.func.now())
    position = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    comment = Column(String, nullable=False, default='', server_default=sql.text("''"))

    collection = relationship('EditorCollection', foreign_keys=[collection_id], innerjoin=True)
    release = relationship('Release', foreign_keys=[release_id], innerjoin=True)


class EditorCollectionReleaseGroup(Base):
    __tablename__ = 'editor_collection_release_group'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    collection_id = Column('collection', Integer, ForeignKey(apply_schema('editor_collection.id', 'musicbrainz'), name='editor_collection_release_group_fk_collection'), nullable=False, primary_key=True)
    release_group_id = Column('release_group', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='editor_collection_release_group_fk_release_group'), nullable=False, primary_key=True)
    added = Column(DateTime(timezone=True), server_default=sql.func.now())
    position = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    comment = Column(String, nullable=False, default='', server_default=sql.text("''"))

    collection = relationship('EditorCollection', foreign_keys=[collection_id], innerjoin=True)
    release_group = relationship('ReleaseGroup', foreign_keys=[release_group_id], innerjoin=True)


class EditorCollectionSeries(Base):
    __tablename__ = 'editor_collection_series'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    collection_id = Column('collection', Integer, ForeignKey(apply_schema('editor_collection.id', 'musicbrainz'), name='editor_collection_series_fk_collection'), nullable=False, primary_key=True)
    series_id = Column('series', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='editor_collection_series_fk_series'), nullable=False, primary_key=True)
    added = Column(DateTime(timezone=True), server_default=sql.func.now())
    position = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    comment = Column(String, nullable=False, default='', server_default=sql.text("''"))

    collection = relationship('EditorCollection', foreign_keys=[collection_id], innerjoin=True)
    series = relationship('Series', foreign_keys=[series_id], innerjoin=True)


class EditorCollectionWork(Base):
    __tablename__ = 'editor_collection_work'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    collection_id = Column('collection', Integer, ForeignKey(apply_schema('editor_collection.id', 'musicbrainz'), name='editor_collection_work_fk_collection'), nullable=False, primary_key=True)
    work_id = Column('work', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='editor_collection_work_fk_work'), nullable=False, primary_key=True)
    added = Column(DateTime(timezone=True), server_default=sql.func.now())
    position = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    comment = Column(String, nullable=False, default='', server_default=sql.text("''"))

    collection = relationship('EditorCollection', foreign_keys=[collection_id], innerjoin=True)
    work = relationship('Work', foreign_keys=[work_id], innerjoin=True)


class EditorCollectionDeletedEntity(Base):
    __tablename__ = 'editor_collection_deleted_entity'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    collection_id = Column('collection', Integer, ForeignKey(apply_schema('editor_collection.id', 'musicbrainz'), name='editor_collection_deleted_entity_fk_collection'), nullable=False, primary_key=True)
    gid = Column(UUID, ForeignKey(apply_schema('deleted_entity.gid', 'musicbrainz'), name='editor_collection_deleted_entity_fk_gid'), nullable=False, primary_key=True)
    added = Column(DateTime(timezone=True), server_default=sql.func.now())
    position = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    comment = Column(String, nullable=False, default='', server_default=sql.text("''"))

    collection = relationship('EditorCollection', foreign_keys=[collection_id], innerjoin=True)


class EditorOauthToken(Base):
    __tablename__ = 'editor_oauth_token'
    __table_args__ = (
        Index('editor_oauth_token_idx_editor', 'editor'),
        Index('editor_oauth_token_idx_access_token', 'access_token', unique=True),
        Index('editor_oauth_token_idx_refresh_token', 'refresh_token', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='editor_oauth_token_fk_editor'), nullable=False)
    application_id = Column('application', Integer, ForeignKey(apply_schema('application.id', 'musicbrainz'), name='editor_oauth_token_fk_application'), nullable=False)
    authorization_code = Column(String)
    refresh_token = Column(String)
    access_token = Column(String)
    expire_time = Column(DateTime(timezone=True), nullable=False)
    scope = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    granted = Column(DateTime(timezone=True), nullable=False, server_default=sql.func.now())
    code_challenge = Column(String)
    code_challenge_method = Column(Enum('plain', 'S256', name='OAUTH_CODE_CHALLENGE_METHOD', schema=mbdata.config.schemas.get('musicbrainz', 'musicbrainz')))

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    application = relationship('Application', foreign_keys=[application_id], innerjoin=True)


class Medium(Base):
    __tablename__ = 'medium'
    __table_args__ = (
        Index('medium_idx_gid', 'gid', unique=True),
        Index('medium_idx_track_count', 'track_count'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='medium_fk_release'), nullable=False)
    position = Column(Integer, nullable=False)
    format_id = Column('format', Integer, ForeignKey(apply_schema('medium_format.id', 'musicbrainz'), name='medium_fk_format'))
    name = Column(String, nullable=False, default='', server_default=sql.text("''"))
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    track_count = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    gid = Column(UUID, nullable=False)

    release = relationship('Release', foreign_keys=[release_id], innerjoin=True, backref=backref('mediums', order_by="Medium.position"))
    format = relationship('MediumFormat', foreign_keys=[format_id])


class MediumAttributeType(Base):
    __tablename__ = 'medium_attribute_type'
    __table_args__ = (
        Index('medium_attribute_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    free_text = Column(Boolean, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('medium_attribute_type.id', 'musicbrainz'), name='medium_attribute_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('MediumAttributeType', foreign_keys=[parent_id])


class MediumAttributeTypeAllowedFormat(Base):
    __tablename__ = 'medium_attribute_type_allowed_format'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    medium_format_id = Column('medium_format', Integer, ForeignKey(apply_schema('medium_format.id', 'musicbrainz'), name='medium_attribute_type_allowed_format_fk_medium_format'), nullable=False, primary_key=True)
    medium_attribute_type_id = Column('medium_attribute_type', Integer, ForeignKey(apply_schema('medium_attribute_type.id', 'musicbrainz'), name='medium_attribute_type_allowed_format_fk_medium_attribute_type'), nullable=False, primary_key=True)

    medium_format = relationship('MediumFormat', foreign_keys=[medium_format_id], innerjoin=True)
    medium_attribute_type = relationship('MediumAttributeType', foreign_keys=[medium_attribute_type_id], innerjoin=True)


class MediumAttributeTypeAllowedValue(Base):
    __tablename__ = 'medium_attribute_type_allowed_value'
    __table_args__ = (
        Index('medium_attribute_type_allowed_value_idx_name', 'medium_attribute_type'),
        Index('medium_attribute_type_allowed_value_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    medium_attribute_type_id = Column('medium_attribute_type', Integer, ForeignKey(apply_schema('medium_attribute_type.id', 'musicbrainz'), name='medium_attribute_type_allowed_value_fk_medium_attribute_type'), nullable=False)
    value = Column(String)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('medium_attribute_type_allowed_value.id', 'musicbrainz'), name='medium_attribute_type_allowed_value_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    medium_attribute_type = relationship('MediumAttributeType', foreign_keys=[medium_attribute_type_id], innerjoin=True)
    parent = relationship('MediumAttributeTypeAllowedValue', foreign_keys=[parent_id])


class MediumAttributeTypeAllowedValueAllowedFormat(Base):
    __tablename__ = 'medium_attribute_type_allowed_value_allowed_format'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    medium_format_id = Column('medium_format', Integer, ForeignKey(apply_schema('medium_format.id', 'musicbrainz'), name='medium_attribute_type_allowed_value_allowed_format_fk_medium_fo'), nullable=False, primary_key=True)
    medium_attribute_type_allowed_value_id = Column('medium_attribute_type_allowed_value', Integer, ForeignKey(apply_schema('medium_attribute_type_allowed_value.id', 'musicbrainz'), name='medium_attribute_type_allowed_value_allowed_format_fk_medium_at'), nullable=False, primary_key=True)

    medium_format = relationship('MediumFormat', foreign_keys=[medium_format_id], innerjoin=True)
    medium_attribute_type_allowed_value = relationship('MediumAttributeTypeAllowedValue', foreign_keys=[medium_attribute_type_allowed_value_id], innerjoin=True)


class MediumAttribute(Base):
    __tablename__ = 'medium_attribute'
    __table_args__ = (
        Index('medium_attribute_idx_medium', 'medium'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    medium_id = Column('medium', Integer, ForeignKey(apply_schema('medium.id', 'musicbrainz'), name='medium_attribute_fk_medium'), nullable=False)
    medium_attribute_type_id = Column('medium_attribute_type', Integer, ForeignKey(apply_schema('medium_attribute_type.id', 'musicbrainz'), name='medium_attribute_fk_medium_attribute_type'), nullable=False)
    medium_attribute_type_allowed_value_id = Column('medium_attribute_type_allowed_value', Integer, ForeignKey(apply_schema('medium_attribute_type_allowed_value.id', 'musicbrainz'), name='medium_attribute_fk_medium_attribute_type_allowed_value'))
    medium_attribute_text = Column(String)

    medium = relationship('Medium', foreign_keys=[medium_id], innerjoin=True)
    medium_attribute_type = relationship('MediumAttributeType', foreign_keys=[medium_attribute_type_id], innerjoin=True)
    medium_attribute_type_allowed_value = relationship('MediumAttributeTypeAllowedValue', foreign_keys=[medium_attribute_type_allowed_value_id])


class MediumCDTOC(Base):
    __tablename__ = 'medium_cdtoc'
    __table_args__ = (
        Index('medium_cdtoc_idx_medium', 'medium'),
        Index('medium_cdtoc_idx_cdtoc', 'cdtoc'),
        Index('medium_cdtoc_idx_uniq', 'medium', 'cdtoc', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    medium_id = Column('medium', Integer, ForeignKey(apply_schema('medium.id', 'musicbrainz'), name='medium_cdtoc_fk_medium'), nullable=False)
    cdtoc_id = Column('cdtoc', Integer, ForeignKey(apply_schema('cdtoc.id', 'musicbrainz'), name='medium_cdtoc_fk_cdtoc'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    medium = relationship('Medium', foreign_keys=[medium_id], innerjoin=True)
    cdtoc = relationship('CDTOC', foreign_keys=[cdtoc_id], innerjoin=True)


class MediumFormat(Base):
    __tablename__ = 'medium_format'
    __table_args__ = (
        Index('medium_format_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('medium_format.id', 'musicbrainz'), name='medium_format_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    year = Column(SMALLINT)
    has_discids = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('MediumFormat', foreign_keys=[parent_id])


class MediumGIDRedirect(Base):
    __tablename__ = 'medium_gid_redirect'
    __table_args__ = (
        Index('medium_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('medium.id', 'musicbrainz'), name='medium_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('Medium', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def medium(self):
        return self.redirect


class Mood(Base):
    __tablename__ = 'mood'
    __table_args__ = (
        Index('mood_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())


class MoodAliasType(Base):
    __tablename__ = 'mood_alias_type'
    __table_args__ = (
        Index('mood_alias_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('mood_alias_type.id', 'musicbrainz'), name='mood_alias_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('MoodAliasType', foreign_keys=[parent_id])


class MoodAlias(Base):
    __tablename__ = 'mood_alias'
    __table_args__ = (
        Index('mood_alias_idx_mood', 'mood'),
        Index('mood_alias_idx_primary', 'mood', 'locale', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    mood_id = Column('mood', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='mood_alias_fk_mood'), nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    type_id = Column('type', Integer, ForeignKey(apply_schema('mood_alias_type.id', 'musicbrainz'), name='mood_alias_fk_type'))
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    primary_for_locale = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    mood = relationship('Mood', foreign_keys=[mood_id], innerjoin=True)
    type = relationship('MoodAliasType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class MoodAnnotation(Base):
    __tablename__ = 'mood_annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    mood_id = Column('mood', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='mood_annotation_fk_mood'), nullable=False, primary_key=True)
    annotation_id = Column('annotation', Integer, ForeignKey(apply_schema('annotation.id', 'musicbrainz'), name='mood_annotation_fk_annotation'), nullable=False, primary_key=True)

    mood = relationship('Mood', foreign_keys=[mood_id], innerjoin=True)
    annotation = relationship('Annotation', foreign_keys=[annotation_id], innerjoin=True)


class OrderableLinkType(Base):
    __tablename__ = 'orderable_link_type'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    link_type_id = Column('link_type', Integer, ForeignKey(apply_schema('link_type.id', 'musicbrainz'), name='orderable_link_type_fk_link_type'), nullable=False, primary_key=True)
    direction = Column(SMALLINT, nullable=False, default=1, server_default=sql.text('1'))

    link_type = relationship('LinkType', foreign_keys=[link_type_id], innerjoin=True)


class Place(Base):
    __tablename__ = 'place'
    __table_args__ = (
        Index('place_idx_gid', 'gid', unique=True),
        Index('place_idx_name', 'name'),
        Index('place_idx_area', 'area'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    type_id = Column('type', Integer, ForeignKey(apply_schema('place_type.id', 'musicbrainz'), name='place_fk_type'))
    address = Column(String, nullable=False, default='', server_default=sql.text("''"))
    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='place_fk_area'))
    coordinates = Column(Point)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    type = relationship('PlaceType', foreign_keys=[type_id])
    area = relationship('Area', foreign_keys=[area_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class PlaceAlias(Base):
    __tablename__ = 'place_alias'
    __table_args__ = (
        Index('place_alias_idx_place', 'place'),
        Index('place_alias_idx_primary', 'place', 'locale', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    place_id = Column('place', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='place_alias_fk_place'), nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    type_id = Column('type', Integer, ForeignKey(apply_schema('place_alias_type.id', 'musicbrainz'), name='place_alias_fk_type'))
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    primary_for_locale = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    place = relationship('Place', foreign_keys=[place_id], innerjoin=True)
    type = relationship('PlaceAliasType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class PlaceAliasType(Base):
    __tablename__ = 'place_alias_type'
    __table_args__ = (
        Index('place_alias_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('place_alias_type.id', 'musicbrainz'), name='place_alias_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('PlaceAliasType', foreign_keys=[parent_id])


class PlaceAnnotation(Base):
    __tablename__ = 'place_annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    place_id = Column('place', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='place_annotation_fk_place'), nullable=False, primary_key=True)
    annotation_id = Column('annotation', Integer, ForeignKey(apply_schema('annotation.id', 'musicbrainz'), name='place_annotation_fk_annotation'), nullable=False, primary_key=True)

    place = relationship('Place', foreign_keys=[place_id], innerjoin=True)
    annotation = relationship('Annotation', foreign_keys=[annotation_id], innerjoin=True)


class PlaceAttributeType(Base):
    __tablename__ = 'place_attribute_type'
    __table_args__ = (
        Index('place_attribute_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    free_text = Column(Boolean, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('place_attribute_type.id', 'musicbrainz'), name='place_attribute_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('PlaceAttributeType', foreign_keys=[parent_id])


class PlaceAttributeTypeAllowedValue(Base):
    __tablename__ = 'place_attribute_type_allowed_value'
    __table_args__ = (
        Index('place_attribute_type_allowed_value_idx_name', 'place_attribute_type'),
        Index('place_attribute_type_allowed_value_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    place_attribute_type_id = Column('place_attribute_type', Integer, ForeignKey(apply_schema('place_attribute_type.id', 'musicbrainz'), name='place_attribute_type_allowed_value_fk_place_attribute_type'), nullable=False)
    value = Column(String)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('place_attribute_type_allowed_value.id', 'musicbrainz'), name='place_attribute_type_allowed_value_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    place_attribute_type = relationship('PlaceAttributeType', foreign_keys=[place_attribute_type_id], innerjoin=True)
    parent = relationship('PlaceAttributeTypeAllowedValue', foreign_keys=[parent_id])


class PlaceAttribute(Base):
    __tablename__ = 'place_attribute'
    __table_args__ = (
        Index('place_attribute_idx_place', 'place'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    place_id = Column('place', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='place_attribute_fk_place'), nullable=False)
    place_attribute_type_id = Column('place_attribute_type', Integer, ForeignKey(apply_schema('place_attribute_type.id', 'musicbrainz'), name='place_attribute_fk_place_attribute_type'), nullable=False)
    place_attribute_type_allowed_value_id = Column('place_attribute_type_allowed_value', Integer, ForeignKey(apply_schema('place_attribute_type_allowed_value.id', 'musicbrainz'), name='place_attribute_fk_place_attribute_type_allowed_value'))
    place_attribute_text = Column(String)

    place = relationship('Place', foreign_keys=[place_id], innerjoin=True)
    place_attribute_type = relationship('PlaceAttributeType', foreign_keys=[place_attribute_type_id], innerjoin=True)
    place_attribute_type_allowed_value = relationship('PlaceAttributeTypeAllowedValue', foreign_keys=[place_attribute_type_allowed_value_id])


class PlaceGIDRedirect(Base):
    __tablename__ = 'place_gid_redirect'
    __table_args__ = (
        Index('place_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='place_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('Place', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def place(self):
        return self.redirect


class PlaceMeta(Base):
    __tablename__ = 'place_meta'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='place_meta_fk_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    rating = Column(SMALLINT)
    rating_count = Column(Integer)

    place = relationship('Place', foreign_keys=[id], innerjoin=True, backref=backref('meta', uselist=False))


class PlaceRatingRaw(Base):
    __tablename__ = 'place_rating_raw'
    __table_args__ = (
        Index('place_rating_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    place_id = Column('place', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='place_rating_raw_fk_place'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='place_rating_raw_fk_editor'), nullable=False, primary_key=True)
    rating = Column(SMALLINT, nullable=False)

    place = relationship('Place', foreign_keys=[place_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)


class PlaceTag(Base):
    __tablename__ = 'place_tag'
    __table_args__ = (
        Index('place_tag_idx_tag', 'tag'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    place_id = Column('place', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='place_tag_fk_place'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='place_tag_fk_tag'), nullable=False, primary_key=True)
    count = Column(Integer, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    place = relationship('Place', foreign_keys=[place_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class PlaceTagRaw(Base):
    __tablename__ = 'place_tag_raw'
    __table_args__ = (
        Index('place_tag_raw_idx_tag', 'tag'),
        Index('place_tag_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    place_id = Column('place', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='place_tag_raw_fk_place'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='place_tag_raw_fk_editor'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='place_tag_raw_fk_tag'), nullable=False, primary_key=True)
    is_upvote = Column(Boolean, nullable=False, default=True, server_default=sql.true())

    place = relationship('Place', foreign_keys=[place_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class PlaceType(Base):
    __tablename__ = 'place_type'
    __table_args__ = (
        Index('place_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('place_type.id', 'musicbrainz'), name='place_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('PlaceType', foreign_keys=[parent_id])


class ReplicationControl(Base):
    __tablename__ = 'replication_control'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    current_schema_sequence = Column(Integer, nullable=False)
    current_replication_sequence = Column(Integer)
    last_replication_date = Column(DateTime(timezone=True))


class Recording(Base):
    __tablename__ = 'recording'
    __table_args__ = (
        Index('recording_idx_gid', 'gid', unique=True),
        Index('recording_idx_name', 'name'),
        Index('recording_idx_artist_credit', 'artist_credit'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    artist_credit_id = Column('artist_credit', Integer, ForeignKey(apply_schema('artist_credit.id', 'musicbrainz'), name='recording_fk_artist_credit'), nullable=False)
    length = Column(Integer)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    video = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    artist_credit = relationship('ArtistCredit', foreign_keys=[artist_credit_id], innerjoin=True)


class RecordingAliasType(Base):
    __tablename__ = 'recording_alias_type'
    __table_args__ = (
        Index('recording_alias_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('recording_alias_type.id', 'musicbrainz'), name='recording_alias_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('RecordingAliasType', foreign_keys=[parent_id])


class RecordingAlias(Base):
    __tablename__ = 'recording_alias'
    __table_args__ = (
        Index('recording_alias_idx_recording', 'recording'),
        Index('recording_alias_idx_primary', 'recording', 'locale', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    recording_id = Column('recording', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='recording_alias_fk_recording'), nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    type_id = Column('type', Integer, ForeignKey(apply_schema('recording_alias_type.id', 'musicbrainz'), name='recording_alias_fk_type'))
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    primary_for_locale = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    recording = relationship('Recording', foreign_keys=[recording_id], innerjoin=True)
    type = relationship('RecordingAliasType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class RecordingRatingRaw(Base):
    __tablename__ = 'recording_rating_raw'
    __table_args__ = (
        Index('recording_rating_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    recording_id = Column('recording', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='recording_rating_raw_fk_recording'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='recording_rating_raw_fk_editor'), nullable=False, primary_key=True)
    rating = Column(SMALLINT, nullable=False)

    recording = relationship('Recording', foreign_keys=[recording_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)


class RecordingTagRaw(Base):
    __tablename__ = 'recording_tag_raw'
    __table_args__ = (
        Index('recording_tag_raw_idx_track', 'recording'),
        Index('recording_tag_raw_idx_tag', 'tag'),
        Index('recording_tag_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    recording_id = Column('recording', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='recording_tag_raw_fk_recording'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='recording_tag_raw_fk_editor'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='recording_tag_raw_fk_tag'), nullable=False, primary_key=True)
    is_upvote = Column(Boolean, nullable=False, default=True, server_default=sql.true())

    recording = relationship('Recording', foreign_keys=[recording_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class RecordingAnnotation(Base):
    __tablename__ = 'recording_annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    recording_id = Column('recording', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='recording_annotation_fk_recording'), nullable=False, primary_key=True)
    annotation_id = Column('annotation', Integer, ForeignKey(apply_schema('annotation.id', 'musicbrainz'), name='recording_annotation_fk_annotation'), nullable=False, primary_key=True)

    recording = relationship('Recording', foreign_keys=[recording_id], innerjoin=True)
    annotation = relationship('Annotation', foreign_keys=[annotation_id], innerjoin=True)


class RecordingAttributeType(Base):
    __tablename__ = 'recording_attribute_type'
    __table_args__ = (
        Index('recording_attribute_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    free_text = Column(Boolean, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('recording_attribute_type.id', 'musicbrainz'), name='recording_attribute_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('RecordingAttributeType', foreign_keys=[parent_id])


class RecordingAttributeTypeAllowedValue(Base):
    __tablename__ = 'recording_attribute_type_allowed_value'
    __table_args__ = (
        Index('recording_attribute_type_allowed_value_idx_name', 'recording_attribute_type'),
        Index('recording_attribute_type_allowed_value_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    recording_attribute_type_id = Column('recording_attribute_type', Integer, ForeignKey(apply_schema('recording_attribute_type.id', 'musicbrainz'), name='recording_attribute_type_allowed_value_fk_recording_attribute_t'), nullable=False)
    value = Column(String)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('recording_attribute_type_allowed_value.id', 'musicbrainz'), name='recording_attribute_type_allowed_value_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    recording_attribute_type = relationship('RecordingAttributeType', foreign_keys=[recording_attribute_type_id], innerjoin=True)
    parent = relationship('RecordingAttributeTypeAllowedValue', foreign_keys=[parent_id])


class RecordingAttribute(Base):
    __tablename__ = 'recording_attribute'
    __table_args__ = (
        Index('recording_attribute_idx_recording', 'recording'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    recording_id = Column('recording', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='recording_attribute_fk_recording'), nullable=False)
    recording_attribute_type_id = Column('recording_attribute_type', Integer, ForeignKey(apply_schema('recording_attribute_type.id', 'musicbrainz'), name='recording_attribute_fk_recording_attribute_type'), nullable=False)
    recording_attribute_type_allowed_value_id = Column('recording_attribute_type_allowed_value', Integer, ForeignKey(apply_schema('recording_attribute_type_allowed_value.id', 'musicbrainz'), name='recording_attribute_fk_recording_attribute_type_allowed_value'))
    recording_attribute_text = Column(String)

    recording = relationship('Recording', foreign_keys=[recording_id], innerjoin=True)
    recording_attribute_type = relationship('RecordingAttributeType', foreign_keys=[recording_attribute_type_id], innerjoin=True)
    recording_attribute_type_allowed_value = relationship('RecordingAttributeTypeAllowedValue', foreign_keys=[recording_attribute_type_allowed_value_id])


class RecordingMeta(Base):
    __tablename__ = 'recording_meta'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='recording_meta_fk_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    rating = Column(SMALLINT)
    rating_count = Column(Integer)

    recording = relationship('Recording', foreign_keys=[id], innerjoin=True, backref=backref('meta', uselist=False))


class RecordingGIDRedirect(Base):
    __tablename__ = 'recording_gid_redirect'
    __table_args__ = (
        Index('recording_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='recording_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('Recording', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def recording(self):
        return self.redirect


class RecordingTag(Base):
    __tablename__ = 'recording_tag'
    __table_args__ = (
        Index('recording_tag_idx_tag', 'tag'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    recording_id = Column('recording', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='recording_tag_fk_recording'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='recording_tag_fk_tag'), nullable=False, primary_key=True)
    count = Column(Integer, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    recording = relationship('Recording', foreign_keys=[recording_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class Release(Base):
    __tablename__ = 'release'
    __table_args__ = (
        Index('release_idx_gid', 'gid', unique=True),
        Index('release_idx_name', 'name'),
        Index('release_idx_release_group', 'release_group'),
        Index('release_idx_artist_credit', 'artist_credit'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    artist_credit_id = Column('artist_credit', Integer, ForeignKey(apply_schema('artist_credit.id', 'musicbrainz'), name='release_fk_artist_credit'), nullable=False)
    release_group_id = Column('release_group', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='release_fk_release_group'), nullable=False)
    status_id = Column('status', Integer, ForeignKey(apply_schema('release_status.id', 'musicbrainz'), name='release_fk_status'))
    packaging_id = Column('packaging', Integer, ForeignKey(apply_schema('release_packaging.id', 'musicbrainz'), name='release_fk_packaging'))
    language_id = Column('language', Integer, ForeignKey(apply_schema('language.id', 'musicbrainz'), name='release_fk_language'))
    script_id = Column('script', Integer, ForeignKey(apply_schema('script.id', 'musicbrainz'), name='release_fk_script'))
    barcode = Column(String(255))
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    quality = Column(SMALLINT, nullable=False, default=-1, server_default=sql.text('-1'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    artist_credit = relationship('ArtistCredit', foreign_keys=[artist_credit_id], innerjoin=True)
    release_group = relationship('ReleaseGroup', foreign_keys=[release_group_id], innerjoin=True)
    status = relationship('ReleaseStatus', foreign_keys=[status_id])
    packaging = relationship('ReleasePackaging', foreign_keys=[packaging_id])
    language = relationship('Language', foreign_keys=[language_id])
    script = relationship('Script', foreign_keys=[script_id])


class ReleaseAliasType(Base):
    __tablename__ = 'release_alias_type'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('release_alias_type.id', 'musicbrainz'), name='release_alias_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('ReleaseAliasType', foreign_keys=[parent_id])


class ReleaseAlias(Base):
    __tablename__ = 'release_alias'
    __table_args__ = (
        Index('release_alias_idx_release', 'release'),
        Index('release_alias_idx_primary', 'release', 'locale', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='release_alias_fk_release'), nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    type_id = Column('type', Integer, ForeignKey(apply_schema('release_alias_type.id', 'musicbrainz'), name='release_alias_fk_type'))
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    primary_for_locale = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    release = relationship('Release', foreign_keys=[release_id], innerjoin=True)
    type = relationship('ReleaseAliasType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class ReleaseCountry(Base):
    __tablename__ = 'release_country'
    __table_args__ = (
        Index('release_country_idx_country', 'country'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='release_country_fk_release'), nullable=False, primary_key=True)
    country_id = Column('country', Integer, ForeignKey(apply_schema('country_area.area', 'musicbrainz'), name='release_country_fk_country'), nullable=False, primary_key=True)
    date_year = Column(SMALLINT)
    date_month = Column(SMALLINT)
    date_day = Column(SMALLINT)

    release = relationship('Release', foreign_keys=[release_id], innerjoin=True, backref=backref('country_dates'))
    country = relationship('CountryArea', foreign_keys=[country_id], innerjoin=True)

    date = composite(PartialDate, date_year, date_month, date_day)


class ReleaseUnknownCountry(Base):
    __tablename__ = 'release_unknown_country'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='release_unknown_country_fk_release'), nullable=False, primary_key=True)
    date_year = Column(SMALLINT)
    date_month = Column(SMALLINT)
    date_day = Column(SMALLINT)

    release = relationship('Release', foreign_keys=[release_id], innerjoin=True, backref=backref('unknown_country_dates'))

    date = composite(PartialDate, date_year, date_month, date_day)


class ReleaseRaw(Base):
    __tablename__ = 'release_raw'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    artist = Column(String(255))
    added = Column(DateTime(timezone=True), server_default=sql.func.now())
    last_modified = Column(DateTime(timezone=True), server_default=sql.func.now())
    lookup_count = Column(Integer, default=0, server_default=sql.text('0'))
    modify_count = Column(Integer, default=0, server_default=sql.text('0'))
    source = Column(Integer, default=0, server_default=sql.text('0'))
    barcode = Column(String(255))
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))


class ReleaseTagRaw(Base):
    __tablename__ = 'release_tag_raw'
    __table_args__ = (
        Index('release_tag_raw_idx_tag', 'tag'),
        Index('release_tag_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='release_tag_raw_fk_release'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='release_tag_raw_fk_editor'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='release_tag_raw_fk_tag'), nullable=False, primary_key=True)
    is_upvote = Column(Boolean, nullable=False, default=True, server_default=sql.true())

    release = relationship('Release', foreign_keys=[release_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class ReleaseAnnotation(Base):
    __tablename__ = 'release_annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='release_annotation_fk_release'), nullable=False, primary_key=True)
    annotation_id = Column('annotation', Integer, ForeignKey(apply_schema('annotation.id', 'musicbrainz'), name='release_annotation_fk_annotation'), nullable=False, primary_key=True)

    release = relationship('Release', foreign_keys=[release_id], innerjoin=True)
    annotation = relationship('Annotation', foreign_keys=[annotation_id], innerjoin=True)


class ReleaseAttributeType(Base):
    __tablename__ = 'release_attribute_type'
    __table_args__ = (
        Index('release_attribute_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    free_text = Column(Boolean, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('release_attribute_type.id', 'musicbrainz'), name='release_attribute_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('ReleaseAttributeType', foreign_keys=[parent_id])


class ReleaseAttributeTypeAllowedValue(Base):
    __tablename__ = 'release_attribute_type_allowed_value'
    __table_args__ = (
        Index('release_attribute_type_allowed_value_idx_name', 'release_attribute_type'),
        Index('release_attribute_type_allowed_value_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    release_attribute_type_id = Column('release_attribute_type', Integer, ForeignKey(apply_schema('release_attribute_type.id', 'musicbrainz'), name='release_attribute_type_allowed_value_fk_release_attribute_type'), nullable=False)
    value = Column(String)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('release_attribute_type_allowed_value.id', 'musicbrainz'), name='release_attribute_type_allowed_value_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    release_attribute_type = relationship('ReleaseAttributeType', foreign_keys=[release_attribute_type_id], innerjoin=True)
    parent = relationship('ReleaseAttributeTypeAllowedValue', foreign_keys=[parent_id])


class ReleaseAttribute(Base):
    __tablename__ = 'release_attribute'
    __table_args__ = (
        Index('release_attribute_idx_release', 'release'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='release_attribute_fk_release'), nullable=False)
    release_attribute_type_id = Column('release_attribute_type', Integer, ForeignKey(apply_schema('release_attribute_type.id', 'musicbrainz'), name='release_attribute_fk_release_attribute_type'), nullable=False)
    release_attribute_type_allowed_value_id = Column('release_attribute_type_allowed_value', Integer, ForeignKey(apply_schema('release_attribute_type_allowed_value.id', 'musicbrainz'), name='release_attribute_fk_release_attribute_type_allowed_value'))
    release_attribute_text = Column(String)

    release = relationship('Release', foreign_keys=[release_id], innerjoin=True)
    release_attribute_type = relationship('ReleaseAttributeType', foreign_keys=[release_attribute_type_id], innerjoin=True)
    release_attribute_type_allowed_value = relationship('ReleaseAttributeTypeAllowedValue', foreign_keys=[release_attribute_type_allowed_value_id])


class ReleaseGIDRedirect(Base):
    __tablename__ = 'release_gid_redirect'
    __table_args__ = (
        Index('release_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='release_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('Release', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def release(self):
        return self.redirect


class ReleaseMeta(Base):
    __tablename__ = 'release_meta'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='release_meta_fk_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    date_added = Column(DateTime(timezone=True), server_default=sql.func.now())
    info_url = Column(String(255))
    amazon_asin = Column(String(10))
    cover_art_presence = Column(Enum('absent', 'present', 'darkened', name='COVER_ART_PRESENCE', schema=mbdata.config.schemas.get('musicbrainz', 'musicbrainz')), nullable=False, default='absent', server_default=sql.text("'absent'"))

    release = relationship('Release', foreign_keys=[id], innerjoin=True, backref=backref('meta', uselist=False))


class ReleaseLabel(Base):
    __tablename__ = 'release_label'
    __table_args__ = (
        Index('release_label_idx_release', 'release'),
        Index('release_label_idx_label', 'label'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='release_label_fk_release'), nullable=False)
    label_id = Column('label', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='release_label_fk_label'))
    catalog_number = Column(String(255))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    release = relationship('Release', foreign_keys=[release_id], innerjoin=True, backref=backref('labels'))
    label = relationship('Label', foreign_keys=[label_id])


class ReleasePackaging(Base):
    __tablename__ = 'release_packaging'
    __table_args__ = (
        Index('release_packaging_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('release_packaging.id', 'musicbrainz'), name='release_packaging_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('ReleasePackaging', foreign_keys=[parent_id])


class ReleaseStatus(Base):
    __tablename__ = 'release_status'
    __table_args__ = (
        Index('release_status_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('release_status.id', 'musicbrainz'), name='release_status_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('ReleaseStatus', foreign_keys=[parent_id])


class ReleaseTag(Base):
    __tablename__ = 'release_tag'
    __table_args__ = (
        Index('release_tag_idx_tag', 'tag'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='release_tag_fk_release'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='release_tag_fk_tag'), nullable=False, primary_key=True)
    count = Column(Integer, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    release = relationship('Release', foreign_keys=[release_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class ReleaseGroup(Base):
    __tablename__ = 'release_group'
    __table_args__ = (
        Index('release_group_idx_gid', 'gid', unique=True),
        Index('release_group_idx_name', 'name'),
        Index('release_group_idx_artist_credit', 'artist_credit'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    artist_credit_id = Column('artist_credit', Integer, ForeignKey(apply_schema('artist_credit.id', 'musicbrainz'), name='release_group_fk_artist_credit'), nullable=False)
    type_id = Column('type', Integer, ForeignKey(apply_schema('release_group_primary_type.id', 'musicbrainz'), name='release_group_fk_type'))
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    artist_credit = relationship('ArtistCredit', foreign_keys=[artist_credit_id], innerjoin=True)
    type = relationship('ReleaseGroupPrimaryType', foreign_keys=[type_id])


class ReleaseGroupAliasType(Base):
    __tablename__ = 'release_group_alias_type'
    __table_args__ = (
        Index('release_group_alias_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('release_group_alias_type.id', 'musicbrainz'), name='release_group_alias_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('ReleaseGroupAliasType', foreign_keys=[parent_id])


class ReleaseGroupAlias(Base):
    __tablename__ = 'release_group_alias'
    __table_args__ = (
        Index('release_group_alias_idx_release_group', 'release_group'),
        Index('release_group_alias_idx_primary', 'release_group', 'locale', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    release_group_id = Column('release_group', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='release_group_alias_fk_release_group'), nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    type_id = Column('type', Integer, ForeignKey(apply_schema('release_group_alias_type.id', 'musicbrainz'), name='release_group_alias_fk_type'))
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    primary_for_locale = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    release_group = relationship('ReleaseGroup', foreign_keys=[release_group_id], innerjoin=True)
    type = relationship('ReleaseGroupAliasType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class ReleaseGroupRatingRaw(Base):
    __tablename__ = 'release_group_rating_raw'
    __table_args__ = (
        Index('release_group_rating_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    release_group_id = Column('release_group', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='release_group_rating_raw_fk_release_group'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='release_group_rating_raw_fk_editor'), nullable=False, primary_key=True)
    rating = Column(SMALLINT, nullable=False)

    release_group = relationship('ReleaseGroup', foreign_keys=[release_group_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)


class ReleaseGroupTagRaw(Base):
    __tablename__ = 'release_group_tag_raw'
    __table_args__ = (
        Index('release_group_tag_raw_idx_tag', 'tag'),
        Index('release_group_tag_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    release_group_id = Column('release_group', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='release_group_tag_raw_fk_release_group'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='release_group_tag_raw_fk_editor'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='release_group_tag_raw_fk_tag'), nullable=False, primary_key=True)
    is_upvote = Column(Boolean, nullable=False, default=True, server_default=sql.true())

    release_group = relationship('ReleaseGroup', foreign_keys=[release_group_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class ReleaseGroupAnnotation(Base):
    __tablename__ = 'release_group_annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    release_group_id = Column('release_group', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='release_group_annotation_fk_release_group'), nullable=False, primary_key=True)
    annotation_id = Column('annotation', Integer, ForeignKey(apply_schema('annotation.id', 'musicbrainz'), name='release_group_annotation_fk_annotation'), nullable=False, primary_key=True)

    release_group = relationship('ReleaseGroup', foreign_keys=[release_group_id], innerjoin=True)
    annotation = relationship('Annotation', foreign_keys=[annotation_id], innerjoin=True)


class ReleaseGroupAttributeType(Base):
    __tablename__ = 'release_group_attribute_type'
    __table_args__ = (
        Index('release_group_attribute_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    free_text = Column(Boolean, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('release_group_attribute_type.id', 'musicbrainz'), name='release_group_attribute_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('ReleaseGroupAttributeType', foreign_keys=[parent_id])


class ReleaseGroupAttributeTypeAllowedValue(Base):
    __tablename__ = 'release_group_attribute_type_allowed_value'
    __table_args__ = (
        Index('release_group_attribute_type_allowed_value_idx_name', 'release_group_attribute_type'),
        Index('release_group_attribute_type_allowed_value_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    release_group_attribute_type_id = Column('release_group_attribute_type', Integer, ForeignKey(apply_schema('release_group_attribute_type.id', 'musicbrainz'), name='release_group_attribute_type_allowed_value_fk_release_group_att'), nullable=False)
    value = Column(String)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('release_group_attribute_type_allowed_value.id', 'musicbrainz'), name='release_group_attribute_type_allowed_value_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    release_group_attribute_type = relationship('ReleaseGroupAttributeType', foreign_keys=[release_group_attribute_type_id], innerjoin=True)
    parent = relationship('ReleaseGroupAttributeTypeAllowedValue', foreign_keys=[parent_id])


class ReleaseGroupAttribute(Base):
    __tablename__ = 'release_group_attribute'
    __table_args__ = (
        Index('release_group_attribute_idx_release_group', 'release_group'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    release_group_id = Column('release_group', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='release_group_attribute_fk_release_group'), nullable=False)
    release_group_attribute_type_id = Column('release_group_attribute_type', Integer, ForeignKey(apply_schema('release_group_attribute_type.id', 'musicbrainz'), name='release_group_attribute_fk_release_group_attribute_type'), nullable=False)
    release_group_attribute_type_allowed_value_id = Column('release_group_attribute_type_allowed_value', Integer, ForeignKey(apply_schema('release_group_attribute_type_allowed_value.id', 'musicbrainz'), name='release_group_attribute_fk_release_group_attribute_type_allowed'))
    release_group_attribute_text = Column(String)

    release_group = relationship('ReleaseGroup', foreign_keys=[release_group_id], innerjoin=True)
    release_group_attribute_type = relationship('ReleaseGroupAttributeType', foreign_keys=[release_group_attribute_type_id], innerjoin=True)
    release_group_attribute_type_allowed_value = relationship('ReleaseGroupAttributeTypeAllowedValue', foreign_keys=[release_group_attribute_type_allowed_value_id])


class ReleaseGroupGIDRedirect(Base):
    __tablename__ = 'release_group_gid_redirect'
    __table_args__ = (
        Index('release_group_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='release_group_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('ReleaseGroup', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def release_group(self):
        return self.redirect


class ReleaseGroupMeta(Base):
    __tablename__ = 'release_group_meta'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='release_group_meta_fk_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    release_count = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    first_release_date_year = Column(SMALLINT)
    first_release_date_month = Column(SMALLINT)
    first_release_date_day = Column(SMALLINT)
    rating = Column(SMALLINT)
    rating_count = Column(Integer)

    release_group = relationship('ReleaseGroup', foreign_keys=[id], innerjoin=True, backref=backref('meta', uselist=False))

    first_release_date = composite(PartialDate, first_release_date_year, first_release_date_month, first_release_date_day)


class ReleaseGroupTag(Base):
    __tablename__ = 'release_group_tag'
    __table_args__ = (
        Index('release_group_tag_idx_tag', 'tag'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    release_group_id = Column('release_group', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='release_group_tag_fk_release_group'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='release_group_tag_fk_tag'), nullable=False, primary_key=True)
    count = Column(Integer, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    release_group = relationship('ReleaseGroup', foreign_keys=[release_group_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class ReleaseGroupPrimaryType(Base):
    __tablename__ = 'release_group_primary_type'
    __table_args__ = (
        Index('release_group_primary_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('release_group_primary_type.id', 'musicbrainz'), name='release_group_primary_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('ReleaseGroupPrimaryType', foreign_keys=[parent_id])


class ReleaseGroupSecondaryType(Base):
    __tablename__ = 'release_group_secondary_type'
    __table_args__ = (
        Index('release_group_secondary_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('release_group_secondary_type.id', 'musicbrainz'), name='release_group_secondary_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('ReleaseGroupSecondaryType', foreign_keys=[parent_id])


class ReleaseGroupSecondaryTypeJoin(Base):
    __tablename__ = 'release_group_secondary_type_join'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    release_group_id = Column('release_group', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='release_group_secondary_type_join_fk_release_group'), nullable=False, primary_key=True)
    secondary_type_id = Column('secondary_type', Integer, ForeignKey(apply_schema('release_group_secondary_type.id', 'musicbrainz'), name='release_group_secondary_type_join_fk_secondary_type'), nullable=False, primary_key=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=sql.func.now())

    release_group = relationship('ReleaseGroup', foreign_keys=[release_group_id], innerjoin=True, backref=backref('secondary_types'))
    secondary_type = relationship('ReleaseGroupSecondaryType', foreign_keys=[secondary_type_id], innerjoin=True)


class Script(Base):
    __tablename__ = 'script'
    __table_args__ = (
        Index('script_idx_iso_code', 'iso_code', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    iso_code = Column(CHAR(4), nullable=False)
    iso_number = Column(CHAR(3), nullable=False)
    name = Column(String(100), nullable=False)
    frequency = Column(SMALLINT, nullable=False, default=0, server_default=sql.text('0'))


class Series(Base):
    __tablename__ = 'series'
    __table_args__ = (
        Index('series_idx_gid', 'gid', unique=True),
        Index('series_idx_name', 'name'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    type_id = Column('type', Integer, ForeignKey(apply_schema('series_type.id', 'musicbrainz'), name='series_fk_type'), nullable=False)
    ordering_type_id = Column('ordering_type', Integer, ForeignKey(apply_schema('series_ordering_type.id', 'musicbrainz'), name='series_fk_ordering_type'), nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    type = relationship('SeriesType', foreign_keys=[type_id], innerjoin=True)
    ordering_type = relationship('SeriesOrderingType', foreign_keys=[ordering_type_id], innerjoin=True)


class SeriesType(Base):
    __tablename__ = 'series_type'
    __table_args__ = (
        Index('series_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    entity_type = Column(String(50), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('series_type.id', 'musicbrainz'), name='series_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('SeriesType', foreign_keys=[parent_id])


class SeriesOrderingType(Base):
    __tablename__ = 'series_ordering_type'
    __table_args__ = (
        Index('series_ordering_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('series_ordering_type.id', 'musicbrainz'), name='series_ordering_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('SeriesOrderingType', foreign_keys=[parent_id])


class SeriesGIDRedirect(Base):
    __tablename__ = 'series_gid_redirect'
    __table_args__ = (
        Index('series_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='series_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('Series', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def series(self):
        return self.redirect


class SeriesAliasType(Base):
    __tablename__ = 'series_alias_type'
    __table_args__ = (
        Index('series_alias_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('series_alias_type.id', 'musicbrainz'), name='series_alias_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('SeriesAliasType', foreign_keys=[parent_id])


class SeriesAlias(Base):
    __tablename__ = 'series_alias'
    __table_args__ = (
        Index('series_alias_idx_series', 'series'),
        Index('series_alias_idx_primary', 'series', 'locale', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    series_id = Column('series', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='series_alias_fk_series'), nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    type_id = Column('type', Integer, ForeignKey(apply_schema('series_alias_type.id', 'musicbrainz'), name='series_alias_fk_type'))
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    primary_for_locale = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    series = relationship('Series', foreign_keys=[series_id], innerjoin=True)
    type = relationship('SeriesAliasType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class SeriesAnnotation(Base):
    __tablename__ = 'series_annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    series_id = Column('series', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='series_annotation_fk_series'), nullable=False, primary_key=True)
    annotation_id = Column('annotation', Integer, ForeignKey(apply_schema('annotation.id', 'musicbrainz'), name='series_annotation_fk_annotation'), nullable=False, primary_key=True)

    series = relationship('Series', foreign_keys=[series_id], innerjoin=True)
    annotation = relationship('Annotation', foreign_keys=[annotation_id], innerjoin=True)


class SeriesAttributeType(Base):
    __tablename__ = 'series_attribute_type'
    __table_args__ = (
        Index('series_attribute_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    free_text = Column(Boolean, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('series_attribute_type.id', 'musicbrainz'), name='series_attribute_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('SeriesAttributeType', foreign_keys=[parent_id])


class SeriesAttributeTypeAllowedValue(Base):
    __tablename__ = 'series_attribute_type_allowed_value'
    __table_args__ = (
        Index('series_attribute_type_allowed_value_idx_name', 'series_attribute_type'),
        Index('series_attribute_type_allowed_value_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    series_attribute_type_id = Column('series_attribute_type', Integer, ForeignKey(apply_schema('series_attribute_type.id', 'musicbrainz'), name='series_attribute_type_allowed_value_fk_series_attribute_type'), nullable=False)
    value = Column(String)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('series_attribute_type_allowed_value.id', 'musicbrainz'), name='series_attribute_type_allowed_value_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    series_attribute_type = relationship('SeriesAttributeType', foreign_keys=[series_attribute_type_id], innerjoin=True)
    parent = relationship('SeriesAttributeTypeAllowedValue', foreign_keys=[parent_id])


class SeriesAttribute(Base):
    __tablename__ = 'series_attribute'
    __table_args__ = (
        Index('series_attribute_idx_series', 'series'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    series_id = Column('series', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='series_attribute_fk_series'), nullable=False)
    series_attribute_type_id = Column('series_attribute_type', Integer, ForeignKey(apply_schema('series_attribute_type.id', 'musicbrainz'), name='series_attribute_fk_series_attribute_type'), nullable=False)
    series_attribute_type_allowed_value_id = Column('series_attribute_type_allowed_value', Integer, ForeignKey(apply_schema('series_attribute_type_allowed_value.id', 'musicbrainz'), name='series_attribute_fk_series_attribute_type_allowed_value'))
    series_attribute_text = Column(String)

    series = relationship('Series', foreign_keys=[series_id], innerjoin=True)
    series_attribute_type = relationship('SeriesAttributeType', foreign_keys=[series_attribute_type_id], innerjoin=True)
    series_attribute_type_allowed_value = relationship('SeriesAttributeTypeAllowedValue', foreign_keys=[series_attribute_type_allowed_value_id])


class SeriesTag(Base):
    __tablename__ = 'series_tag'
    __table_args__ = (
        Index('series_tag_idx_tag', 'tag'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    series_id = Column('series', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='series_tag_fk_series'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='series_tag_fk_tag'), nullable=False, primary_key=True)
    count = Column(Integer, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    series = relationship('Series', foreign_keys=[series_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class SeriesTagRaw(Base):
    __tablename__ = 'series_tag_raw'
    __table_args__ = (
        Index('series_tag_raw_idx_series', 'series'),
        Index('series_tag_raw_idx_tag', 'tag'),
        Index('series_tag_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    series_id = Column('series', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='series_tag_raw_fk_series'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='series_tag_raw_fk_editor'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='series_tag_raw_fk_tag'), nullable=False, primary_key=True)
    is_upvote = Column(Boolean, nullable=False, default=True, server_default=sql.true())

    series = relationship('Series', foreign_keys=[series_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class Tag(Base):
    __tablename__ = 'tag'
    __table_args__ = (
        Index('tag_idx_name', 'name', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    ref_count = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))


class TagRelation(Base):
    __tablename__ = 'tag_relation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    tag1_id = Column('tag1', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='tag_relation_fk_tag1'), nullable=False, primary_key=True)
    tag2_id = Column('tag2', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='tag_relation_fk_tag2'), nullable=False, primary_key=True)
    weight = Column(Integer, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    tag1 = relationship('Tag', foreign_keys=[tag1_id], innerjoin=True)
    tag2 = relationship('Tag', foreign_keys=[tag2_id], innerjoin=True)


class Track(Base):
    __tablename__ = 'track'
    __table_args__ = (
        Index('track_idx_gid', 'gid', unique=True),
        Index('track_idx_recording', 'recording'),
        Index('track_idx_artist_credit', 'artist_credit'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    recording_id = Column('recording', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='track_fk_recording'), nullable=False)
    medium_id = Column('medium', Integer, ForeignKey(apply_schema('medium.id', 'musicbrainz'), name='track_fk_medium'), nullable=False)
    position = Column(Integer, nullable=False)
    number = Column(String, nullable=False)
    name = Column(String, nullable=False)
    artist_credit_id = Column('artist_credit', Integer, ForeignKey(apply_schema('artist_credit.id', 'musicbrainz'), name='track_fk_artist_credit'), nullable=False)
    length = Column(Integer)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    is_data_track = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    recording = relationship('Recording', foreign_keys=[recording_id], innerjoin=True, backref=backref('tracks'))
    medium = relationship('Medium', foreign_keys=[medium_id], innerjoin=True, backref=backref('tracks', order_by="Track.position"))
    artist_credit = relationship('ArtistCredit', foreign_keys=[artist_credit_id], innerjoin=True)


class TrackGIDRedirect(Base):
    __tablename__ = 'track_gid_redirect'
    __table_args__ = (
        Index('track_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('track.id', 'musicbrainz'), name='track_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('Track', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def track(self):
        return self.redirect


class TrackRaw(Base):
    __tablename__ = 'track_raw'
    __table_args__ = (
        Index('track_raw_idx_release', 'release'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    release_id = Column('release', Integer, ForeignKey(apply_schema('release_raw.id', 'musicbrainz'), name='track_raw_fk_release'), nullable=False)
    title = Column(String(255), nullable=False)
    artist = Column(String(255))
    sequence = Column(Integer, nullable=False)

    release = relationship('ReleaseRaw', foreign_keys=[release_id], innerjoin=True)


class MediumIndex(Base):
    __tablename__ = 'medium_index'
    __table_args__ = (
        Index('medium_index_idx', 'toc'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    medium_id = Column('medium', Integer, ForeignKey(apply_schema('medium.id', 'musicbrainz'), name='medium_index_fk_medium', ondelete='CASCADE'), primary_key=True)
    toc = Column(Cube)

    medium = relationship('Medium', foreign_keys=[medium_id])


class UnreferencedRowLog(Base):
    __tablename__ = 'unreferenced_row_log'
    __table_args__ = (
        Index('unreferenced_row_log_idx_inserted', 'inserted'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    table_name = Column(String, nullable=False, primary_key=True)
    row_id = Column(Integer, nullable=False, primary_key=True)
    inserted = Column(DateTime(timezone=True), server_default=sql.func.now())


class URL(Base):
    __tablename__ = 'url'
    __table_args__ = (
        Index('url_idx_gid', 'gid', unique=True),
        Index('url_idx_url', 'url', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    url = Column(String, nullable=False)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())


class URLGIDRedirect(Base):
    __tablename__ = 'url_gid_redirect'
    __table_args__ = (
        Index('url_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='url_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('URL', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def url(self):
        return self.redirect


class Vote(Base):
    __tablename__ = 'vote'
    __table_args__ = (
        Index('vote_idx_edit', 'edit'),
        Index('vote_idx_editor_vote_time', 'editor', 'vote_time'),
        Index('vote_idx_editor_edit', 'editor', 'edit'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='vote_fk_editor'), nullable=False)
    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='vote_fk_edit'), nullable=False)
    vote = Column(SMALLINT, nullable=False)
    vote_time = Column(DateTime(timezone=True), server_default=sql.func.now())
    superseded = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)


class Work(Base):
    __tablename__ = 'work'
    __table_args__ = (
        Index('work_idx_gid', 'gid', unique=True),
        Index('work_idx_name', 'name'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    type_id = Column('type', Integer, ForeignKey(apply_schema('work_type.id', 'musicbrainz'), name='work_fk_type'))
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    type = relationship('WorkType', foreign_keys=[type_id])


class WorkLanguage(Base):
    __tablename__ = 'work_language'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    work_id = Column('work', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='work_language_fk_work'), nullable=False, primary_key=True)
    language_id = Column('language', Integer, ForeignKey(apply_schema('language.id', 'musicbrainz'), name='work_language_fk_language'), nullable=False, primary_key=True)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    work = relationship('Work', foreign_keys=[work_id], innerjoin=True)
    language = relationship('Language', foreign_keys=[language_id], innerjoin=True)


class WorkRatingRaw(Base):
    __tablename__ = 'work_rating_raw'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    work_id = Column('work', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='work_rating_raw_fk_work'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='work_rating_raw_fk_editor'), nullable=False, primary_key=True)
    rating = Column(SMALLINT, nullable=False)

    work = relationship('Work', foreign_keys=[work_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)


class WorkTagRaw(Base):
    __tablename__ = 'work_tag_raw'
    __table_args__ = (
        Index('work_tag_raw_idx_tag', 'tag'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    work_id = Column('work', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='work_tag_raw_fk_work'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='work_tag_raw_fk_editor'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='work_tag_raw_fk_tag'), nullable=False, primary_key=True)
    is_upvote = Column(Boolean, nullable=False, default=True, server_default=sql.true())

    work = relationship('Work', foreign_keys=[work_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class WorkAliasType(Base):
    __tablename__ = 'work_alias_type'
    __table_args__ = (
        Index('work_alias_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('work_alias_type.id', 'musicbrainz'), name='work_alias_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('WorkAliasType', foreign_keys=[parent_id])


class WorkAlias(Base):
    __tablename__ = 'work_alias'
    __table_args__ = (
        Index('work_alias_idx_work', 'work'),
        Index('work_alias_idx_primary', 'work', 'locale', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    work_id = Column('work', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='work_alias_fk_work'), nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    type_id = Column('type', Integer, ForeignKey(apply_schema('work_alias_type.id', 'musicbrainz'), name='work_alias_fk_type'))
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    primary_for_locale = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    work = relationship('Work', foreign_keys=[work_id], innerjoin=True)
    type = relationship('WorkAliasType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class WorkAnnotation(Base):
    __tablename__ = 'work_annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    work_id = Column('work', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='work_annotation_fk_work'), nullable=False, primary_key=True)
    annotation_id = Column('annotation', Integer, ForeignKey(apply_schema('annotation.id', 'musicbrainz'), name='work_annotation_fk_annotation'), nullable=False, primary_key=True)

    work = relationship('Work', foreign_keys=[work_id], innerjoin=True)
    annotation = relationship('Annotation', foreign_keys=[annotation_id], innerjoin=True)


class WorkGIDRedirect(Base):
    __tablename__ = 'work_gid_redirect'
    __table_args__ = (
        Index('work_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='work_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('Work', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def work(self):
        return self.redirect


class WorkMeta(Base):
    __tablename__ = 'work_meta'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='work_meta_fk_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    rating = Column(SMALLINT)
    rating_count = Column(Integer)

    work = relationship('Work', foreign_keys=[id], innerjoin=True, backref=backref('meta', uselist=False))


class WorkTag(Base):
    __tablename__ = 'work_tag'
    __table_args__ = (
        Index('work_tag_idx_tag', 'tag'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    work_id = Column('work', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='work_tag_fk_work'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='work_tag_fk_tag'), nullable=False, primary_key=True)
    count = Column(Integer, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    work = relationship('Work', foreign_keys=[work_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class WorkType(Base):
    __tablename__ = 'work_type'
    __table_args__ = (
        Index('work_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('work_type.id', 'musicbrainz'), name='work_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('WorkType', foreign_keys=[parent_id])


class WorkAttributeType(Base):
    __tablename__ = 'work_attribute_type'
    __table_args__ = (
        Index('work_attribute_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    free_text = Column(Boolean, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('work_attribute_type.id', 'musicbrainz'), name='work_attribute_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('WorkAttributeType', foreign_keys=[parent_id])


class WorkAttributeTypeAllowedValue(Base):
    __tablename__ = 'work_attribute_type_allowed_value'
    __table_args__ = (
        Index('work_attribute_type_allowed_value_idx_name', 'work_attribute_type'),
        Index('work_attribute_type_allowed_value_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    work_attribute_type_id = Column('work_attribute_type', Integer, ForeignKey(apply_schema('work_attribute_type.id', 'musicbrainz'), name='work_attribute_type_allowed_value_fk_work_attribute_type'), nullable=False)
    value = Column(String)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('work_attribute_type_allowed_value.id', 'musicbrainz'), name='work_attribute_type_allowed_value_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    work_attribute_type = relationship('WorkAttributeType', foreign_keys=[work_attribute_type_id], innerjoin=True)
    parent = relationship('WorkAttributeTypeAllowedValue', foreign_keys=[parent_id])


class WorkAttribute(Base):
    __tablename__ = 'work_attribute'
    __table_args__ = (
        Index('work_attribute_idx_work', 'work'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    work_id = Column('work', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='work_attribute_fk_work'), nullable=False)
    work_attribute_type_id = Column('work_attribute_type', Integer, ForeignKey(apply_schema('work_attribute_type.id', 'musicbrainz'), name='work_attribute_fk_work_attribute_type'), nullable=False)
    work_attribute_type_allowed_value_id = Column('work_attribute_type_allowed_value', Integer, ForeignKey(apply_schema('work_attribute_type_allowed_value.id', 'musicbrainz'), name='work_attribute_fk_work_attribute_type_allowed_value'))
    work_attribute_text = Column(String)

    work = relationship('Work', foreign_keys=[work_id], innerjoin=True)
    work_attribute_type = relationship('WorkAttributeType', foreign_keys=[work_attribute_type_id], innerjoin=True)
    work_attribute_type_allowed_value = relationship('WorkAttributeTypeAllowedValue', foreign_keys=[work_attribute_type_allowed_value_id])


class ArtType(Base):
    __tablename__ = 'art_type'
    __table_args__ = (
        Index('art_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('cover_art_archive', 'cover_art_archive')}
    )

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('art_type.id', 'cover_art_archive'), name='art_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('ArtType', foreign_keys=[parent_id])


class ImageType(Base):
    __tablename__ = 'image_type'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('cover_art_archive', 'cover_art_archive')}
    )

    mime_type = Column(String, nullable=False, primary_key=True)
    suffix = Column(String, nullable=False)


class CoverArt(Base):
    __tablename__ = 'cover_art'
    __table_args__ = (
        Index('cover_art_idx_release', 'release'),
        {'schema': mbdata.config.schemas.get('cover_art_archive', 'cover_art_archive')}
    )

    id = Column(BIGINT, nullable=False, primary_key=True)
    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='cover_art_fk_release', ondelete='CASCADE'), nullable=False)
    comment = Column(String, nullable=False, default='', server_default=sql.text("''"))
    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='cover_art_fk_edit'), nullable=False)
    ordering = Column(Integer, nullable=False)
    date_uploaded = Column(DateTime(timezone=True), nullable=False, server_default=sql.func.now())
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    mime_type = Column(String, ForeignKey(apply_schema('image_type.mime_type', 'cover_art_archive'), name='cover_art_fk_mime_type'), nullable=False)
    filesize = Column(Integer)
    thumb_250_filesize = Column(Integer)
    thumb_500_filesize = Column(Integer)
    thumb_1200_filesize = Column(Integer)

    release = relationship('Release', foreign_keys=[release_id], innerjoin=True)
    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)


class CoverArtType(Base):
    __tablename__ = 'cover_art_type'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('cover_art_archive', 'cover_art_archive')}
    )

    id = Column('id', BIGINT, ForeignKey(apply_schema('cover_art.id', 'cover_art_archive'), name='cover_art_type_fk_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    type_id = Column('type_id', Integer, ForeignKey(apply_schema('art_type.id', 'cover_art_archive'), name='cover_art_type_fk_type_id'), nullable=False, primary_key=True)

    cover_art = relationship('CoverArt', foreign_keys=[id], innerjoin=True)
    type = relationship('ArtType', foreign_keys=[type_id], innerjoin=True)


class ReleaseGroupCoverArt(Base):
    __tablename__ = 'release_group_cover_art'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('cover_art_archive', 'cover_art_archive')}
    )

    release_group_id = Column('release_group', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='release_group_cover_art_fk_release_group'), nullable=False, primary_key=True)
    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='release_group_cover_art_fk_release'), nullable=False)

    release_group = relationship('ReleaseGroup', foreign_keys=[release_group_id], innerjoin=True)
    release = relationship('Release', foreign_keys=[release_id], innerjoin=True)


class WikidocsIndex(Base):
    __tablename__ = 'wikidocs_index'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('wikidocs', 'wikidocs')}
    )

    page_name = Column(String, nullable=False, primary_key=True)
    revision = Column(Integer, nullable=False)


class LinkAreaAreaExample(Base):
    __tablename__ = 'l_area_area_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_area_area.id', 'musicbrainz'), name='l_area_area_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkAreaArea', foreign_keys=[id], innerjoin=True)


class LinkAreaArtistExample(Base):
    __tablename__ = 'l_area_artist_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_area_artist.id', 'musicbrainz'), name='l_area_artist_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkAreaArtist', foreign_keys=[id], innerjoin=True)


class LinkAreaEventExample(Base):
    __tablename__ = 'l_area_event_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_area_event.id', 'musicbrainz'), name='l_area_event_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkAreaEvent', foreign_keys=[id], innerjoin=True)


class LinkAreaGenreExample(Base):
    __tablename__ = 'l_area_genre_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_area_genre.id', 'musicbrainz'), name='l_area_genre_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkAreaGenre', foreign_keys=[id], innerjoin=True)


class LinkAreaInstrumentExample(Base):
    __tablename__ = 'l_area_instrument_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_area_instrument.id', 'musicbrainz'), name='l_area_instrument_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkAreaInstrument', foreign_keys=[id], innerjoin=True)


class LinkAreaLabelExample(Base):
    __tablename__ = 'l_area_label_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_area_label.id', 'musicbrainz'), name='l_area_label_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkAreaLabel', foreign_keys=[id], innerjoin=True)


class LinkAreaMoodExample(Base):
    __tablename__ = 'l_area_mood_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_area_mood.id', 'musicbrainz'), name='l_area_mood_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkAreaMood', foreign_keys=[id], innerjoin=True)


class LinkAreaPlaceExample(Base):
    __tablename__ = 'l_area_place_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_area_place.id', 'musicbrainz'), name='l_area_place_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkAreaPlace', foreign_keys=[id], innerjoin=True)


class LinkAreaRecordingExample(Base):
    __tablename__ = 'l_area_recording_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_area_recording.id', 'musicbrainz'), name='l_area_recording_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkAreaRecording', foreign_keys=[id], innerjoin=True)


class LinkAreaReleaseExample(Base):
    __tablename__ = 'l_area_release_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_area_release.id', 'musicbrainz'), name='l_area_release_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkAreaRelease', foreign_keys=[id], innerjoin=True)


class LinkAreaReleaseGroupExample(Base):
    __tablename__ = 'l_area_release_group_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_area_release_group.id', 'musicbrainz'), name='l_area_release_group_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkAreaReleaseGroup', foreign_keys=[id], innerjoin=True)


class LinkAreaURLExample(Base):
    __tablename__ = 'l_area_url_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_area_url.id', 'musicbrainz'), name='l_area_url_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkAreaURL', foreign_keys=[id], innerjoin=True)


class LinkAreaWorkExample(Base):
    __tablename__ = 'l_area_work_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_area_work.id', 'musicbrainz'), name='l_area_work_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkAreaWork', foreign_keys=[id], innerjoin=True)


class LinkArtistArtistExample(Base):
    __tablename__ = 'l_artist_artist_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_artist_artist.id', 'musicbrainz'), name='l_artist_artist_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkArtistArtist', foreign_keys=[id], innerjoin=True)


class LinkArtistEventExample(Base):
    __tablename__ = 'l_artist_event_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_artist_event.id', 'musicbrainz'), name='l_artist_event_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkArtistEvent', foreign_keys=[id], innerjoin=True)


class LinkArtistGenreExample(Base):
    __tablename__ = 'l_artist_genre_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_artist_genre.id', 'musicbrainz'), name='l_artist_genre_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkArtistGenre', foreign_keys=[id], innerjoin=True)


class LinkArtistInstrumentExample(Base):
    __tablename__ = 'l_artist_instrument_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_artist_instrument.id', 'musicbrainz'), name='l_artist_instrument_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkArtistInstrument', foreign_keys=[id], innerjoin=True)


class LinkArtistLabelExample(Base):
    __tablename__ = 'l_artist_label_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_artist_label.id', 'musicbrainz'), name='l_artist_label_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkArtistLabel', foreign_keys=[id], innerjoin=True)


class LinkArtistMoodExample(Base):
    __tablename__ = 'l_artist_mood_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_artist_mood.id', 'musicbrainz'), name='l_artist_mood_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkArtistMood', foreign_keys=[id], innerjoin=True)


class LinkArtistPlaceExample(Base):
    __tablename__ = 'l_artist_place_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_artist_place.id', 'musicbrainz'), name='l_artist_place_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkArtistPlace', foreign_keys=[id], innerjoin=True)


class LinkArtistRecordingExample(Base):
    __tablename__ = 'l_artist_recording_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_artist_recording.id', 'musicbrainz'), name='l_artist_recording_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkArtistRecording', foreign_keys=[id], innerjoin=True)


class LinkArtistReleaseExample(Base):
    __tablename__ = 'l_artist_release_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_artist_release.id', 'musicbrainz'), name='l_artist_release_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkArtistRelease', foreign_keys=[id], innerjoin=True)


class LinkArtistReleaseGroupExample(Base):
    __tablename__ = 'l_artist_release_group_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_artist_release_group.id', 'musicbrainz'), name='l_artist_release_group_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkArtistReleaseGroup', foreign_keys=[id], innerjoin=True)


class LinkArtistURLExample(Base):
    __tablename__ = 'l_artist_url_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_artist_url.id', 'musicbrainz'), name='l_artist_url_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkArtistURL', foreign_keys=[id], innerjoin=True)


class LinkArtistWorkExample(Base):
    __tablename__ = 'l_artist_work_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_artist_work.id', 'musicbrainz'), name='l_artist_work_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkArtistWork', foreign_keys=[id], innerjoin=True)


class LinkEventEventExample(Base):
    __tablename__ = 'l_event_event_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_event_event.id', 'musicbrainz'), name='l_event_event_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkEventEvent', foreign_keys=[id], innerjoin=True)


class LinkEventGenreExample(Base):
    __tablename__ = 'l_event_genre_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_event_genre.id', 'musicbrainz'), name='l_event_genre_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkEventGenre', foreign_keys=[id], innerjoin=True)


class LinkEventInstrumentExample(Base):
    __tablename__ = 'l_event_instrument_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_event_instrument.id', 'musicbrainz'), name='l_event_instrument_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkEventInstrument', foreign_keys=[id], innerjoin=True)


class LinkEventLabelExample(Base):
    __tablename__ = 'l_event_label_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_event_label.id', 'musicbrainz'), name='l_event_label_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkEventLabel', foreign_keys=[id], innerjoin=True)


class LinkEventMoodExample(Base):
    __tablename__ = 'l_event_mood_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_event_mood.id', 'musicbrainz'), name='l_event_mood_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkEventMood', foreign_keys=[id], innerjoin=True)


class LinkEventPlaceExample(Base):
    __tablename__ = 'l_event_place_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_event_place.id', 'musicbrainz'), name='l_event_place_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkEventPlace', foreign_keys=[id], innerjoin=True)


class LinkEventRecordingExample(Base):
    __tablename__ = 'l_event_recording_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_event_recording.id', 'musicbrainz'), name='l_event_recording_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkEventRecording', foreign_keys=[id], innerjoin=True)


class LinkEventReleaseExample(Base):
    __tablename__ = 'l_event_release_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_event_release.id', 'musicbrainz'), name='l_event_release_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkEventRelease', foreign_keys=[id], innerjoin=True)


class LinkEventReleaseGroupExample(Base):
    __tablename__ = 'l_event_release_group_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_event_release_group.id', 'musicbrainz'), name='l_event_release_group_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkEventReleaseGroup', foreign_keys=[id], innerjoin=True)


class LinkEventSeriesExample(Base):
    __tablename__ = 'l_event_series_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_event_series.id', 'musicbrainz'), name='l_event_series_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkEventSeries', foreign_keys=[id], innerjoin=True)


class LinkEventURLExample(Base):
    __tablename__ = 'l_event_url_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_event_url.id', 'musicbrainz'), name='l_event_url_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkEventURL', foreign_keys=[id], innerjoin=True)


class LinkEventWorkExample(Base):
    __tablename__ = 'l_event_work_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_event_work.id', 'musicbrainz'), name='l_event_work_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkEventWork', foreign_keys=[id], innerjoin=True)


class LinkGenreGenreExample(Base):
    __tablename__ = 'l_genre_genre_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_genre_genre.id', 'musicbrainz'), name='l_genre_genre_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkGenreGenre', foreign_keys=[id], innerjoin=True)


class LinkGenreInstrumentExample(Base):
    __tablename__ = 'l_genre_instrument_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_genre_instrument.id', 'musicbrainz'), name='l_genre_instrument_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkGenreInstrument', foreign_keys=[id], innerjoin=True)


class LinkGenreLabelExample(Base):
    __tablename__ = 'l_genre_label_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_genre_label.id', 'musicbrainz'), name='l_genre_label_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkGenreLabel', foreign_keys=[id], innerjoin=True)


class LinkGenreMoodExample(Base):
    __tablename__ = 'l_genre_mood_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_genre_mood.id', 'musicbrainz'), name='l_genre_mood_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkGenreMood', foreign_keys=[id], innerjoin=True)


class LinkGenrePlaceExample(Base):
    __tablename__ = 'l_genre_place_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_genre_place.id', 'musicbrainz'), name='l_genre_place_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkGenrePlace', foreign_keys=[id], innerjoin=True)


class LinkGenreRecordingExample(Base):
    __tablename__ = 'l_genre_recording_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_genre_recording.id', 'musicbrainz'), name='l_genre_recording_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkGenreRecording', foreign_keys=[id], innerjoin=True)


class LinkGenreReleaseExample(Base):
    __tablename__ = 'l_genre_release_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_genre_release.id', 'musicbrainz'), name='l_genre_release_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkGenreRelease', foreign_keys=[id], innerjoin=True)


class LinkGenreReleaseGroupExample(Base):
    __tablename__ = 'l_genre_release_group_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_genre_release_group.id', 'musicbrainz'), name='l_genre_release_group_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkGenreReleaseGroup', foreign_keys=[id], innerjoin=True)


class LinkGenreSeriesExample(Base):
    __tablename__ = 'l_genre_series_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_genre_series.id', 'musicbrainz'), name='l_genre_series_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkGenreSeries', foreign_keys=[id], innerjoin=True)


class LinkGenreURLExample(Base):
    __tablename__ = 'l_genre_url_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_genre_url.id', 'musicbrainz'), name='l_genre_url_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkGenreURL', foreign_keys=[id], innerjoin=True)


class LinkGenreWorkExample(Base):
    __tablename__ = 'l_genre_work_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_genre_work.id', 'musicbrainz'), name='l_genre_work_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkGenreWork', foreign_keys=[id], innerjoin=True)


class LinkInstrumentInstrumentExample(Base):
    __tablename__ = 'l_instrument_instrument_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_instrument_instrument.id', 'musicbrainz'), name='l_instrument_instrument_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkInstrumentInstrument', foreign_keys=[id], innerjoin=True)


class LinkInstrumentLabelExample(Base):
    __tablename__ = 'l_instrument_label_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_instrument_label.id', 'musicbrainz'), name='l_instrument_label_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkInstrumentLabel', foreign_keys=[id], innerjoin=True)


class LinkInstrumentMoodExample(Base):
    __tablename__ = 'l_instrument_mood_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_instrument_mood.id', 'musicbrainz'), name='l_instrument_mood_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkInstrumentMood', foreign_keys=[id], innerjoin=True)


class LinkInstrumentPlaceExample(Base):
    __tablename__ = 'l_instrument_place_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_instrument_place.id', 'musicbrainz'), name='l_instrument_place_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkInstrumentPlace', foreign_keys=[id], innerjoin=True)


class LinkInstrumentRecordingExample(Base):
    __tablename__ = 'l_instrument_recording_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_instrument_recording.id', 'musicbrainz'), name='l_instrument_recording_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkInstrumentRecording', foreign_keys=[id], innerjoin=True)


class LinkInstrumentReleaseExample(Base):
    __tablename__ = 'l_instrument_release_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_instrument_release.id', 'musicbrainz'), name='l_instrument_release_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkInstrumentRelease', foreign_keys=[id], innerjoin=True)


class LinkInstrumentReleaseGroupExample(Base):
    __tablename__ = 'l_instrument_release_group_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_instrument_release_group.id', 'musicbrainz'), name='l_instrument_release_group_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkInstrumentReleaseGroup', foreign_keys=[id], innerjoin=True)


class LinkInstrumentSeriesExample(Base):
    __tablename__ = 'l_instrument_series_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_instrument_series.id', 'musicbrainz'), name='l_instrument_series_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkInstrumentSeries', foreign_keys=[id], innerjoin=True)


class LinkInstrumentURLExample(Base):
    __tablename__ = 'l_instrument_url_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_instrument_url.id', 'musicbrainz'), name='l_instrument_url_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkInstrumentURL', foreign_keys=[id], innerjoin=True)


class LinkInstrumentWorkExample(Base):
    __tablename__ = 'l_instrument_work_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_instrument_work.id', 'musicbrainz'), name='l_instrument_work_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkInstrumentWork', foreign_keys=[id], innerjoin=True)


class LinkLabelLabelExample(Base):
    __tablename__ = 'l_label_label_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_label_label.id', 'musicbrainz'), name='l_label_label_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkLabelLabel', foreign_keys=[id], innerjoin=True)


class LinkLabelMoodExample(Base):
    __tablename__ = 'l_label_mood_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_label_mood.id', 'musicbrainz'), name='l_label_mood_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkLabelMood', foreign_keys=[id], innerjoin=True)


class LinkLabelPlaceExample(Base):
    __tablename__ = 'l_label_place_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_label_place.id', 'musicbrainz'), name='l_label_place_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkLabelPlace', foreign_keys=[id], innerjoin=True)


class LinkLabelRecordingExample(Base):
    __tablename__ = 'l_label_recording_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_label_recording.id', 'musicbrainz'), name='l_label_recording_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkLabelRecording', foreign_keys=[id], innerjoin=True)


class LinkLabelReleaseExample(Base):
    __tablename__ = 'l_label_release_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_label_release.id', 'musicbrainz'), name='l_label_release_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkLabelRelease', foreign_keys=[id], innerjoin=True)


class LinkLabelReleaseGroupExample(Base):
    __tablename__ = 'l_label_release_group_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_label_release_group.id', 'musicbrainz'), name='l_label_release_group_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkLabelReleaseGroup', foreign_keys=[id], innerjoin=True)


class LinkLabelURLExample(Base):
    __tablename__ = 'l_label_url_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_label_url.id', 'musicbrainz'), name='l_label_url_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkLabelURL', foreign_keys=[id], innerjoin=True)


class LinkLabelWorkExample(Base):
    __tablename__ = 'l_label_work_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_label_work.id', 'musicbrainz'), name='l_label_work_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkLabelWork', foreign_keys=[id], innerjoin=True)


class LinkMoodMoodExample(Base):
    __tablename__ = 'l_mood_mood_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_mood_mood.id', 'musicbrainz'), name='l_mood_mood_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkMoodMood', foreign_keys=[id], innerjoin=True)


class LinkMoodPlaceExample(Base):
    __tablename__ = 'l_mood_place_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_mood_place.id', 'musicbrainz'), name='l_mood_place_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkMoodPlace', foreign_keys=[id], innerjoin=True)


class LinkMoodRecordingExample(Base):
    __tablename__ = 'l_mood_recording_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_mood_recording.id', 'musicbrainz'), name='l_mood_recording_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkMoodRecording', foreign_keys=[id], innerjoin=True)


class LinkMoodReleaseExample(Base):
    __tablename__ = 'l_mood_release_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_mood_release.id', 'musicbrainz'), name='l_mood_release_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkMoodRelease', foreign_keys=[id], innerjoin=True)


class LinkMoodReleaseGroupExample(Base):
    __tablename__ = 'l_mood_release_group_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_mood_release_group.id', 'musicbrainz'), name='l_mood_release_group_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkMoodReleaseGroup', foreign_keys=[id], innerjoin=True)


class LinkMoodSeriesExample(Base):
    __tablename__ = 'l_mood_series_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_mood_series.id', 'musicbrainz'), name='l_mood_series_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkMoodSeries', foreign_keys=[id], innerjoin=True)


class LinkMoodURLExample(Base):
    __tablename__ = 'l_mood_url_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_mood_url.id', 'musicbrainz'), name='l_mood_url_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkMoodURL', foreign_keys=[id], innerjoin=True)


class LinkMoodWorkExample(Base):
    __tablename__ = 'l_mood_work_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_mood_work.id', 'musicbrainz'), name='l_mood_work_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkMoodWork', foreign_keys=[id], innerjoin=True)


class LinkPlacePlaceExample(Base):
    __tablename__ = 'l_place_place_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_place_place.id', 'musicbrainz'), name='l_place_place_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkPlacePlace', foreign_keys=[id], innerjoin=True)


class LinkPlaceRecordingExample(Base):
    __tablename__ = 'l_place_recording_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_place_recording.id', 'musicbrainz'), name='l_place_recording_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkPlaceRecording', foreign_keys=[id], innerjoin=True)


class LinkPlaceReleaseExample(Base):
    __tablename__ = 'l_place_release_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_place_release.id', 'musicbrainz'), name='l_place_release_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkPlaceRelease', foreign_keys=[id], innerjoin=True)


class LinkPlaceReleaseGroupExample(Base):
    __tablename__ = 'l_place_release_group_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_place_release_group.id', 'musicbrainz'), name='l_place_release_group_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkPlaceReleaseGroup', foreign_keys=[id], innerjoin=True)


class LinkPlaceURLExample(Base):
    __tablename__ = 'l_place_url_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_place_url.id', 'musicbrainz'), name='l_place_url_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkPlaceURL', foreign_keys=[id], innerjoin=True)


class LinkPlaceWorkExample(Base):
    __tablename__ = 'l_place_work_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_place_work.id', 'musicbrainz'), name='l_place_work_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkPlaceWork', foreign_keys=[id], innerjoin=True)


class LinkRecordingRecordingExample(Base):
    __tablename__ = 'l_recording_recording_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_recording_recording.id', 'musicbrainz'), name='l_recording_recording_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkRecordingRecording', foreign_keys=[id], innerjoin=True)


class LinkRecordingReleaseExample(Base):
    __tablename__ = 'l_recording_release_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_recording_release.id', 'musicbrainz'), name='l_recording_release_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkRecordingRelease', foreign_keys=[id], innerjoin=True)


class LinkRecordingReleaseGroupExample(Base):
    __tablename__ = 'l_recording_release_group_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_recording_release_group.id', 'musicbrainz'), name='l_recording_release_group_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkRecordingReleaseGroup', foreign_keys=[id], innerjoin=True)


class LinkRecordingURLExample(Base):
    __tablename__ = 'l_recording_url_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_recording_url.id', 'musicbrainz'), name='l_recording_url_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkRecordingURL', foreign_keys=[id], innerjoin=True)


class LinkRecordingWorkExample(Base):
    __tablename__ = 'l_recording_work_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_recording_work.id', 'musicbrainz'), name='l_recording_work_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkRecordingWork', foreign_keys=[id], innerjoin=True)


class LinkReleaseReleaseExample(Base):
    __tablename__ = 'l_release_release_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_release_release.id', 'musicbrainz'), name='l_release_release_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkReleaseRelease', foreign_keys=[id], innerjoin=True)


class LinkReleaseReleaseGroupExample(Base):
    __tablename__ = 'l_release_release_group_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_release_release_group.id', 'musicbrainz'), name='l_release_release_group_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkReleaseReleaseGroup', foreign_keys=[id], innerjoin=True)


class LinkReleaseURLExample(Base):
    __tablename__ = 'l_release_url_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_release_url.id', 'musicbrainz'), name='l_release_url_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkReleaseURL', foreign_keys=[id], innerjoin=True)


class LinkReleaseWorkExample(Base):
    __tablename__ = 'l_release_work_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_release_work.id', 'musicbrainz'), name='l_release_work_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkReleaseWork', foreign_keys=[id], innerjoin=True)


class LinkReleaseGroupReleaseGroupExample(Base):
    __tablename__ = 'l_release_group_release_group_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_release_group_release_group.id', 'musicbrainz'), name='l_release_group_release_group_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkReleaseGroupReleaseGroup', foreign_keys=[id], innerjoin=True)


class LinkReleaseGroupURLExample(Base):
    __tablename__ = 'l_release_group_url_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_release_group_url.id', 'musicbrainz'), name='l_release_group_url_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkReleaseGroupURL', foreign_keys=[id], innerjoin=True)


class LinkReleaseGroupWorkExample(Base):
    __tablename__ = 'l_release_group_work_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_release_group_work.id', 'musicbrainz'), name='l_release_group_work_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkReleaseGroupWork', foreign_keys=[id], innerjoin=True)


class LinkAreaSeriesExample(Base):
    __tablename__ = 'l_area_series_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_area_series.id', 'musicbrainz'), name='l_area_series_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkAreaSeries', foreign_keys=[id], innerjoin=True)


class LinkArtistSeriesExample(Base):
    __tablename__ = 'l_artist_series_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_artist_series.id', 'musicbrainz'), name='l_artist_series_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkArtistSeries', foreign_keys=[id], innerjoin=True)


class LinkLabelSeriesExample(Base):
    __tablename__ = 'l_label_series_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_label_series.id', 'musicbrainz'), name='l_label_series_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkLabelSeries', foreign_keys=[id], innerjoin=True)


class LinkPlaceSeriesExample(Base):
    __tablename__ = 'l_place_series_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_place_series.id', 'musicbrainz'), name='l_place_series_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkPlaceSeries', foreign_keys=[id], innerjoin=True)


class LinkRecordingSeriesExample(Base):
    __tablename__ = 'l_recording_series_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_recording_series.id', 'musicbrainz'), name='l_recording_series_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkRecordingSeries', foreign_keys=[id], innerjoin=True)


class LinkReleaseSeriesExample(Base):
    __tablename__ = 'l_release_series_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_release_series.id', 'musicbrainz'), name='l_release_series_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkReleaseSeries', foreign_keys=[id], innerjoin=True)


class LinkReleaseGroupSeriesExample(Base):
    __tablename__ = 'l_release_group_series_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_release_group_series.id', 'musicbrainz'), name='l_release_group_series_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkReleaseGroupSeries', foreign_keys=[id], innerjoin=True)


class LinkSeriesSeriesExample(Base):
    __tablename__ = 'l_series_series_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_series_series.id', 'musicbrainz'), name='l_series_series_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkSeriesSeries', foreign_keys=[id], innerjoin=True)


class LinkSeriesURLExample(Base):
    __tablename__ = 'l_series_url_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_series_url.id', 'musicbrainz'), name='l_series_url_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkSeriesURL', foreign_keys=[id], innerjoin=True)


class LinkSeriesWorkExample(Base):
    __tablename__ = 'l_series_work_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_series_work.id', 'musicbrainz'), name='l_series_work_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkSeriesWork', foreign_keys=[id], innerjoin=True)


class LinkURLURLExample(Base):
    __tablename__ = 'l_url_url_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_url_url.id', 'musicbrainz'), name='l_url_url_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkURLURL', foreign_keys=[id], innerjoin=True)


class LinkURLWorkExample(Base):
    __tablename__ = 'l_url_work_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_url_work.id', 'musicbrainz'), name='l_url_work_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkURLWork', foreign_keys=[id], innerjoin=True)


class LinkWorkWorkExample(Base):
    __tablename__ = 'l_work_work_example'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('l_work_work.id', 'musicbrainz'), name='l_work_work_example_fk_id'), nullable=False, primary_key=True)
    published = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)

    link = relationship('LinkWorkWork', foreign_keys=[id], innerjoin=True)


class LinkTypeDocumentation(Base):
    __tablename__ = 'link_type_documentation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('documentation', 'documentation')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('link_type.id', 'musicbrainz'), name='link_type_documentation_fk_id'), nullable=False, primary_key=True)
    documentation = Column(String, nullable=False)
    examples_deleted = Column(SMALLINT, nullable=False, default=0, server_default=sql.text('0'))

    link_type = relationship('LinkType', foreign_keys=[id], innerjoin=True)


class Statistic(Base):
    __tablename__ = 'statistic'
    __table_args__ = (
        Index('statistic_name', 'name'),
        Index('statistic_name_date_collected', 'name', 'date_collected', unique=True),
        {'schema': mbdata.config.schemas.get('statistics', 'statistics')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    value = Column(Integer, nullable=False)
    date_collected = Column(Date, nullable=False, server_default=sql.func.now())


class StatisticEvent(Base):
    __tablename__ = 'statistic_event'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('statistics', 'statistics')}
    )

    date = Column(Date, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    description = Column(String, nullable=False)


