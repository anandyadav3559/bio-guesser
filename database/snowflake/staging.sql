//LIST @biogeoguesser.staging.gbif_stage;

//bronze layer for each stage
create or replace table biogeoguesser.public.bronze_temp(
    scientific_name varchar(50),
    occurance_key BIGINT,
    species_key BIGINT NOT NULL,
    source_modified DATETIME,
    source_ingested_at DATETIME NOT NULL,
    latitude DOUBLE,
    longitude DOUBLE,
    geo_hash VARCHAR(12),
    image_url TEXT,
    payload variant,
    PRIMARY KEY (occurance_key)
);

// adding into tmp bronze
COPY INTO biogeoguesser.public.bronze_temp
(scientific_name,occurance_key, species_key, source_modified, source_ingested_at, latitude, longitude, geo_hash, image_url, payload)
FROM (
  SELECT
    $1:scientific_name::varchar,
    $1:occurance_key::BIGINT,
    $1:species_key::BIGINT,
    $1:source_modified::TIMESTAMP_NTZ,
    $1:source_ingested_at::TIMESTAMP_NTZ,
    $1:location.latitude::FLOAT,
    $1:location.longitude::FLOAT,
    $1:location.geo_hash::VARCHAR,
    $1:image_url::VARCHAR,
    $1:payload::VARIANT
  FROM @biogeoguesser.staging.gbif_stage
)
FILE_FORMAT = (FORMAT_NAME = BIOGEOGUESSER.STAGING.JSON_FORMAT)
ON_ERROR = 'CONTINUE';

// removing stage file so next stage file can come
remove @biogeoguesser.staging.gbif_stage;
//select * from biogeoguesser.public.bronze_animal_occurrences;

// update the bronze tmp table to original table
INSERT INTO biogeoguesser.public.bronze_animal_occurrences
SELECT * FROM biogeoguesser.public.bronze_temp;
/*delete from biogeoguesser.public.bronze_animal_occurrences;*/


// temporary silver table
create or replace TABLE biogeoguesser.public.silver_tmp as
select * from biogeoguesser.public.bronze_temp
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY occurance_key 
    ORDER BY source_modified DESC
) = 1;

// appending tmp silver to orignal tmp
INSERT INTO biogeoguesser.public.silver_animal_occurrences
SELECT * FROM biogeoguesser.public.silver_tmp;
//select * from biogeoguesser.public.silver_animal_occurrences;
//select * from biogeoguesser.public.silver_tmp;


// creating tmp golden animal layer
CREATE or replace TABLE biogeoguesser.public.golden_tmp (
    SCIENTIFIC_NAME varchar(50),
    species_key BIGINT NOT NULL,
    image_url   STRING,
    fact        STRING,
    is_active   BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (species_key)
);
INSERT INTO biogeoguesser.public.golden_tmp (scientific_name, species_key, image_url, fact)
SELECT 
    unique_species.scientific_name,
    unique_species.species_key,
    unique_species.image_url,
    -- The AI only runs once per unique scientific_name
    SNOWFLAKE.CORTEX.AI_COMPLETE(
        'gemini-2.5-flash', 
        'Give me a short biological fact about ' || unique_species.scientific_name || '. No names/locations.'
    ) AS fact
FROM (
    -- This subquery handles the 'distinct' logic
    SELECT scientific_name, species_key, image_url
    FROM biogeoguesser.public.silver_tmp
    QUALIFY ROW_NUMBER() OVER (PARTITION BY scientific_name ORDER BY species_key) = 1
) AS unique_species;


// appending golden_animal table
insert into biogeoguesser.public.golden_animal
select distinct * from biogeoguesser.public.golden_tmp;


MERGE INTO biogeoguesser.public.golden_animal_locations tgt
USING (
    SELECT
        species_key,
        COUNT(*) AS total_points,

        ARRAY_AGG(
            OBJECT_CONSTRUCT(
                'lat', latitude,
                'lon', longitude
            )
        ) AS locations,

        ARRAY_AGG(DISTINCT geo_hash) AS geo_hashes
    FROM biogeoguesser.public.silver_tmp
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL
    GROUP BY species_key
) src
ON tgt.species_key = src.species_key
WHEN MATCHED THEN UPDATE SET
    total_points = src.total_points,
    locations = src.locations,
    geo_hashes = src.geo_hashes,
    updated_at = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN INSERT (
    species_key, total_points, locations, geo_hashes
) VALUES (
    src.species_key, src.total_points, src.locations, src.geo_hashes
);

select * from biogeoguesser.public.golden_animal_locations;
select * from biogeoguesser.public.golden_animal;

drop table biogeoguesser.public.bronze_temp;
drop table biogeoguesser.public.silver_tmp;
drop table biogeoguesser.public.golden_tmp;


//delete from biogeoguesser.public.bronze_animal_occurrences;
//delete from biogeoguesser.public.silver_animal_occurrences;
//delete from biogeoguesser.public.golden_animal;
