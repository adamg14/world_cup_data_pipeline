from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from pipelines.data_pipeline import extract_dataset, read_csv

dag = DAG(
    dag_id="web_scraping",
    default_args = {
        "owner": "Adam Worede",
        "start_date": datetime(2025, 5, 25),
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

extract_goalscorer_data = PythonOperator(
    task_id = "goalscorer_data_extraction",
    python_callable = read_csv,
    provide_context=True,
    op_kwargs = {
        "file_path": "data/goalscorers.csv"
    },
    dag = dag
)

extract_team_data = PythonOperator(
    task_id = "match_data_extraction",
    python_callable = extract_dataset,
    provide_context= True,
    op_kwargs = {
        "url": "swaptr/fifa-world-cup-2022-statistics",
        "destination_directory": "../data"
    },
    dag = dag
)

extract_player_stats_data = PythonOperator(
    task_id = "player_stats_data_extraction",
    python_callable = extract_dataset,
    provide_context = True,
    op_kwargs = {
        "url": "tittobobby/fifa-world-cup-2022-player-stats",
        "destination_directory": "../data"
    },
    dag = dag
)

extract_match_data = PythonOperator(
    task_id = "match_data_extraction",
    python_callable = extract_dataset,
    provide_context = True,
    op_kwargs = {
        "url": "shrikrishnaparab/fifa-world-cup-2022-qatar-match-data",
        "destination_directory": "../data"
    }
)

# data loading