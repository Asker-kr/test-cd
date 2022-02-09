from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

## DAG
default_args = {
    "owner": "sooyoung.kim",
    "depends_on_past": False,
    "email": [
        "dataops@greenlabs.co.kr",
    ],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "start_date": datetime(2022, 2, 7),
    "retry_delay": timedelta(minutes=3)
}

dag = DAG(
    dag_id="redshift-connection-test",
    description="redshift connection을 사용하여 연결이 되는지 확인하고 데이터를 생성한다",
    schedule_interval="30 16 * * *",  # (16:30 UTC = 01:30 KST)
    template_searchpath=["/usr/local/airflow/dags/sqls/test"],
    catchup=False,
    default_args=default_args
)

# Tasks
start = DummyOperator(dag=dag, task_id="start")

test_select_orders_from_redshift = PostgresOperator(
    task_id="test_select_orders_from_redshift",
    postgres_conn_id="redshift-ods-connection",
    database="ods",
    sql="select_orders.sql",
    params={
        "target": "farmmorning.dw.user_profile",
    },
    dag=dag
)

test_ctas_from_redshift = PostgresOperator(
    task_id="test_ctas_from_redshift",
    postgres_conn_id="redshift-ods-connection",
    database="ods",
    sql="ctas_orders.sql",
    params={
        "target": "farmmorning.dw.user_profile",
    },
    dag=dag
)

# Flow
start >> [test_select_orders_from_redshift, test_ctas_from_redshift]
