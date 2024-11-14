### Prepared By Rama Kishore Korlepara on 2022-09-21 ###
### Airflow DAG code to create a dataproc cluster on the fly, run the ETL PySpark job and delete the cluster at the end ###
### Runs ETL job on CreditRisk Data for ModelOps Demo ###

from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.dataproc import  DataprocCreateClusterOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocDeleteClusterOperator

default_args = {
    'depends_on_past': False   
}

#Values to create cluster on fly
CLUSTER_NAME = 'etl-job-model-ops-demo'
REGION='us-central1'
PROJECT_ID='mlops-365205'

#Change this variable value to run any required spark code
PYSPARK_URI='gs://spark-code1/etl_working_code.py'

#Cluster config details
CLUSTER_CONFIG = {
    "master_config": {
        "num_instances": 1,
        "machine_type_uri": "n1-standard-2",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 50},
    },
    "worker_config": {
        "num_instances": 2,
        "machine_type_uri": "n1-standard-2",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 50},
    }
}


PYSPARK_JOB = {
    "reference": {"project_id": PROJECT_ID},
    "placement": {"cluster_name": CLUSTER_NAME},
    "pyspark_job": {
    "main_python_file_uri": PYSPARK_URI #,
    #"jar_file_uris": ["gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"]}
}
}

with DAG('etl-dataproc-demo',default_args=default_args,description='A simple DAG to create a Dataproc ETL workflow',
         schedule_interval=None,start_date = days_ago(2), catchup=False) as dag:
    
    create_cluster = DataprocCreateClusterOperator(
        task_id="create_cluster",
        project_id=PROJECT_ID,
        cluster_config=CLUSTER_CONFIG,
        region=REGION,
        cluster_name=CLUSTER_NAME,
    )

    pyspark_submit_etl = DataprocSubmitJobOperator(
        task_id="pyspark_submit_etl", 
        job=PYSPARK_JOB, 
        region=REGION, 
        project_id=PROJECT_ID
    )

    delete_cluster = DataprocDeleteClusterOperator(
        task_id="delete_cluster", 
        project_id=PROJECT_ID, 
        cluster_name=CLUSTER_NAME, 
        region=REGION
    )

    create_cluster >> pyspark_submit_etl >> delete_cluster

