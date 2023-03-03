#!/usr/bin/env bash
docker build -t smarthealth-api .
docker run --env-file .env -p 3010:3010 -it smarthealth-api