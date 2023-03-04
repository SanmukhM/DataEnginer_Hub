#Use randint to indentify the accuracy of the Dags task
#create 3 task for select one of the best.

#Step 1 : Import DAG from airflow | Point to remember is DAG should be used as Context manager, I will take parameter
 #Dagid, start_time, schedule__interval, catchup

from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from random import randint
from airflow.operators.bash import BashOperator

#BranchPythonOperator

def choose_best_model(ti):
    accuracies=ti.xcom_pull(task_ids=[
        'training_model_A',
        'training_model_A',
        'training_model_A'
    ]
                )
    best_accuracy=max(accuracies)
    if (best_accuracy>7):
        return 'accurate'
    return 'inaccurate'

#Python callable Functions

def _training_model():
    return randin(1,10 )

#open Dag with context manager

with DAG('Sanmukh_dag', start_date=datetime(2021,1,1),schedule_interval="@daily",catchup=False) as dag:  #Initialize Dag operator
    training_model_A= PythonOperator(
          task_id="training_model_A",
              python_callable=_training_model
      )
        
    training_model_B= PythonOperator(
      task_id="training_model_B",
              python_callable=_training_model
      )
    training_model_C= PythonOperator(
      task_id="training_model_C",
              python_callable=_training_model
      )
    
    choose_best_model= BranchPythonOperator(
        task_id="choose_best_model",
        python_callable=choose_best_model
    
    )
    accurate=BashOperator(
       task_id="accurate",
       bash_command="echo 'accurate'"

    )
    inaccurate=BashOperator(
       task_id="inaccurate",
       bash_command="echo 'inaccurate'"

    )
    

