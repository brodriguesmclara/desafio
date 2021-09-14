from airflow import DAG
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator, DataprocClusterDeleteOperator,\
     DataProcPigOperator, DataProcPySparkOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime
from airflow.contrib.operators import gcs_to_bq
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.operators import bigquery_operator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators import BashOperator, PythonOperator, bash_operator
from airflow.contrib.sensors.gcs_sensor import GoogleCloudStoragePrefixSensor 

# Dia de Hoje
now = datetime.now()
dia = now.strftime("%Y-%m-%d")
today = now.strftime("%d-%m-%Y")

# Variaveis do projeto
region = "us-east1"
zone = "us-east1-b"
project_id = "local-terminus-325600"
bucket = "dasa_saude"

# Argumentos padrao do airflow
default_args = {
            "owner": "Bruno",
            "depends_on_past": False,
            "start_date": datetime(2021,9,14), # Data de início da DAG
            "retries": 0,
        }


# Nome da dag, descricao, e frequencia de execucao
dag = DAG(
    dag_id="desafio_dasa",
    default_args = default_args,
    description = "Orquestração ingestão de dados",
    schedule_interval = "0 4 * * *" # Executar às 04:00 todo dia
    )

# Funcao que espera um determinado arquivo para começar a orquestracao
def storage_sensor(task, bucket_path, prefix_file):
    file_sensor = GoogleCloudStoragePrefixSensor(
            task_id='{}'.format(task, dia),  
            bucket=bucket,
            prefix='{}/{}'.format(bucket_path, prefix_file),
            dag=dag
        )

    return file_sensor 

# Executa script pyspark no Dataproc
def execute_script(task, script_storage, cluster):
    pyspark_operator = DataProcPySparkOperator(
            task_id='{}_{}'.format(task, dia),
            main=script_storage,
            cluster_name=cluster,
            region="us-central1",
            dag=dag
        )

    return pyspark_operator


# Cria cluster, qualquer alteracao de configuracao deve ser feita aqui
def create_cluster(task, cluster, status):
    cluster_dataproc = DataprocClusterCreateOperator(
        task_id = task,
        project_id = project_id,
        #service_account = 'composer-np-data-netezza@data-88d7.iam.gserviceaccount.com',
        cluster_name = cluster,
        num_workers = 2,
        region = "us-central1",
        zone = "us-central1-f",
        #num_preemptible_workers = 0,
        #metadata = dict(PIP_PACKAGES="google-cloud-storage pandas simpledbf"),  
        master_machine_type = "n1-standard-2",
        worker_machine_type = "n1-standard-2",
        master_disk_size = 30,
        worker_disk_size = 30,
        storage_bucket = bucket,
        #image_version = "1.3.82-debian10",
        trigger_rule=status,
        #subnetwork_uri = 'projects/np-network-ffe3/regions/southamerica-east1/subnetworks/data',
        #internal_ip_only = True,
        #auto_delete_ttl = 3600,
        dag = dag
    )

    return cluster_dataproc


# Deleta cluster, mas so se todos os jobs ja terminaram
def delete_cluster(task, cluster):
    del_cluster = DataprocClusterDeleteOperator(
            task_id = task,
            project_id = project_id,
            cluster_name = cluster,
            region = "us-central1",
            trigger_rule="all_done",
            dag=dag
        )

    return del_cluster

# Carrega arquivos no Big Query
def load_big_query(task, source_objects, table_name):
    load_big_query_operator = GoogleCloudStorageToBigQueryOperator(
        task_id=task,
        bucket=bucket,
        source_objects=[source_objects],
        source_format='PARQUET',
        create_disposition = 'CREATE_IF_NEEDED',
        destination_project_dataset_table= "{}:dasa_bi.{}".format(project_id, table_name),
        write_disposition='WRITE_APPEND',
        time_partitioning={"type":"DAY"},
        encoding='utf-8',
        autodetect=True,
        ignore_unknown_values = True,
        #cluster_fields= True,
        dag=dag)

    return load_big_query_operator

# Chama as procedures
def procedures(task, procedure):
    sp_create_base_cluster = BigQueryOperator(
        task_id=task,
        bql=procedure,
        use_legacy_sql=False,
        dag=dag,
        depends_on_past=False)

    return sp_create_base_cluster
    
def bashoperator(task, command, status):
    bash = BashOperator(
           task_id=task,
           trigger_rule = status,
           bash_command=command,
           dag=dag)

    return bash 

# Função que recebe um prefixo para inicio de orquestração
file_sensor_contas09 = storage_sensor("file_sensor_contas09", "input_file", "contas_201909.csv")
file_sensor_contas10 = storage_sensor("file_sensor_contas10", "input_file", "contas_201910.csv")
file_sensor_contas11 = storage_sensor("file_sensor_contas11", "input_file", "contas_201911.csv")
file_sensor_cadastro = storage_sensor("file_sensor_cadastro", "input_file", "cadastro.json")


# Função executa script .py
run_cadastro = execute_script("run_cadastro","gs://"+bucket+"/codigos/cadastro_flat.py", "cluster-dasa-desafio")
run_contas = execute_script("run_contas","gs://"+bucket+"/codigos/contas.py", "cluster-dasa-desafio")


# Função cria cluster Dataproc dependendo do arquivo de prefixo que chegar no storage 
cluster_dasa_etl = create_cluster("cluster_dasa_etl", "cluster-dasa-desafio", "one_success")

# Função deleta cluster
delete_cluster_dasa_etl = delete_cluster("delete_cluster_dasa_etl", "cluster-dasa-desafio")

# Função carrega arquivos PARQUET no Big Query
load_cadastro = load_big_query("load_cadastro","output_file/cadastro_flat_"+dia+".parquet/*.parquet","Cadastro")
load_contas = load_big_query("load_contas","output_file/contas_"+dia+".parquet/*.parquet","Contas")

# Função chama as procedures do Big Query
sp_cria_prestador = procedures("sp_cria_prestador","CALL dasa_bi.sp_cria_prestador()")

#Move arquivos ja processados para pasta processados no diretorio de input_file
move_arquivos_csv = bashoperator("move_arquivos_csv",
	"gsutil mv gs://{}/input_file/*.csv gs://{}/input_file/processados/{}/".format(bucket, bucket, dia),
	"one_success")
move_arquivos_json = bashoperator("move_arquivos_json",
	"gsutil mv gs://{}/input_file/*.json gs://{}/input_file/processados/{}/".format(bucket, bucket, dia),
	"one_success")    


[file_sensor_contas09, file_sensor_contas10, file_sensor_contas11, file_sensor_cadastro] >> cluster_dasa_etl >> [ run_cadastro, run_contas] >> delete_cluster_dasa_etl >> \
[load_cadastro, load_contas, move_arquivos_csv, move_arquivos_json ] >> sp_cria_prestador 
