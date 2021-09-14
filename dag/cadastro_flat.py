# Importando as bibliotecas Pyspark
import pyspark
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from datetime import datetime
from pyspark.sql.functions import explode,udf
import pyspark.sql.functions as sf
from pyspark.sql.window import Window
from datetime import datetime, date

now =datetime.now()
dia=now.strftime("%Y%m%d")
day = now.strftime("%Y-%m-%d")

#Cria contexto SQL no Spark
sqlContext = pyspark.SQLContext(pyspark.SparkContext.getOrCreate())

#Lê arquivo json de entrada
print('Lendo arquivo JSON')
df = sqlContext.read.json("gs://dasa_saude/input_file/cadastro.json")

#Eliminando array do arquivo
print('Tratando campos array')
df = df.select(explode(df.cadastro))
df_flat = df.select('col.email','col.empresa','col.endereco','col.name','col.telefone')

#Cria SK
print('Criando Id')
#df_final1 = df_flat\
#.select(sf.row_number().over(Window.partitionBy().orderBy(df_flat['name'])).alias('sk_name')
#,'name','telefone','endereco','empresa','email').distinct()

df_final = df_flat\
.withColumn('e',sf.substring('email',0,3))\
.select(sf.concat('name',sf.lit('#'),'e').alias('id_cad'),'name','telefone','endereco','empresa','email')

#Escreve arquivo json sem array e salva em um diretorio de saida
print('Escrevendo DataFrame tratado no arquivo de saida')

df_final.write.parquet("gs://dasa_saude/output_file/cadastro_flat_{}.parquet/".format(day))

print('Fim da execução')