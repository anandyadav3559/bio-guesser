create or replace TABLE biogeoguesser.public.bronze_animal_occurrences(
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

/*like indexing*/
ALTER TABLE biogeoguesser.public.bronze_animal_occurrences CLUSTER BY (species_key, geo_hash);

/* schema where staging will happen */
CREATE OR REPLACE SCHEMA biogeoguesser.staging;

/* file format stage might have multiple file format*/
CREATE OR REPLACE FILE FORMAT biogeoguesser.staging.json_format
  TYPE = 'JSON'
  STRIP_OUTER_ARRAY = TRUE;


CREATE OR REPLACE STAGE biogeoguesser.staging.gbif_stage
FILE_FORMAT = biogeoguesser.staging.json_format;

/* silver layer */
create or replace TABLE biogeoguesser.public.silver_animal_occurrences(
    SCIENTIFIC_NAME varchar(50),
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






/* golden layer */
CREATE or replace TABLE biogeoguesser.public.golden_animal (
    SCIENTIFIC_NAME varchar(50),
    species_key BIGINT NOT NULL,
    image_url   STRING,
    fact        STRING,
    is_active   BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (species_key)
);


CREATE OR REPLACE TABLE biogeoguesser.public.golden_animal_locations (
    species_key       BIGINT NOT NULL,
    total_points      INT,
    
    -- array of {lat, lon} objects
    locations         ARRAY,
    
    -- extra: helps map view + density grouping
    geo_hashes        ARRAY,

    updated_at        TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (species_key)
);
