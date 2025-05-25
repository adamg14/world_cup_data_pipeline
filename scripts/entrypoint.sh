#!/bin/bash

airflow db check || airflow db init

airflow users list | grep -q admin || \
airflow users create \
  --username admin \
  --password admin \
  --firstname admin \
  --lastname admin \
  --role Admin \
  --email admin@example.com

exec airflow "$@"