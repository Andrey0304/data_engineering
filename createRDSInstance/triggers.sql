CREATE OR REPLACE FUNCTION update_col ()
    RETURNS TRIGGER
    LANGUAGE  plpgsql
    AS
$$
BEGIN
    NEW.update_time=now();
    RETURN NEW;
END
$$;

DO
$$
DECLARE
     tableName VARCHAR;
BEGIN
FOR  tableName IN SELECT table_name
                  FROM information_schema.columns
                  WHERE column_name = 'update_time'
LOOP
    EXECUTE 'DROP TRIGGER IF EXISTS  trigger_update_time ON ' || tableName || ' CASCADE;';
    RAISE NOTICE 'CREATE TRIGGER FOR: %', tableName; -- print analog
    EXECUTE 'CREATE TRIGGER trigger_update_time
             BEFORE UPDATE
             ON ' || tableName || ' FOR EACH ROW
             EXECUTE PROCEDURE update_col ();';
END LOOP;
END
$$ LANGUAGE plpgsql;