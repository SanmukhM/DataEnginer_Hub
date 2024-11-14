from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.utils.dates import days_ago
from airflow.sensors.external_task_sensor import ExternalTaskSensor

# Define default arguments for the DAG
default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'email': ['your_email@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
}

# Instantiate the DAG
with DAG(
    'bigquery_load_job',
    default_args=default_args,
    description='Schedule a BigQuery load job',
    schedule_interval=None,  # Set your desired schedule (e.g., '@daily', '0 0 * * *')
    start_date=days_ago(1),
    catchup=False,
    tags=['bigquery', 'load_job'],
) as dag:

    # Define the sensor to wait for another DAG
    wait_for_another_dag = ExternalTaskSensor(
        task_id='wait_for_another_dag',
        external_dag_id='your_other_dag_id',  # Replace with the DAG ID you want to wait for
        external_task_id=None,  # You can specify a specific task ID or leave it as None to wait for the entire DAG
        dag=dag,
    )

    # Define the BigQuery load job configuration
    load_job = BigQueryInsertJobOperator(
        task_id='load_data_to_bigquery',
        configuration={
            'load': {
                'sourceUris': ['gs://your-bucket/your-data-file.csv'],  # Replace with your GCS URI
                'destinationTable': {
                    'projectId': 'your-project-id',
                    'datasetId': 'your_dataset_id',
                    'tableId': 'your_table_id',
                },
                'sourceFormat': 'CSV',  # Adjust if needed (e.g., 'NEWLINE_DELIMITED_JSON')
                'writeDisposition': 'WRITE_TRUNCATE',  # Or 'WRITE_APPEND'
                'autodetect': True,  # Set to False if you need to provide a schema
                # Add other load job configuration options as needed
            }
        },
        location='your-location',  # Replace with your BigQuery location (e.g., 'US')
    )

    # Set task dependencies 
    wait_for_another_dag >> load_job  # The load job will run after the sensor is successful