/* sending toward user */
CREATE OR REPLACE PROCEDURE get_species_data(species_key NUMBER)
RETURNS TABLE (
species_key bigint,
    scientific_name STRING,
    image_url STRING,
    species_fact STRING,
    status_code NUMBER
)
LANGUAGE SQL
AS
$$
DECLARE
    -- Use a result set to store the query output
    res RESULTSET;
BEGIN
    -- We select exactly one row for the API
    res := (
        SELECT 
            species_key,
            scientific_name, 
            image_url, 
            fact, 
            200 AS status_code
        FROM biogeoguesser.public.golden_animal
        WHERE species_key = :species_key
        LIMIT 1
    );
    
    RETURN TABLE(res);
END;
$$;
call get_species_data(5219416);


create or replace procedure get_animal_locations(species_key BIGINT)
returns table(
    species_key       BIGINT,
    total_points      INT,
    locations         ARRAY,
    geo_hashes        ARRAY
) language sql
as 
$$
DECLARE
res RESULTSET;
begin
res :=(
select species_key,total_points,locations,geo_hashes from biogeoguesser.public.golden_animal_locations
where species_key = :species_key
);
 RETURN TABLE(res);
end;
$$;

CALL get_animal_locations(5219416); -- Correct for BIGINT