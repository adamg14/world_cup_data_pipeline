from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from pipelines.data_pipeline import extract_dataset, read_csv, write_data_lake

dag = DAG(
    dag_id="web_scraping",
    start_date = datetime(2025, 5, 27),
    default_args = {
        "owner": "Adam Worede"
    },
    schedule_interval = None,
    catchup = False
)

# data extraction - these python operators take a raw data source (csv) either stored locally or downloaded from kaggle and transforms into a pandas dataframe
extract_stadium_data = PythonOperator(
    task_id = "stadium_data_extraction",
    python_callable = read_csv,
    provide_context=True,
    op_kwargs = {
        "file_path": "./data/stadiums.csv"
    },
    dag = dag
)

# loading the raw data into the azure data lake
load_stadium_data = PythonOperator(
    task_id = "stadium_data_load",
    python_callable = write_data_lake,
    provide_context = True,
    op_kwargs = {
        "local_file_path": "./data/stadiums.csv",
        "adl_file_path": "raw-data/stadiums.csv"
    },
    dag = dag
)

extract_goalscorer_data = PythonOperator(
    task_id = "goalscorer_data_extraction",
    python_callable = read_csv,
    provide_context=True,
    op_kwargs = {
        "file_path": "./data/goalscorers.csv"
    },
    dag = dag
)

extract_team_data = PythonOperator(
    task_id = "match_data_extraction",
    python_callable = extract_dataset,
    provide_context= True,
    op_kwargs = {
        "url": "swaptr/fifa-world-cup-2022-statistics",
        "destination_directory": "./data"
    },
    dag = dag
)

extract_player_stats_data = PythonOperator(
    task_id = "player_stats_data_extraction",
    python_callable = extract_dataset,
    provide_context = True,
    op_kwargs = {
        "url": "tittobobby/fifa-world-cup-2022-player-stats",
        "destination_directory": "./data"
    },
    dag = dag
)

extract_match_data = PythonOperator(
    task_id = "match_data_extraction",
    python_callable = extract_dataset,
    provide_context = True,
    op_kwargs = {
        "url": "shrikrishnaparab/fifa-world-cup-2022-qatar-match-data",
        "destination_directory": "./data"
    }
)

extract_stadium_data >> load_stadium_data

# data loading