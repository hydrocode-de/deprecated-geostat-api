#!/bin/bash
export PYGEOAPI_DATA_PATH=/src/data
export PYGEOAPI_DB_NAME=data.db

# run
python -m geostat_api run --prod