from airflow import dag
from datetime import datetime
dag = DAG(
    dag_id="web_scraping",
    default_args = {
        "owner" = "Adam Worede",
        "start_date": datetime(2025, 5, 25),
    },
    schedule_interval = None,
    catchup = False
)

# data extraction
# data transformation
# data loading