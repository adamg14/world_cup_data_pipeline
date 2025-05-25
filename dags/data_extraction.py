from airflow import dag
from datetime import datetime
from airflow.operators.python import PythonOperator
from "../pipelines/data_pipeline" import get_wikipedia_page

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
extract_stadium_data = PytonOperator(
    task_id = "staium_data_extraction"
    python_callable = get_wikipedia_page,
    provide_context=True,
    op_kwags = {
        "url": "https://en.wikipedia.org/wiki/List_of_football_stadiums_in_Qatar"
    },
    dag = dag
)

extract_statistics = PythonOperator(
    task_id = "statistics_data_extraction",
    python_callable = get_wikipedia_page,
    provide_context=True,
    op_kwags = {
        "url": "https://en.wikipedia.org/wiki/2022_FIFA_World_Cup#Statistics"
    },
    dag = dag
)
# data transformation
# data loading