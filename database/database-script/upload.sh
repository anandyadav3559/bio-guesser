#!/usr/bin/env bash
set -euo pipefail

ACCOUNT="ggyjkvm-zvb37272"
USER="ANAND3559"

STAGE="biogeoguesser.staging.gbif_stage"
LOCAL_PATH="/mnt/c/Users/anand/OneDrive/Desktop/bio-geo-guesser/database/database-script/data/data.json"
# For multiple:
# LOCAL_PATH="/mnt/c/Users/anand/OneDrive/Desktop/bio-guesser/data/*.json"

snowsql -a "$ACCOUNT" -u "$USER" -o exit_on_error=true <<SQL
PUT file://$LOCAL_PATH @$STAGE AUTO_COMPRESS=TRUE OVERWRITE=FALSE;
LIST @$STAGE;
SQL

echo "✅ Upload completed to stage @$STAGE"
