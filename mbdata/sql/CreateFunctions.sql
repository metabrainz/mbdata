\set ON_ERROR_STOP 1
BEGIN;

CREATE OR REPLACE FUNCTION _median(INTEGER[]) RETURNS INTEGER AS $$
  WITH q AS (
      SELECT val
      FROM unnest($1) val
      WHERE VAL IS NOT NULL
      ORDER BY val
  )
  SELECT val
  FROM q
  LIMIT 1
  -- Subtracting (n + 1) % 2 creates a left bias
  OFFSET greatest(0, floor((select count(*) FROM q) / 2.0) - ((select count(*) + 1 FROM q) % 2));
$$ LANGUAGE sql IMMUTABLE;

CREATE AGGREGATE median(INTEGER) (
  SFUNC=array_append,
  STYPE=INTEGER[],
  FINALFUNC=_median,
  INITCOND='{}'
);

-- Generates UUID version 4 (random-based)
CREATE OR REPLACE FUNCTION generate_uuid_v4() RETURNS uuid
    AS $$
DECLARE
    value VARCHAR(36);
BEGIN
    value =          lpad(to_hex(ceil(random() * 255)::int), 2, '0');
    value = value || lpad(to_hex(ceil(random() * 255)::int), 2, '0');
    value = value || lpad(to_hex(ceil(random() * 255)::int), 2, '0');
    value = value || lpad(to_hex(ceil(random() * 255)::int), 2, '0');
    value = value || '-';
    value = value || lpad(to_hex(ceil(random() * 255)::int), 2, '0');
    value = value || lpad(to_hex(ceil(random() * 255)::int), 2, '0');
    value = value || '-';
    value = value || lpad((to_hex((ceil(random() * 255)::int & 15) | 64)), 2, '0');
    value = value || lpad(to_hex(ceil(random() * 255)::int), 2, '0');
    value = value || '-';
    value = value || lpad((to_hex((ceil(random() * 255)::int & 63) | 128)), 2, '0');
    value = value || lpad(to_hex(ceil(random() * 255)::int), 2, '0');
    value = value || '-';
    value = value || lpad(to_hex(ceil(random() * 255)::int), 2, '0');
    value = value || lpad(to_hex(ceil(random() * 255)::int), 2, '0');
    value = value || lpad(to_hex(ceil(random() * 255)::int), 2, '0');
    value = value || lpad(to_hex(ceil(random() * 255)::int), 2, '0');
    value = value || lpad(to_hex(ceil(random() * 255)::int), 2, '0');
    value = value || lpad(to_hex(ceil(random() * 255)::int), 2, '0');
    RETURN value::uuid;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION from_hex(t text) RETURNS integer
    AS $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN EXECUTE 'SELECT x'''||t||'''::integer AS hex' LOOP
        RETURN r.hex;
    END LOOP;
END
$$ LANGUAGE plpgsql IMMUTABLE STRICT;

-- NameSpace_URL = '6ba7b8119dad11d180b400c04fd430c8'
CREATE OR REPLACE FUNCTION generate_uuid_v3(namespace varchar, name varchar) RETURNS uuid
    AS $$
DECLARE
    value varchar(36);
    bytes varchar;
BEGIN
    bytes = md5(decode(namespace, 'hex') || decode(name, 'escape'));
    value = substr(bytes, 1+0, 8);
    value = value || '-';
    value = value || substr(bytes, 1+2*4, 4);
    value = value || '-';
    value = value || lpad(to_hex((from_hex(substr(bytes, 1+2*6, 2)) & 15) | 48), 2, '0');
    value = value || substr(bytes, 1+2*7, 2);
    value = value || '-';
    value = value || lpad(to_hex((from_hex(substr(bytes, 1+2*8, 2)) & 63) | 128), 2, '0');
    value = value || substr(bytes, 1+2*9, 2);
    value = value || '-';
    value = value || substr(bytes, 1+2*10, 12);
    return value::uuid;
END;
$$ LANGUAGE 'plpgsql' IMMUTABLE STRICT;


CREATE OR REPLACE FUNCTION inc_ref_count(tbl varchar, row_id integer, val integer) RETURNS void AS $$
BEGIN
    -- increment ref_count for the new name
    EXECUTE 'SELECT ref_count FROM ' || tbl || ' WHERE id = ' || row_id || ' FOR UPDATE';
    EXECUTE 'UPDATE ' || tbl || ' SET ref_count = ref_count + ' || val || ' WHERE id = ' || row_id;
    RETURN;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION dec_ref_count(tbl varchar, row_id integer, val integer) RETURNS void AS $$
DECLARE
    ref_count integer;
BEGIN
    -- decrement ref_count for the old name,
    -- or prepare it for deletion if ref_count would drop to 0
    EXECUTE 'SELECT ref_count FROM ' || tbl || ' WHERE id = ' || row_id || ' FOR UPDATE' INTO ref_count;
    IF ref_count <= val THEN
        EXECUTE 'INSERT INTO unreferenced_row_log (table_name, row_id) VALUES ($1, $2)' USING tbl, row_id;
    END IF;
    EXECUTE 'UPDATE ' || tbl || ' SET ref_count = ref_count - ' || val || ' WHERE id = ' || row_id;
    RETURN;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION integer_date(year SMALLINT, month SMALLINT, day SMALLINT)
RETURNS INTEGER AS $$
    -- Returns an integer representation of the given date, keeping
    -- NULL values sorted last.
    SELECT (
        CASE
            WHEN year IS NULL AND month IS NULL AND day IS NULL
            THEN NULL
            ELSE (
                coalesce(year::TEXT, '9999') ||
                lpad(coalesce(month::TEXT, '99'), 2, '0') ||
                lpad(coalesce(day::TEXT, '99'), 2, '0')
            )::INTEGER
        END
    )
$$ LANGUAGE SQL IMMUTABLE PARALLEL SAFE;

-----------------------------------------------------------------------
-- area triggers
-----------------------------------------------------------------------

-- Ensure attribute type allows free text if free text is added
CREATE OR REPLACE FUNCTION ensure_area_attribute_type_allows_text()
RETURNS trigger AS $$
BEGIN
    IF NEW.area_attribute_text IS NOT NULL
        AND NOT EXISTS (
            SELECT TRUE
              FROM area_attribute_type
             WHERE area_attribute_type.id = NEW.area_attribute_type
               AND free_text
    )
    THEN
        RAISE EXCEPTION 'This attribute type can not contain free text';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- artist triggers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION a_ins_artist() RETURNS trigger AS $$
BEGIN
    -- add a new entry to the artist_meta table
    INSERT INTO artist_meta (id) VALUES (NEW.id);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

-- Ensure attribute type allows free text if free text is added
CREATE OR REPLACE FUNCTION ensure_artist_attribute_type_allows_text()
RETURNS trigger AS $$
BEGIN
    IF NEW.artist_attribute_text IS NOT NULL
        AND NOT EXISTS (
            SELECT TRUE
              FROM artist_attribute_type
             WHERE artist_attribute_type.id = NEW.artist_attribute_type
               AND free_text
    )
    THEN
        RAISE EXCEPTION 'This attribute type can not contain free text';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- artist_credit triggers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION b_upd_artist_credit_name() RETURNS trigger AS $$
BEGIN
    -- Artist credits are assumed to be immutable. When changes need to
    -- be made, we `find_or_insert` the new artist credits and swap
    -- them with the old ones rather than mutate existing entries.
    --
    -- This simplifies a lot of assumptions we can make about their
    -- cacheability, and the consistency of materialized tables like
    -- artist_release_group.
    RAISE EXCEPTION 'Cannot update artist_credit_name';
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- editor triggers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION check_editor_name() RETURNS trigger AS $$
BEGIN
    IF (SELECT 1 FROM old_editor_name WHERE lower(name) = lower(NEW.name))
    THEN
        RAISE EXCEPTION 'Attempt to use a previously-used editor name.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- event triggers
-----------------------------------------------------------------------

-- Ensure attribute type allows free text if free text is added
CREATE OR REPLACE FUNCTION ensure_event_attribute_type_allows_text()
RETURNS trigger AS $$
BEGIN
    IF NEW.event_attribute_text IS NOT NULL
        AND NOT EXISTS (
            SELECT TRUE
              FROM event_attribute_type
             WHERE event_attribute_type.id = NEW.event_attribute_type
               AND free_text
    )
    THEN
        RAISE EXCEPTION 'This attribute type can not contain free text';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- event triggers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION a_ins_event() RETURNS trigger AS $$
BEGIN
    -- add a new entry to the event_meta table
    INSERT INTO event_meta (id) VALUES (NEW.id);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- instrument triggers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION a_ins_instrument() RETURNS trigger AS $$
BEGIN
    WITH inserted_rows (id) AS (
        INSERT INTO link_attribute_type (parent, root, child_order, gid, name, description)
        VALUES (14, 14, 0, NEW.gid, NEW.name, NEW.description)
        RETURNING id
    ) INSERT INTO link_creditable_attribute_type (attribute_type) SELECT id FROM inserted_rows;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION a_upd_instrument() RETURNS trigger AS $$
BEGIN
    UPDATE link_attribute_type SET name = NEW.name, description = NEW.description WHERE gid = NEW.gid;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'no link_attribute_type found for instrument %', NEW.gid;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION a_del_instrument() RETURNS trigger AS $$
BEGIN
    DELETE FROM link_attribute_type WHERE gid = OLD.gid;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'no link_attribute_type found for instrument %', NEW.gid;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Ensure attribute type allows free text if free text is added
CREATE OR REPLACE FUNCTION ensure_instrument_attribute_type_allows_text()
RETURNS trigger AS $$
BEGIN
    IF NEW.instrument_attribute_text IS NOT NULL
        AND NOT EXISTS (
            SELECT TRUE
              FROM instrument_attribute_type
             WHERE instrument_attribute_type.id = NEW.instrument_attribute_type
               AND free_text
    )
    THEN
        RAISE EXCEPTION 'This attribute type can not contain free text';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- label triggers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION a_ins_label() RETURNS trigger AS $$
BEGIN
    INSERT INTO label_meta (id) VALUES (NEW.id);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

-- Ensure attribute type allows free text if free text is added
CREATE OR REPLACE FUNCTION ensure_label_attribute_type_allows_text()
RETURNS trigger AS $$
BEGIN
    IF NEW.label_attribute_text IS NOT NULL
        AND NOT EXISTS (
            SELECT TRUE
              FROM label_attribute_type
             WHERE label_attribute_type.id = NEW.label_attribute_type
               AND free_text
    )
    THEN
        RAISE EXCEPTION 'This attribute type can not contain free text';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- medium triggers
-----------------------------------------------------------------------

-- Ensure attribute type allows free text if free text is added
CREATE OR REPLACE FUNCTION ensure_medium_attribute_type_allows_text()
RETURNS trigger AS $$
BEGIN
    IF NEW.medium_attribute_text IS NOT NULL
        AND NOT EXISTS (
            SELECT TRUE
              FROM medium_attribute_type
             WHERE medium_attribute_type.id = NEW.medium_attribute_type
               AND free_text
    )
    THEN
        RAISE EXCEPTION 'This attribute type can not contain free text';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- place triggers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION a_ins_place() RETURNS trigger AS $$
BEGIN
    -- add a new entry to the place_meta table
    INSERT INTO place_meta (id) VALUES (NEW.id);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

-- Ensure attribute type allows free text if free text is added
CREATE OR REPLACE FUNCTION ensure_place_attribute_type_allows_text()
RETURNS trigger AS $$
BEGIN
    IF NEW.place_attribute_text IS NOT NULL
        AND NOT EXISTS (
            SELECT TRUE
              FROM place_attribute_type
             WHERE place_attribute_type.id = NEW.place_attribute_type
               AND free_text
    )
    THEN
        RAISE EXCEPTION 'This attribute type can not contain free text';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- recording triggers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION median_track_length(recording_id integer)
RETURNS integer AS $$
  SELECT median(track.length) FROM track WHERE recording = $1;
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION b_upd_recording() RETURNS TRIGGER AS $$
BEGIN
  IF OLD.length IS DISTINCT FROM NEW.length
    AND EXISTS (SELECT TRUE FROM track WHERE recording = NEW.id)
    AND NEW.length IS DISTINCT FROM median_track_length(NEW.id)
  THEN
    NEW.length = median_track_length(NEW.id);
  END IF;

  NEW.last_updated = now();
  RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_ins_recording() RETURNS trigger AS $$
BEGIN
    PERFORM inc_ref_count('artist_credit', NEW.artist_credit, 1);
    INSERT INTO recording_meta (id) VALUES (NEW.id);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_upd_recording() RETURNS trigger AS $$
BEGIN
    IF NEW.artist_credit != OLD.artist_credit THEN
        PERFORM dec_ref_count('artist_credit', OLD.artist_credit, 1);
        PERFORM inc_ref_count('artist_credit', NEW.artist_credit, 1);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_del_recording() RETURNS trigger AS $$
BEGIN
    PERFORM dec_ref_count('artist_credit', OLD.artist_credit, 1);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

-- Ensure attribute type allows free text if free text is added
CREATE OR REPLACE FUNCTION ensure_recording_attribute_type_allows_text()
RETURNS trigger AS $$
BEGIN
    IF NEW.recording_attribute_text IS NOT NULL
        AND NOT EXISTS (
            SELECT TRUE
              FROM recording_attribute_type
             WHERE recording_attribute_type.id = NEW.recording_attribute_type
               AND free_text
    )
    THEN
        RAISE EXCEPTION 'This attribute type can not contain free text';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- release triggers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION a_ins_release() RETURNS trigger AS $$
BEGIN
    -- increment ref_count of the name
    PERFORM inc_ref_count('artist_credit', NEW.artist_credit, 1);
    -- increment release_count of the parent release group
    UPDATE release_group_meta SET release_count = release_count + 1 WHERE id = NEW.release_group;
    -- add new release_meta
    INSERT INTO release_meta (id) VALUES (NEW.id);
    INSERT INTO artist_release_pending_update VALUES (NEW.id);
    INSERT INTO artist_release_group_pending_update VALUES (NEW.release_group);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_upd_release() RETURNS trigger AS $$
BEGIN
    IF NEW.artist_credit != OLD.artist_credit THEN
        PERFORM dec_ref_count('artist_credit', OLD.artist_credit, 1);
        PERFORM inc_ref_count('artist_credit', NEW.artist_credit, 1);
    END IF;
    IF (
        NEW.status IS DISTINCT FROM OLD.status AND
        (NEW.status = 6 OR OLD.status = 6)
    ) THEN
        PERFORM set_release_first_release_date(NEW.id);

        -- avoid executing it twice as this will be executed a few lines below if RG changes
        IF NEW.release_group = OLD.release_group THEN
            PERFORM set_release_group_first_release_date(NEW.release_group);
        END IF;

        PERFORM set_releases_recordings_first_release_dates(ARRAY[NEW.id]);
    END IF;
    IF NEW.release_group != OLD.release_group THEN
        -- release group is changed, decrement release_count in the original RG, increment in the new one
        UPDATE release_group_meta SET release_count = release_count - 1 WHERE id = OLD.release_group;
        UPDATE release_group_meta SET release_count = release_count + 1 WHERE id = NEW.release_group;
        PERFORM set_release_group_first_release_date(OLD.release_group);
        PERFORM set_release_group_first_release_date(NEW.release_group);
    END IF;
    IF (
        NEW.status IS DISTINCT FROM OLD.status OR
        NEW.release_group != OLD.release_group OR
        NEW.artist_credit != OLD.artist_credit
    ) THEN
        INSERT INTO artist_release_group_pending_update
        VALUES (NEW.release_group), (OLD.release_group);
    END IF;
    IF (
        NEW.barcode IS DISTINCT FROM OLD.barcode OR
        NEW.name != OLD.name OR
        NEW.artist_credit != OLD.artist_credit
    ) THEN
        INSERT INTO artist_release_pending_update VALUES (OLD.id);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_del_release() RETURNS trigger AS $$
BEGIN
    -- decrement ref_count of the name
    PERFORM dec_ref_count('artist_credit', OLD.artist_credit, 1);
    -- decrement release_count of the parent release group
    UPDATE release_group_meta SET release_count = release_count - 1 WHERE id = OLD.release_group;
    INSERT INTO artist_release_pending_update VALUES (OLD.id);
    INSERT INTO artist_release_group_pending_update VALUES (OLD.release_group);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_upd_release_group_primary_type_mirror()
RETURNS trigger AS $$
BEGIN
    -- DO NOT modify any replicated tables in this function; it's used
    -- by a trigger on mirrors.
    IF (NEW.child_order IS DISTINCT FROM OLD.child_order)
    THEN
        INSERT INTO artist_release_group_pending_update (
            SELECT id FROM release_group
            WHERE release_group.type = OLD.id
        );
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_upd_release_group_secondary_type_mirror()
RETURNS trigger AS $$
BEGIN
    -- DO NOT modify any replicated tables in this function; it's used
    -- by a trigger on mirrors.
    IF (NEW.child_order IS DISTINCT FROM OLD.child_order)
    THEN
        INSERT INTO artist_release_group_pending_update (
            SELECT release_group
            FROM release_group_secondary_type_join
            WHERE secondary_type = OLD.id
        );
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_ins_release_group_secondary_type_join()
RETURNS trigger AS $$
BEGIN
    INSERT INTO artist_release_group_pending_update VALUES (NEW.release_group);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_del_release_group_secondary_type_join()
RETURNS trigger AS $$
BEGIN
    INSERT INTO artist_release_group_pending_update VALUES (OLD.release_group);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_ins_release_label()
RETURNS trigger AS $$
BEGIN
    INSERT INTO artist_release_pending_update VALUES (NEW.release);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_upd_release_label()
RETURNS trigger AS $$
BEGIN
    IF NEW.catalog_number IS DISTINCT FROM OLD.catalog_number THEN
        INSERT INTO artist_release_pending_update VALUES (OLD.release);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_del_release_label()
RETURNS trigger AS $$
BEGIN
    INSERT INTO artist_release_pending_update VALUES (OLD.release);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

-- Ensure attribute type allows free text if free text is added
CREATE OR REPLACE FUNCTION ensure_release_attribute_type_allows_text()
RETURNS trigger AS $$
BEGIN
    IF NEW.release_attribute_text IS NOT NULL
        AND NOT EXISTS (
            SELECT TRUE
              FROM release_attribute_type
             WHERE release_attribute_type.id = NEW.release_attribute_type
               AND free_text
    )
    THEN
        RAISE EXCEPTION 'This attribute type can not contain free text';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- release_group triggers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION a_ins_release_group() RETURNS trigger AS $$
BEGIN
    PERFORM inc_ref_count('artist_credit', NEW.artist_credit, 1);
    INSERT INTO release_group_meta (id) VALUES (NEW.id);
    INSERT INTO artist_release_group_pending_update VALUES (NEW.id);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_upd_release_group() RETURNS trigger AS $$
BEGIN
    IF NEW.artist_credit != OLD.artist_credit THEN
        PERFORM dec_ref_count('artist_credit', OLD.artist_credit, 1);
        PERFORM inc_ref_count('artist_credit', NEW.artist_credit, 1);
    END IF;
    IF (
        NEW.name != OLD.name OR
        NEW.artist_credit != OLD.artist_credit OR
        NEW.type IS DISTINCT FROM OLD.type
     ) THEN
        INSERT INTO artist_release_group_pending_update VALUES (OLD.id);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_del_release_group() RETURNS trigger AS $$
BEGIN
    PERFORM dec_ref_count('artist_credit', OLD.artist_credit, 1);
    INSERT INTO artist_release_group_pending_update VALUES (OLD.id);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION b_upd_release_group_secondary_type_join() RETURNS trigger AS $$
BEGIN
    -- Like artist credits, rows in release_group_secondary_type_join
    -- are immutable. When updates need to be made for a particular
    -- release group, they're deleted and re-inserted.
    --
    -- A benefit of this is that we don't need UPDATE triggers to keep
    -- artist_release_group up-to-date.
    RAISE EXCEPTION 'Cannot update release_group_secondary_type_join';
END;
$$ LANGUAGE 'plpgsql';

-- Ensure attribute type allows free text if free text is added
CREATE OR REPLACE FUNCTION ensure_release_group_attribute_type_allows_text()
RETURNS trigger AS $$
  BEGIN
    IF NEW.release_group_attribute_text IS NOT NULL
        AND NOT EXISTS (
           SELECT TRUE FROM release_group_attribute_type
        WHERE release_group_attribute_type.id = NEW.release_group_attribute_type
        AND free_text
    )
    THEN
        RAISE EXCEPTION 'This attribute type can not contain free text';
    ELSE RETURN NEW;
    END IF;
  END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- series triggers
-----------------------------------------------------------------------

-- Ensure attribute type allows free text if free text is added
CREATE OR REPLACE FUNCTION ensure_series_attribute_type_allows_text()
RETURNS trigger AS $$
BEGIN
    IF NEW.series_attribute_text IS NOT NULL
        AND NOT EXISTS (
            SELECT TRUE
              FROM series_attribute_type
             WHERE series_attribute_type.id = NEW.series_attribute_type
               AND free_text
    )
    THEN
        RAISE EXCEPTION 'This attribute type can not contain free text';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- track triggers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION a_ins_track() RETURNS trigger AS $$
BEGIN
    PERFORM inc_ref_count('artist_credit', NEW.artist_credit, 1);
    -- increment track_count in the parent medium
    UPDATE medium SET track_count = track_count + 1 WHERE id = NEW.medium;
    PERFORM materialise_recording_length(NEW.recording);
    PERFORM set_recordings_first_release_dates(ARRAY[NEW.recording]);
    INSERT INTO artist_release_pending_update (
        SELECT release FROM medium
        WHERE id = NEW.medium
    );
    INSERT INTO artist_release_group_pending_update (
        SELECT release_group FROM release
        JOIN medium ON medium.release = release.id
        WHERE medium.id = NEW.medium
    );
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_upd_track() RETURNS trigger AS $$
BEGIN
    IF NEW.artist_credit != OLD.artist_credit THEN
        PERFORM dec_ref_count('artist_credit', OLD.artist_credit, 1);
        PERFORM inc_ref_count('artist_credit', NEW.artist_credit, 1);
        INSERT INTO artist_release_pending_update (
            SELECT release FROM medium
            WHERE id = OLD.medium
        );
        INSERT INTO artist_release_group_pending_update (
            SELECT release_group FROM release
            JOIN medium ON medium.release = release.id
            WHERE medium.id = OLD.medium
        );
    END IF;
    IF NEW.medium != OLD.medium THEN
        IF (
            SELECT count(DISTINCT release)
              FROM medium
             WHERE id IN (NEW.medium, OLD.medium)
        ) = 2
        THEN
            -- I don't believe this code path should ever be hit.
            -- We have no functionality to move tracks between
            -- mediums. If this is ever allowed, however, we should
            -- ensure that both old and new mediums share the same
            -- release, otherwise we'd have to carefully handle this
            -- case when when updating materialized tables for
            -- recordings' first release dates and artists' release
            -- groups. -mwiencek, 2021-03-14
            RAISE EXCEPTION 'Cannot move a track between releases';
        END IF;

        -- medium is changed, decrement track_count in the original medium, increment in the new one
        UPDATE medium SET track_count = track_count - 1 WHERE id = OLD.medium;
        UPDATE medium SET track_count = track_count + 1 WHERE id = NEW.medium;
    END IF;
    IF OLD.recording <> NEW.recording THEN
      PERFORM materialise_recording_length(OLD.recording);
      PERFORM set_recordings_first_release_dates(ARRAY[OLD.recording, NEW.recording]);
    END IF;
    PERFORM materialise_recording_length(NEW.recording);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_del_track() RETURNS trigger AS $$
BEGIN
    PERFORM dec_ref_count('artist_credit', OLD.artist_credit, 1);
    -- decrement track_count in the parent medium
    UPDATE medium SET track_count = track_count - 1 WHERE id = OLD.medium;
    PERFORM materialise_recording_length(OLD.recording);
    PERFORM set_recordings_first_release_dates(ARRAY[OLD.recording]);
    INSERT INTO artist_release_pending_update (
        SELECT release FROM medium
        WHERE id = OLD.medium
    );
    INSERT INTO artist_release_group_pending_update (
        SELECT release_group FROM release
        JOIN medium ON medium.release = release.id
        WHERE medium.id = OLD.medium
    );
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- work triggers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION a_ins_work() RETURNS trigger AS $$
BEGIN
    INSERT INTO work_meta (id) VALUES (NEW.id);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

-- Ensure attribute type allows free text if free text is added
CREATE OR REPLACE FUNCTION ensure_work_attribute_type_allows_text()
RETURNS trigger AS $$
BEGIN
    IF NEW.work_attribute_text IS NOT NULL
        AND NOT EXISTS (
            SELECT TRUE FROM work_attribute_type
             WHERE work_attribute_type.id = NEW.work_attribute_type
               AND free_text
    )
    THEN
        RAISE EXCEPTION 'This attribute type can not contain free text';
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- alternative tracklist triggers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION inc_nullable_artist_credit(row_id integer) RETURNS void AS $$
BEGIN
    IF row_id IS NOT NULL THEN
        PERFORM inc_ref_count('artist_credit', row_id, 1);
    END IF;
    RETURN;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION dec_nullable_artist_credit(row_id integer) RETURNS void AS $$
BEGIN
    IF row_id IS NOT NULL THEN
        PERFORM dec_ref_count('artist_credit', row_id, 1);
    END IF;
    RETURN;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_ins_alternative_release_or_track() RETURNS trigger AS $$
BEGIN
    PERFORM inc_nullable_artist_credit(NEW.artist_credit);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_upd_alternative_release_or_track() RETURNS trigger AS $$
BEGIN
    IF NEW.artist_credit IS DISTINCT FROM OLD.artist_credit THEN
        PERFORM inc_nullable_artist_credit(NEW.artist_credit);
        PERFORM dec_nullable_artist_credit(OLD.artist_credit);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_del_alternative_release_or_track() RETURNS trigger AS $$
BEGIN
    PERFORM dec_nullable_artist_credit(OLD.artist_credit);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_ins_alternative_medium_track() RETURNS trigger AS $$
BEGIN
    PERFORM inc_ref_count('alternative_track', NEW.alternative_track, 1);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_upd_alternative_medium_track() RETURNS trigger AS $$
BEGIN
    IF NEW.alternative_track IS DISTINCT FROM OLD.alternative_track THEN
        PERFORM inc_ref_count('alternative_track', NEW.alternative_track, 1);
        PERFORM dec_ref_count('alternative_track', OLD.alternative_track, 1);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_del_alternative_medium_track() RETURNS trigger AS $$
BEGIN
    PERFORM dec_ref_count('alternative_track', OLD.alternative_track, 1);
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- lastupdate triggers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION b_upd_last_updated_table() RETURNS trigger AS $$
BEGIN
    NEW.last_updated = NOW();
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_upd_edit() RETURNS trigger AS $$
BEGIN
    IF NEW.status != OLD.status THEN
       UPDATE edit_artist SET status = NEW.status WHERE edit = NEW.id;
       UPDATE edit_label  SET status = NEW.status WHERE edit = NEW.id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION b_ins_edit_materialize_status() RETURNS trigger AS $$
BEGIN
    NEW.status = (SELECT status FROM edit WHERE id = NEW.edit);
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

------------------------
-- Collection deletion and hiding triggers
------------------------

CREATE OR REPLACE FUNCTION replace_old_sub_on_add()
RETURNS trigger AS $$
  BEGIN
    UPDATE editor_subscribe_collection
     SET available = TRUE, last_seen_name = NULL,
      last_edit_sent = NEW.last_edit_sent
     WHERE editor = NEW.editor AND collection = NEW.collection;

    IF FOUND THEN
      RETURN NULL;
    ELSE
      RETURN NEW;
    END IF;
  END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION del_collection_sub_on_delete()
RETURNS trigger AS $$
  BEGIN
    UPDATE editor_subscribe_collection sub
     SET available = FALSE, last_seen_name = OLD.name
     FROM editor_collection coll
     WHERE sub.collection = OLD.id AND sub.collection = coll.id;

    RETURN OLD;
  END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION del_collection_sub_on_private()
RETURNS trigger AS $$
  BEGIN
    IF NEW.public = FALSE AND OLD.public = TRUE THEN
      UPDATE editor_subscribe_collection sub
         SET available = FALSE,
             last_seen_name = OLD.name
       WHERE sub.collection = OLD.id
         AND sub.editor != NEW.editor
         AND sub.editor NOT IN (SELECT ecc.editor
                                  FROM editor_collection_collaborator ecc
                                 WHERE ecc.collection = sub.collection);
    END IF;

    RETURN NEW;
  END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION restore_collection_sub_on_public()
RETURNS trigger AS $$
  BEGIN
    IF NEW.public = TRUE AND OLD.public = FALSE THEN
      UPDATE editor_subscribe_collection sub
         SET available = TRUE,
             last_seen_name = NEW.name
       WHERE sub.collection = OLD.id
         AND sub.available = FALSE;
    END IF;

    RETURN NULL;
  END;
$$ LANGUAGE 'plpgsql';

------------------------
-- CD Lookup
------------------------

CREATE OR REPLACE FUNCTION create_cube_from_durations(durations INTEGER[]) RETURNS cube AS $$
DECLARE
    point    cube;
    str      VARCHAR;
    i        INTEGER;
    count    INTEGER;
    dest     INTEGER;
    dim      CONSTANT INTEGER = 6;
    selected INTEGER[];
BEGIN

    count = array_upper(durations, 1);
    FOR i IN 0..dim LOOP
        selected[i] = 0;
    END LOOP;

    IF count < dim THEN
        FOR i IN 1..count LOOP
            selected[i] = durations[i];
        END LOOP;
    ELSE
        FOR i IN 1..count LOOP
            dest = (dim * (i-1) / count) + 1;
            selected[dest] = selected[dest] + durations[i];
        END LOOP;
    END IF;

    str = '(';
    FOR i IN 1..dim LOOP
        IF i > 1 THEN
            str = str || ',';
        END IF;
        str = str || cast(selected[i] as text);
    END LOOP;
    str = str || ')';

    RETURN str::cube;
END;
$$ LANGUAGE 'plpgsql' IMMUTABLE;

CREATE OR REPLACE FUNCTION create_bounding_cube(durations INTEGER[], fuzzy INTEGER) RETURNS cube AS $$
DECLARE
    point    cube;
    str      VARCHAR;
    i        INTEGER;
    dest     INTEGER;
    count    INTEGER;
    dim      CONSTANT INTEGER = 6;
    selected INTEGER[];
    scalers  INTEGER[];
BEGIN

    count = array_upper(durations, 1);
    IF count < dim THEN
        FOR i IN 1..dim LOOP
            selected[i] = 0;
            scalers[i] = 0;
        END LOOP;
        FOR i IN 1..count LOOP
            selected[i] = durations[i];
            scalers[i] = 1;
        END LOOP;
    ELSE
        FOR i IN 1..dim LOOP
            selected[i] = 0;
            scalers[i] = 0;
        END LOOP;
        FOR i IN 1..count LOOP
            dest = (dim * (i-1) / count) + 1;
            selected[dest] = selected[dest] + durations[i];
            scalers[dest] = scalers[dest] + 1;
        END LOOP;
    END IF;

    str = '(';
    FOR i IN 1..dim LOOP
        IF i > 1 THEN
            str = str || ',';
        END IF;
        str = str || cast((selected[i] - (fuzzy * scalers[i])) as text);
    END LOOP;
    str = str || '),(';
    FOR i IN 1..dim LOOP
        IF i > 1 THEN
            str = str || ',';
        END IF;
        str = str || cast((selected[i] + (fuzzy * scalers[i])) as text);
    END LOOP;
    str = str || ')';

    RETURN str::cube;
END;
$$ LANGUAGE 'plpgsql' IMMUTABLE;

-------------------------------------------------------------------
-- Maintain musicbrainz.release_first_release_date
-------------------------------------------------------------------
CREATE OR REPLACE FUNCTION get_release_first_release_date_rows(condition TEXT)
RETURNS SETOF release_first_release_date AS $$
BEGIN
    RETURN QUERY EXECUTE '
        SELECT DISTINCT ON (release) release,
            date_year AS year,
            date_month AS month,
            date_day AS day
        FROM (
            SELECT release, date_year, date_month, date_day FROM release_country
            WHERE (date_year IS NOT NULL OR date_month IS NOT NULL OR date_day IS NOT NULL)
            UNION ALL
            SELECT release, date_year, date_month, date_day FROM release_unknown_country
        ) all_dates
        WHERE ' || condition ||
        ' AND NOT EXISTS (
          SELECT TRUE
            FROM release
           WHERE release.id = all_dates.release
             AND status = 6
        )
        ORDER BY release, year NULLS LAST, month NULLS LAST, day NULLS LAST';
END;
$$ LANGUAGE 'plpgsql' STRICT;

CREATE OR REPLACE FUNCTION set_release_first_release_date(release_id INTEGER)
RETURNS VOID AS $$
BEGIN
  -- DO NOT modify any replicated tables in this function; it's used
  -- by a trigger on mirrors.
  DELETE FROM release_first_release_date
  WHERE release = release_id;

  INSERT INTO release_first_release_date
  SELECT * FROM get_release_first_release_date_rows(
    format('release = %L', release_id)
  );

  INSERT INTO artist_release_pending_update VALUES (release_id);
END;
$$ LANGUAGE 'plpgsql' STRICT;

-------------------------------------------------------------------
-- Maintain release_group_meta.first_release_date
-------------------------------------------------------------------
CREATE OR REPLACE FUNCTION set_release_group_first_release_date(release_group_id INTEGER)
RETURNS VOID AS $$
BEGIN
    UPDATE release_group_meta SET first_release_date_year = first.year,
                                  first_release_date_month = first.month,
                                  first_release_date_day = first.day
      FROM (
        SELECT rd.year, rd.month, rd.day
        FROM release_group
        LEFT JOIN release ON release.release_group = release_group.id
        LEFT JOIN release_first_release_date rd ON (rd.release = release.id)
        WHERE release_group.id = release_group_id
        ORDER BY
          rd.year NULLS LAST,
          rd.month NULLS LAST,
          rd.day NULLS LAST
        LIMIT 1
      ) AS first
    WHERE id = release_group_id;
    INSERT INTO artist_release_group_pending_update VALUES (release_group_id);
END;
$$ LANGUAGE 'plpgsql';

-------------------------------------------------------------------
-- Maintain musicbrainz.recording_first_release_date
-------------------------------------------------------------------
CREATE OR REPLACE FUNCTION get_recording_first_release_date_rows(condition TEXT)
RETURNS SETOF recording_first_release_date AS $$
BEGIN
    RETURN QUERY EXECUTE '
        SELECT DISTINCT ON (track.recording)
            track.recording, rd.year, rd.month, rd.day
        FROM track
        JOIN medium ON medium.id = track.medium
        JOIN release_first_release_date rd ON rd.release = medium.release
        WHERE ' || condition || '
        ORDER BY track.recording,
            rd.year NULLS LAST,
            rd.month NULLS LAST,
            rd.day NULLS LAST';
END;
$$ LANGUAGE 'plpgsql' STRICT;

CREATE OR REPLACE FUNCTION set_recordings_first_release_dates(recording_ids INTEGER[])
RETURNS VOID AS $$
BEGIN
  -- DO NOT modify any replicated tables in this function; it's used
  -- by a trigger on mirrors.
  DELETE FROM recording_first_release_date
  WHERE recording = ANY(recording_ids);

  INSERT INTO recording_first_release_date
  SELECT * FROM get_recording_first_release_date_rows(
    format('track.recording = any(%L)', recording_ids)
  );
END;
$$ LANGUAGE 'plpgsql' STRICT;

CREATE OR REPLACE FUNCTION set_mediums_recordings_first_release_dates(medium_ids INTEGER[])
RETURNS VOID AS $$
BEGIN
  PERFORM set_recordings_first_release_dates((
    SELECT array_agg(recording)
      FROM track
     WHERE track.medium = any(medium_ids)
  ));
  RETURN;
END;
$$ LANGUAGE 'plpgsql' STRICT;

CREATE OR REPLACE FUNCTION set_releases_recordings_first_release_dates(release_ids INTEGER[])
RETURNS VOID AS $$
BEGIN
  PERFORM set_recordings_first_release_dates((
    SELECT array_agg(recording)
      FROM track
      JOIN medium ON medium.id = track.medium
     WHERE medium.release = any(release_ids)
  ));
  RETURN;
END;
$$ LANGUAGE 'plpgsql' STRICT;

CREATE OR REPLACE FUNCTION a_upd_medium_mirror()
RETURNS trigger AS $$
BEGIN
    -- DO NOT modify any replicated tables in this function; it's used
    -- by a trigger on mirrors.
    IF NEW.release IS DISTINCT FROM OLD.release THEN
        PERFORM set_mediums_recordings_first_release_dates(ARRAY[OLD.id]);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_ins_release_event()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM set_release_first_release_date(NEW.release);

  PERFORM set_release_group_first_release_date(release_group)
  FROM release
  WHERE release.id = NEW.release;

  PERFORM set_releases_recordings_first_release_dates(ARRAY[NEW.release]);

  IF TG_TABLE_NAME = 'release_country' THEN
    INSERT INTO artist_release_pending_update VALUES (NEW.release);
  END IF;

  RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_upd_release_event()
RETURNS TRIGGER AS $$
BEGIN
  IF (
    NEW.release != OLD.release OR
    NEW.date_year IS DISTINCT FROM OLD.date_year OR
    NEW.date_month IS DISTINCT FROM OLD.date_month OR
    NEW.date_day IS DISTINCT FROM OLD.date_day
  ) THEN
    PERFORM set_release_first_release_date(OLD.release);
    IF NEW.release != OLD.release THEN
        PERFORM set_release_first_release_date(NEW.release);
    END IF;

    PERFORM set_release_group_first_release_date(release_group)
    FROM release
    WHERE release.id IN (NEW.release, OLD.release);

    PERFORM set_releases_recordings_first_release_dates(ARRAY[NEW.release, OLD.release]);
  END IF;

  IF TG_TABLE_NAME = 'release_country' THEN
    IF NEW.country != OLD.country THEN
      INSERT INTO artist_release_pending_update VALUES (OLD.release);
    END IF;
  END IF;

  RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION a_del_release_event()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM set_release_first_release_date(OLD.release);

  PERFORM set_release_group_first_release_date(release_group)
  FROM release
  WHERE release.id = OLD.release;

  PERFORM set_releases_recordings_first_release_dates(ARRAY[OLD.release]);

  IF TG_TABLE_NAME = 'release_country' THEN
    INSERT INTO artist_release_pending_update VALUES (OLD.release);
  END IF;

  RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION deny_special_purpose_deletion() RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'Attempted to delete a special purpose row';
END;
$$ LANGUAGE 'plpgsql';

-------------------------------------------------------------------
-- Ratings
-------------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_aggregate_rating(entity_type ratable_entity_type, entity_id INTEGER)
RETURNS VOID AS $$
BEGIN
  -- update the aggregate rating for the given entity_id.
  EXECUTE format(
    $SQL$
      UPDATE %2$I
         SET rating = agg.rating,
             rating_count = nullif(agg.rating_count, 0)
        FROM (
          SELECT count(rating)::INTEGER AS rating_count,
                 -- trunc(x + 0.5) is used because round() on REAL values
                 -- rounds to the nearest even number.
                 trunc((sum(rating)::REAL /
                        count(rating)::REAL) +
                       0.5::REAL)::SMALLINT AS rating
            FROM %3$I
           WHERE %1$I = $1
        ) agg
       WHERE id = $1
    $SQL$,
    entity_type::TEXT,
    entity_type::TEXT || '_meta',
    entity_type::TEXT || '_rating_raw'
  ) USING entity_id;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION update_aggregate_rating_for_raw_insert()
RETURNS trigger AS $$
DECLARE
  entity_type ratable_entity_type;
  new_entity_id INTEGER;
BEGIN
  entity_type := TG_ARGV[0]::ratable_entity_type;
  EXECUTE format('SELECT ($1).%s', entity_type::TEXT) INTO new_entity_id USING NEW;
  PERFORM update_aggregate_rating(entity_type, new_entity_id);
  RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION update_aggregate_rating_for_raw_update()
RETURNS trigger AS $$
DECLARE
  entity_type ratable_entity_type;
  new_entity_id INTEGER;
  old_entity_id INTEGER;
BEGIN
  entity_type := TG_ARGV[0]::ratable_entity_type;
  EXECUTE format('SELECT ($1).%s', entity_type) INTO new_entity_id USING NEW;
  EXECUTE format('SELECT ($1).%s', entity_type) INTO old_entity_id USING OLD;
  IF (old_entity_id = new_entity_id AND OLD.rating != NEW.rating) THEN
    -- Case 1: only the rating changed.
    PERFORM update_aggregate_rating(entity_type, old_entity_id);
  ELSIF (old_entity_id != new_entity_id OR OLD.rating != NEW.rating) THEN
    -- Case 2: the entity or rating changed.
    PERFORM update_aggregate_rating(entity_type, old_entity_id);
    PERFORM update_aggregate_rating(entity_type, new_entity_id);
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION update_aggregate_rating_for_raw_delete()
RETURNS trigger AS $$
DECLARE
  entity_type ratable_entity_type;
  old_entity_id INTEGER;
BEGIN
  entity_type := TG_ARGV[0]::ratable_entity_type;
  EXECUTE format('SELECT ($1).%s', entity_type::TEXT) INTO old_entity_id USING OLD;
  PERFORM update_aggregate_rating(entity_type, old_entity_id);
  RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION delete_ratings(enttype TEXT, ids INTEGER[])
RETURNS TABLE(editor INT, rating SMALLINT) AS $$
DECLARE
    tablename TEXT;
BEGIN
    tablename = enttype || '_rating_raw';
    RETURN QUERY
       EXECUTE 'DELETE FROM ' || tablename || ' WHERE ' || enttype || ' = any($1)
                RETURNING editor, rating'
         USING ids;
    RETURN;
END;
$$ LANGUAGE 'plpgsql';

-------------------------------------------------------------------
-- Prevent link attributes being used on links that don't support them
-------------------------------------------------------------------
CREATE OR REPLACE FUNCTION prevent_invalid_attributes()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (
        SELECT TRUE
        FROM (VALUES (NEW.link, NEW.attribute_type)) la (link, attribute_type)
        JOIN link l ON l.id = la.link
        JOIN link_type lt ON l.link_type = lt.id
        JOIN link_attribute_type lat ON lat.id = la.attribute_type
        JOIN link_type_attribute_type ltat ON ltat.attribute_type = lat.root AND ltat.link_type = lt.id
    ) THEN
        RAISE EXCEPTION 'Attribute type % is invalid for link %', NEW.attribute_type, NEW.link;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

--------------------------------------------------------------------------------
-- Remove unused link rows when a relationship is changed
--------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION remove_unused_links()
RETURNS TRIGGER AS $$
DECLARE
    other_ars_exist BOOLEAN;
BEGIN
    EXECUTE 'SELECT EXISTS (SELECT TRUE FROM ' || quote_ident(TG_TABLE_NAME) ||
            ' WHERE link = $1)'
    INTO other_ars_exist
    USING OLD.link;

    IF NOT other_ars_exist THEN
       DELETE FROM link_attribute WHERE link = OLD.link;
       DELETE FROM link_attribute_credit WHERE link = OLD.link;
       DELETE FROM link_attribute_text_value WHERE link = OLD.link;
       DELETE FROM link WHERE id = OLD.link;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION delete_unused_url(ids INTEGER[])
RETURNS VOID AS $$
BEGIN
  DELETE FROM url_gid_redirect WHERE new_id = any(ids);
  DELETE FROM url WHERE id = any(ids);
EXCEPTION
  WHEN foreign_key_violation THEN RETURN;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION remove_unused_url()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_TABLE_NAME LIKE 'l_url_%' THEN
      EXECUTE delete_unused_url(ARRAY[OLD.entity0]);
    END IF;

    IF TG_TABLE_NAME LIKE 'l_%_url' THEN
      EXECUTE delete_unused_url(ARRAY[OLD.entity1]);
    END IF;

    IF TG_TABLE_NAME LIKE 'url' THEN
      EXECUTE delete_unused_url(ARRAY[OLD.id, NEW.id]);
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION simplify_search_hints()
RETURNS trigger AS $$
BEGIN
    IF NEW.type::int = TG_ARGV[0]::int THEN
        NEW.sort_name := NEW.name;
        NEW.begin_date_year := NULL;
        NEW.begin_date_month := NULL;
        NEW.begin_date_day := NULL;
        NEW.end_date_year := NULL;
        NEW.end_date_month := NULL;
        NEW.end_date_day := NULL;
        NEW.end_date_day := NULL;
        NEW.ended := FALSE;
        NEW.locale := NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION end_date_implies_ended()
RETURNS trigger AS $$
BEGIN
    IF NEW.end_date_year IS NOT NULL OR
       NEW.end_date_month IS NOT NULL OR
       NEW.end_date_day IS NOT NULL
    THEN
        NEW.ended = TRUE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION end_area_implies_ended()
RETURNS trigger AS $$
BEGIN
    IF NEW.end_area IS NOT NULL
    THEN
        NEW.ended = TRUE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION delete_orphaned_recordings()
RETURNS TRIGGER
AS $$
  BEGIN
    PERFORM TRUE
    FROM recording outer_r
    WHERE id = OLD.recording
      AND edits_pending = 0
      AND NOT EXISTS (
        SELECT TRUE
        FROM edit JOIN edit_recording er ON edit.id = er.edit
        WHERE er.recording = outer_r.id
          AND type IN (71, 207, 218)
          LIMIT 1
      ) AND NOT EXISTS (
        SELECT TRUE FROM track WHERE track.recording = outer_r.id LIMIT 1
      ) AND NOT EXISTS (
        SELECT TRUE FROM l_area_recording WHERE entity1 = outer_r.id
          UNION ALL
        SELECT TRUE FROM l_artist_recording WHERE entity1 = outer_r.id
          UNION ALL
        SELECT TRUE FROM l_event_recording WHERE entity1 = outer_r.id
          UNION ALL
        SELECT TRUE FROM l_instrument_recording WHERE entity1 = outer_r.id
          UNION ALL
        SELECT TRUE FROM l_label_recording WHERE entity1 = outer_r.id
          UNION ALL
        SELECT TRUE FROM l_place_recording WHERE entity1 = outer_r.id
          UNION ALL
        SELECT TRUE FROM l_recording_recording WHERE entity1 = outer_r.id OR entity0 = outer_r.id
          UNION ALL
        SELECT TRUE FROM l_recording_release WHERE entity0 = outer_r.id
          UNION ALL
        SELECT TRUE FROM l_recording_release_group WHERE entity0 = outer_r.id
          UNION ALL
        SELECT TRUE FROM l_recording_series WHERE entity0 = outer_r.id
          UNION ALL
        SELECT TRUE FROM l_recording_work WHERE entity0 = outer_r.id
          UNION ALL
         SELECT TRUE FROM l_recording_url WHERE entity0 = outer_r.id
      );

    IF FOUND THEN
      -- Remove references from tables that don't change whether or not this recording
      -- is orphaned.
      DELETE FROM isrc WHERE recording = OLD.recording;
      DELETE FROM recording_alias WHERE recording = OLD.recording;
      DELETE FROM recording_annotation WHERE recording = OLD.recording;
      DELETE FROM recording_gid_redirect WHERE new_id = OLD.recording;
      DELETE FROM recording_rating_raw WHERE recording = OLD.recording;
      DELETE FROM recording_tag WHERE recording = OLD.recording;
      DELETE FROM recording_tag_raw WHERE recording = OLD.recording;
      DELETE FROM editor_collection_recording WHERE recording = OLD.recording;

      DELETE FROM recording WHERE id = OLD.recording;
    END IF;

    RETURN NULL;
  END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION padded_by_whitespace(TEXT) RETURNS boolean AS $$
  SELECT btrim($1) <> $1;
$$ LANGUAGE SQL IMMUTABLE;

CREATE OR REPLACE FUNCTION controlled_for_whitespace(TEXT) RETURNS boolean AS $$
  SELECT NOT padded_by_whitespace($1);
$$ LANGUAGE SQL IMMUTABLE SET search_path = musicbrainz, public;

CREATE OR REPLACE FUNCTION update_aggregate_tag_count(entity_type taggable_entity_type, entity_id INTEGER, tag_id INTEGER, count_change SMALLINT)
RETURNS VOID AS $$
BEGIN
  -- Insert-or-update the aggregate vote count for the given (entity_id, tag_id).
  EXECUTE format(
    $SQL$
      INSERT INTO %1$I AS agg (%2$I, tag, count)
           VALUES ($1, $2, $3)
      ON CONFLICT (%2$I, tag) DO UPDATE SET count = agg.count + $3
    $SQL$,
    entity_type::TEXT || '_tag',
    entity_type::TEXT
  ) USING entity_id, tag_id, count_change;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION delete_unused_aggregate_tag(entity_type taggable_entity_type, entity_id INTEGER, tag_id INTEGER)
RETURNS VOID AS $$
BEGIN
  -- Delete the aggregate tag row for (entity_id, tag_id) if no raw tag pair
  -- exists for the same.
  --
  -- Note that an aggregate vote count of 0 doesn't imply there are no raw
  -- tags; it's a sum of all the votes, so it can also mean that there's a
  -- downvote for every upvote.
  EXECUTE format(
    $SQL$
      DELETE FROM %1$I
            WHERE %2$I = $1
              AND tag = $2
              AND NOT EXISTS (SELECT 1 FROM %3$I WHERE %2$I = $1 AND tag = $2)
    $SQL$,
    entity_type::TEXT || '_tag',
    entity_type::TEXT,
    entity_type::TEXT || '_tag_raw'
  ) USING entity_id, tag_id;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION update_tag_counts_for_raw_insert()
RETURNS trigger AS $$
DECLARE
  entity_type taggable_entity_type;
  new_entity_id INTEGER;
BEGIN
  entity_type := TG_ARGV[0]::taggable_entity_type;
  EXECUTE format('SELECT ($1).%s', entity_type::TEXT) INTO new_entity_id USING NEW;
  PERFORM update_aggregate_tag_count(entity_type, new_entity_id, NEW.tag, (CASE WHEN NEW.is_upvote THEN 1 ELSE -1 END)::SMALLINT);
  UPDATE tag SET ref_count = ref_count + 1 WHERE id = NEW.tag;
  RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION update_tag_counts_for_raw_update()
RETURNS trigger AS $$
DECLARE
  entity_type taggable_entity_type;
  new_entity_id INTEGER;
  old_entity_id INTEGER;
BEGIN
  entity_type := TG_ARGV[0]::taggable_entity_type;
  EXECUTE format('SELECT ($1).%s', entity_type) INTO new_entity_id USING NEW;
  EXECUTE format('SELECT ($1).%s', entity_type) INTO old_entity_id USING OLD;
  IF (old_entity_id = new_entity_id AND OLD.tag = NEW.tag AND OLD.is_upvote != NEW.is_upvote) THEN
    -- Case 1: only the vote changed.
    PERFORM update_aggregate_tag_count(entity_type, old_entity_id, OLD.tag, (CASE WHEN OLD.is_upvote THEN -2 ELSE 2 END)::SMALLINT);
  ELSIF (old_entity_id != new_entity_id OR OLD.tag != NEW.tag OR OLD.is_upvote != NEW.is_upvote) THEN
    -- Case 2: the entity, tag, or vote changed.
    PERFORM update_aggregate_tag_count(entity_type, old_entity_id, OLD.tag, (CASE WHEN OLD.is_upvote THEN -1 ELSE 1 END)::SMALLINT);
    PERFORM update_aggregate_tag_count(entity_type, new_entity_id, NEW.tag, (CASE WHEN NEW.is_upvote THEN 1 ELSE -1 END)::SMALLINT);
    PERFORM delete_unused_aggregate_tag(entity_type, old_entity_id, OLD.tag);
  END IF;
  IF OLD.tag != NEW.tag THEN
    UPDATE tag SET ref_count = ref_count - 1 WHERE id = OLD.tag;
    UPDATE tag SET ref_count = ref_count + 1 WHERE id = NEW.tag;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION update_tag_counts_for_raw_delete()
RETURNS trigger AS $$
DECLARE
  entity_type taggable_entity_type;
  old_entity_id INTEGER;
BEGIN
  entity_type := TG_ARGV[0]::taggable_entity_type;
  EXECUTE format('SELECT ($1).%s', entity_type::TEXT) INTO old_entity_id USING OLD;
  PERFORM update_aggregate_tag_count(entity_type, old_entity_id, OLD.tag, (CASE WHEN OLD.is_upvote THEN -1 ELSE 1 END)::SMALLINT);
  PERFORM delete_unused_aggregate_tag(entity_type, old_entity_id, OLD.tag);
  UPDATE tag SET ref_count = ref_count - 1 WHERE id = OLD.tag;
  RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION delete_unused_tag(tag_id INT)
RETURNS void AS $$
  BEGIN
    DELETE FROM tag WHERE id = tag_id;
  EXCEPTION
    WHEN foreign_key_violation THEN RETURN;
  END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION trg_delete_unused_tag()
RETURNS trigger AS $$
  BEGIN
    PERFORM delete_unused_tag(NEW.id);
    RETURN NULL;
  END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION trg_delete_unused_tag_ref()
RETURNS trigger AS $$
  BEGIN
    PERFORM delete_unused_tag(OLD.tag);
    RETURN NULL;
  END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION inserting_edits_requires_confirmed_email_address()
RETURNS trigger AS $$
BEGIN
  IF NOT (
    SELECT email_confirm_date IS NOT NULL AND email_confirm_date <= now()
    FROM editor
    WHERE editor.id = NEW.editor
  ) THEN
    RAISE EXCEPTION 'Editor tried to create edit without a confirmed email address';
  ELSE
    RETURN NEW;
  END IF;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION deny_deprecated_links()
RETURNS trigger AS $$
BEGIN
  IF (SELECT is_deprecated FROM link_type WHERE id = NEW.link_type)
  THEN
    RAISE EXCEPTION 'Attempt to create a relationship with a deprecated type';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION check_has_dates()
RETURNS trigger AS $$
BEGIN
    IF (NEW.begin_date_year IS NOT NULL OR
       NEW.begin_date_month IS NOT NULL OR
       NEW.begin_date_day IS NOT NULL OR
       NEW.end_date_year IS NOT NULL OR
       NEW.end_date_month IS NOT NULL OR
       NEW.end_date_day IS NOT NULL OR
       NEW.ended = TRUE)
       AND NOT (SELECT has_dates FROM link_type WHERE id = NEW.link_type)
  THEN
    RAISE EXCEPTION 'Attempt to add dates to a relationship type that does not support dates.';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION materialise_recording_length(recording_id INT)
RETURNS void as $$
BEGIN
  UPDATE recording SET length = median
   FROM (SELECT median_track_length(recording_id) median) track
  WHERE recording.id = recording_id
    AND recording.length IS DISTINCT FROM track.median;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION track_count_matches_cdtoc(medium, int) RETURNS boolean AS $$
    SELECT $1.track_count = $2 + COALESCE(
        (SELECT count(*) FROM track
         WHERE medium = $1.id AND (position = 0 OR is_data_track = true)
    ), 0);
$$ LANGUAGE SQL IMMUTABLE;

COMMIT;

-----------------------------------------------------------------------
-- edit_note triggers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION a_ins_edit_note() RETURNS trigger AS $$
BEGIN
    INSERT INTO edit_note_recipient (recipient, edit_note) (
        SELECT edit.editor, NEW.id
          FROM edit
         WHERE edit.id = NEW.edit
           AND edit.editor != NEW.editor
    );
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- Text search helpers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION mb_lower(input text) RETURNS text AS $$
  SELECT lower(input COLLATE musicbrainz.musicbrainz);
$$ LANGUAGE SQL IMMUTABLE PARALLEL SAFE STRICT;

CREATE OR REPLACE FUNCTION mb_simple_tsvector(input text) RETURNS tsvector AS $$
  -- The builtin 'simple' dictionary, which the mb_simple text search
  -- configuration makes use of, would normally lowercase the input string
  -- for us, but internally it hardcodes DEFAULT_COLLATION_OID; therefore
  -- we first lowercase the input string ourselves using mb_lower.
  SELECT to_tsvector('musicbrainz.mb_simple', musicbrainz.mb_lower(input));
$$ LANGUAGE SQL IMMUTABLE PARALLEL SAFE STRICT;

-----------------------------------------------------------------------
-- Edit data helpers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION edit_data_type_info(data JSONB) RETURNS TEXT AS $$
BEGIN
    CASE jsonb_typeof(data)
    WHEN 'object' THEN
        RETURN '{' ||
            (SELECT string_agg(
                to_json(key) || ':' ||
                edit_data_type_info(jsonb_extract_path(data, key)),
                ',' ORDER BY key)
               FROM jsonb_object_keys(data) AS key) ||
            '}';
    WHEN 'array' THEN
        RETURN '[' ||
            (SELECT string_agg(
                DISTINCT edit_data_type_info(item),
                ',' ORDER BY edit_data_type_info(item))
               FROM jsonb_array_elements(data) AS item) ||
            ']';
    WHEN 'string' THEN
        RETURN '1';
    WHEN 'number' THEN
        RETURN '2';
    WHEN 'boolean' THEN
        RETURN '4';
    WHEN 'null' THEN
        RETURN '8';
    END CASE;
    RETURN '';
END;
$$ LANGUAGE plpgsql IMMUTABLE PARALLEL SAFE STRICT;

-----------------------------------------------------------------------
-- Maintain musicbrainz.artist_release
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_artist_release_rows(
    release_id INTEGER
) RETURNS SETOF artist_release AS $$
BEGIN
    -- PostgreSQL 12 generates a vastly more efficient plan when only
    -- one release ID is passed. A condition like `r.id = any(...)`
    -- can be over 200x slower, even with only one release ID in the
    -- array.
    RETURN QUERY EXECUTE $SQL$
        SELECT DISTINCT ON (ar.artist, r.id)
            ar.is_track_artist,
            ar.artist,
            integer_date(rfrd.year, rfrd.month, rfrd.day) AS first_release_date,
            array_agg(
                DISTINCT rl.catalog_number ORDER BY rl.catalog_number
            ) FILTER (WHERE rl.catalog_number IS NOT NULL)::TEXT[] AS catalog_numbers,
            min(iso.code ORDER BY iso.code)::CHAR(2) AS country_code,
            left(regexp_replace(
                (CASE r.barcode WHEN '' THEN '0' ELSE r.barcode END),
                '[^0-9]+', '', 'g'
            ), 18)::BIGINT AS barcode,
            r.name,
            r.id
        FROM (
            SELECT FALSE AS is_track_artist, racn.artist, r.id AS release
            FROM release r
            JOIN artist_credit_name racn ON racn.artist_credit = r.artist_credit
            UNION ALL
            SELECT TRUE AS is_track_artist, tacn.artist, m.release
            FROM medium m
            JOIN track t ON t.medium = m.id
            JOIN artist_credit_name tacn ON tacn.artist_credit = t.artist_credit
        ) ar
        JOIN release r ON r.id = ar.release
        LEFT JOIN release_first_release_date rfrd ON rfrd.release = r.id
        LEFT JOIN release_label rl ON rl.release = r.id
        LEFT JOIN release_country rc ON rc.release = r.id
        LEFT JOIN iso_3166_1 iso ON iso.area = rc.country
    $SQL$ || (CASE WHEN release_id IS NULL THEN '' ELSE 'WHERE r.id = $1' END) ||
    $SQL$
        GROUP BY ar.is_track_artist, ar.artist, rfrd.release, r.id
        ORDER BY ar.artist, r.id, ar.is_track_artist
    $SQL$
    USING release_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION apply_artist_release_pending_updates()
RETURNS trigger AS $$
DECLARE
    release_ids INTEGER[];
    release_id INTEGER;
BEGIN
    -- DO NOT modify any replicated tables in this function; it's used
    -- by a trigger on mirrors.
    WITH pending AS (
        DELETE FROM artist_release_pending_update
        RETURNING release
    )
    SELECT array_agg(DISTINCT release)
    INTO release_ids
    FROM pending;

    IF coalesce(array_length(release_ids, 1), 0) > 0 THEN
        -- If the user hasn't generated `artist_release`, then we
        -- shouldn't update or insert to it. MBS determines whether to
        -- use this table based on it being non-empty, so a partial
        -- table would manifest as partial data on the website and
        -- webservice.
        PERFORM 1 FROM artist_release LIMIT 1;
        IF FOUND THEN
            DELETE FROM artist_release WHERE release = any(release_ids);

            FOREACH release_id IN ARRAY release_ids LOOP
                -- We handle each release ID separately because the
                -- `get_artist_release_rows` query can be planned much
                -- more efficiently that way.
                INSERT INTO artist_release
                SELECT * FROM get_artist_release_rows(release_id);
            END LOOP;
        END IF;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- Maintain musicbrainz.artist_release_group
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_artist_release_group_rows(
    release_group_id INTEGER
) RETURNS SETOF artist_release_group AS $$
BEGIN
    -- PostgreSQL 12 generates a vastly more efficient plan when only
    -- one release group ID is passed. A condition like
    -- `rg.id = any(...)` can be over 200x slower, even with only one
    -- release group ID in the array.
    RETURN QUERY EXECUTE $SQL$
        SELECT DISTINCT ON (a_rg.artist, rg.id)
            a_rg.is_track_artist,
            a_rg.artist,
            -- Withdrawn releases were once official by definition
            bool_and(r.status IS NOT NULL AND r.status != 1 AND r.status != 5),
            rgpt.child_order::SMALLINT,
            rg.type::SMALLINT,
            array_agg(
                DISTINCT rgst.child_order ORDER BY rgst.child_order)
                FILTER (WHERE rgst.child_order IS NOT NULL
            )::SMALLINT[],
            array_agg(
                DISTINCT st.secondary_type ORDER BY st.secondary_type)
                FILTER (WHERE st.secondary_type IS NOT NULL
            )::SMALLINT[],
            integer_date(
                rgm.first_release_date_year,
                rgm.first_release_date_month,
                rgm.first_release_date_day
            ),
            rg.name,
            rg.id
        FROM (
            SELECT FALSE AS is_track_artist, rgacn.artist, rg.id AS release_group
            FROM release_group rg
            JOIN artist_credit_name rgacn ON rgacn.artist_credit = rg.artist_credit
            UNION ALL
            SELECT TRUE AS is_track_artist, tacn.artist, r.release_group
            FROM release r
            JOIN medium m ON m.release = r.id
            JOIN track t ON t.medium = m.id
            JOIN artist_credit_name tacn ON tacn.artist_credit = t.artist_credit
        ) a_rg
        JOIN release_group rg ON rg.id = a_rg.release_group
        LEFT JOIN release r ON r.release_group = rg.id
        JOIN release_group_meta rgm ON rgm.id = rg.id
        LEFT JOIN release_group_primary_type rgpt ON rgpt.id = rg.type
        LEFT JOIN release_group_secondary_type_join st ON st.release_group = rg.id
        LEFT JOIN release_group_secondary_type rgst ON rgst.id = st.secondary_type
    $SQL$ || (CASE WHEN release_group_id IS NULL THEN '' ELSE 'WHERE rg.id = $1' END) ||
    $SQL$
        GROUP BY a_rg.is_track_artist, a_rg.artist, rgm.id, rg.id, rgpt.child_order
        ORDER BY a_rg.artist, rg.id, a_rg.is_track_artist
    $SQL$
    USING release_group_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION apply_artist_release_group_pending_updates()
RETURNS trigger AS $$
DECLARE
    release_group_ids INTEGER[];
    release_group_id INTEGER;
BEGIN
    -- DO NOT modify any replicated tables in this function; it's used
    -- by a trigger on mirrors.
    WITH pending AS (
        DELETE FROM artist_release_group_pending_update
        RETURNING release_group
    )
    SELECT array_agg(DISTINCT release_group)
    INTO release_group_ids
    FROM pending;

    IF coalesce(array_length(release_group_ids, 1), 0) > 0 THEN
        -- If the user hasn't generated `artist_release_group`, then we
        -- shouldn't update or insert to it. MBS determines whether to
        -- use this table based on it being non-empty, so a partial
        -- table would manifest as partial data on the website and
        -- webservice.
        PERFORM 1 FROM artist_release_group LIMIT 1;
        IF FOUND THEN
            DELETE FROM artist_release_group WHERE release_group = any(release_group_ids);

            FOREACH release_group_id IN ARRAY release_group_ids LOOP
                -- We handle each release group ID separately because
                -- the `get_artist_release_group_rows` query can be
                -- planned much more efficiently that way.
                INSERT INTO artist_release_group
                SELECT * FROM get_artist_release_group_rows(release_group_id);
            END LOOP;
        END IF;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- Relationship triggers
-----------------------------------------------------------------------

CREATE OR REPLACE FUNCTION a_ins_l_area_area_mirror() RETURNS trigger AS $$
DECLARE
    part_of_area_link_type_id CONSTANT SMALLINT := 356;
BEGIN
    -- DO NOT modify any replicated tables in this function; it's used
    -- by a trigger on mirrors.
    IF (SELECT link_type FROM link WHERE id = NEW.link) = part_of_area_link_type_id THEN
        PERFORM update_area_containment_mirror(ARRAY[NEW.entity0], ARRAY[NEW.entity1]);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION a_upd_l_area_area_mirror() RETURNS trigger AS $$
DECLARE
    part_of_area_link_type_id CONSTANT SMALLINT := 356;
    old_lt_id INTEGER;
    new_lt_id INTEGER;
BEGIN
    -- DO NOT modify any replicated tables in this function; it's used
    -- by a trigger on mirrors.
    SELECT link_type INTO old_lt_id FROM link WHERE id = OLD.link;
    SELECT link_type INTO new_lt_id FROM link WHERE id = NEW.link;
    IF (
        (
            old_lt_id = part_of_area_link_type_id AND
            new_lt_id = part_of_area_link_type_id AND
            (OLD.entity0 != NEW.entity0 OR OLD.entity1 != NEW.entity1)
        ) OR
        (old_lt_id = part_of_area_link_type_id) != (new_lt_id = part_of_area_link_type_id)
    ) THEN
        PERFORM update_area_containment_mirror(ARRAY[OLD.entity0, NEW.entity0], ARRAY[OLD.entity1, NEW.entity1]);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION a_del_l_area_area_mirror() RETURNS trigger AS $$
DECLARE
    part_of_area_link_type_id CONSTANT SMALLINT := 356;
BEGIN
    -- DO NOT modify any replicated tables in this function; it's used
    -- by a trigger on mirrors.
    IF (SELECT link_type FROM link WHERE id = OLD.link) = part_of_area_link_type_id THEN
        PERFORM update_area_containment_mirror(ARRAY[OLD.entity0], ARRAY[OLD.entity1]);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION b_upd_link() RETURNS trigger AS $$
BEGIN
    -- Like artist credits, links are shared across many entities
    -- (relationships) and so are immutable: they can only be inserted
    -- or deleted.
    --
    -- This helps ensure the data integrity of relationships and other
    -- materialized tables that rely on their immutability, like
    -- area_containment.
    RAISE EXCEPTION 'link rows are immutable';
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION b_upd_link_attribute() RETURNS trigger AS $$
BEGIN
    -- Refer to b_upd_link.
    RAISE EXCEPTION 'link_attribute rows are immutable';
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION b_upd_link_attribute_credit() RETURNS trigger AS $$
BEGIN
    -- Refer to b_upd_link.
    RAISE EXCEPTION 'link_attribute_credit rows are immutable';
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION b_upd_link_attribute_text_value() RETURNS trigger AS $$
BEGIN
    -- Refer to b_upd_link.
    RAISE EXCEPTION 'link_attribute_text_value rows are immutable';
END;
$$ LANGUAGE 'plpgsql';

-----------------------------------------------------------------------
-- Maintain musicbrainz.area_containment
-----------------------------------------------------------------------

-- Returns a set of area_containment rows that cover the entire parent
-- hierarchy for descendant_area_ids.  If NULL is passed, the entire
-- area_containment hierarchy is built.  (In that case, it doesn't matter
-- whether you use this function or get_area_descendant_hierarchy_rows.)
--
-- Note: This function may return duplicate rows.  It's expected that the
-- caller uses DISTINCT ON in the outer query.
CREATE OR REPLACE FUNCTION get_area_parent_hierarchy_rows(
    descendant_area_ids INTEGER[]
) RETURNS SETOF area_containment AS $$
DECLARE
    part_of_area_link_type_id CONSTANT SMALLINT := 356;
BEGIN
    RETURN QUERY EXECUTE $SQL$
        WITH RECURSIVE area_parent_hierarchy(descendant, parent, path, cycle) AS (
            SELECT entity1, entity0, ARRAY[ROW(entity1, entity0)], FALSE
              FROM l_area_area laa
              JOIN link ON laa.link = link.id
             WHERE link.link_type = $1
    $SQL$ || (CASE WHEN descendant_area_ids IS NULL THEN '' ELSE 'AND entity1 = any($2)' END) ||
    $SQL$
             UNION ALL
            SELECT descendant, entity0, path || ROW(descendant, entity0), ROW(descendant, entity0) = any(path)
              FROM l_area_area laa
              JOIN link ON laa.link = link.id
              JOIN area_parent_hierarchy ON area_parent_hierarchy.parent = laa.entity1
             WHERE link.link_type = $1
               AND descendant != entity0
               AND NOT cycle
        )
        SELECT descendant, parent, array_length(path, 1)::SMALLINT
          FROM area_parent_hierarchy
    $SQL$
    USING part_of_area_link_type_id, descendant_area_ids;
END;
$$ LANGUAGE plpgsql;

-- Returns a set of area_containment rows that cover the entire descendant
-- hierarchy for parent_area_ids.  If NULL is passed, the entire
-- area_containment hierarchy is built.  (In that case, it doesn't matter
-- whether you use this function or get_area_parent_hierarchy_rows.)
--
-- Note: This function may return duplicate rows.  It's expected that the
-- caller uses DISTINCT ON in the outer query.
CREATE OR REPLACE FUNCTION get_area_descendant_hierarchy_rows(
    parent_area_ids INTEGER[]
) RETURNS SETOF area_containment AS $$
DECLARE
    part_of_area_link_type_id CONSTANT SMALLINT := 356;
BEGIN
    RETURN QUERY EXECUTE $SQL$
        WITH RECURSIVE area_descendant_hierarchy(descendant, parent, path, cycle) AS (
            SELECT entity1, entity0, ARRAY[ROW(entity1, entity0)], FALSE
              FROM l_area_area laa
              JOIN link ON laa.link = link.id
             WHERE link.link_type = $1
    $SQL$ || (CASE WHEN parent_area_ids IS NULL THEN '' ELSE 'AND entity0 = any($2)' END) ||
    $SQL$
             UNION ALL
            SELECT entity1, parent, path || ROW(entity1, parent), ROW(entity1, parent) = any(path)
              FROM l_area_area laa
              JOIN link ON laa.link = link.id
              JOIN area_descendant_hierarchy ON area_descendant_hierarchy.descendant = laa.entity0
             WHERE link.link_type = $1
               AND parent != entity1
               AND NOT cycle
        )
        SELECT descendant, parent, array_length(path, 1)::SMALLINT
          FROM area_descendant_hierarchy
    $SQL$
    USING part_of_area_link_type_id, parent_area_ids;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_area_containment_mirror(
    parent_ids INTEGER[], -- entity0 of area-area "part of"
    descendant_ids INTEGER[] -- entity1
) RETURNS VOID AS $$
DECLARE
    part_of_area_link_type_id CONSTANT SMALLINT := 356;
    descendant_ids_to_update INTEGER[];
    parent_ids_to_update INTEGER[];
BEGIN
    -- DO NOT modify any replicated tables in this function; it's used
    -- by a trigger on mirrors.

    SELECT array_agg(descendant)
      INTO descendant_ids_to_update
      FROM area_containment
     WHERE parent = any(parent_ids);

    SELECT array_agg(parent)
      INTO parent_ids_to_update
      FROM area_containment
     WHERE descendant = any(descendant_ids);

    -- For INSERTS/UPDATES, include the new IDs that aren't present in
    -- area_containment yet.
    descendant_ids_to_update := descendant_ids_to_update || descendant_ids;
    parent_ids_to_update := parent_ids_to_update || parent_ids;

    DELETE FROM area_containment
     WHERE descendant = any(descendant_ids_to_update);

    DELETE FROM area_containment
     WHERE parent = any(parent_ids_to_update);

    -- Update the parents of all descendants of parent_ids.
    -- Update the descendants of all parents of descendant_ids.

    INSERT INTO area_containment
    SELECT DISTINCT ON (descendant, parent)
        descendant, parent, depth
      FROM (
          SELECT * FROM get_area_parent_hierarchy_rows(descendant_ids_to_update)
          UNION ALL
          SELECT * FROM get_area_descendant_hierarchy_rows(parent_ids_to_update)
      ) area_hierarchy
     ORDER BY descendant, parent, depth;
END;
$$ LANGUAGE plpgsql;

-- vi: set ts=4 sw=4 et :
