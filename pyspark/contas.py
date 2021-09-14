import pyspark
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from datetime import datetime
from pyspark.sql.functions import *
import pyspark.sql.functions as sf
from datetime import datetime, date

now =datetime.now()
dia=now.strftime("%Y%m%d")
day = now.strftime("%Y-%m-%d")

print('Lendo arquivo CSV')
sqlContext = pyspark.SQLContext(pyspark.SparkContext.getOrCreate())
df_csv = sqlContext.read.format('CSV').option('header',True).option('delimiter',';').load('gs://dasa_saude/input_file/*.csv')
print('Arquivo CSV carregado')

split_col = sf.split(df_csv['Data'], '-')

print('Tratando campos de data no DataFrame')
df_data = df_csv\
.select('email','name'
,concat(when(sf.length(split_col.getItem(0)) < 2,concat(sf.lit('0'),split_col.getItem(0))).otherwise(split_col.getItem(0))
,sf.lit('-'),when(split_col.getItem(1) == 'jan','01')
.when(split_col.getItem(1) == 'fev','02')
.when(split_col.getItem(1) == 'mar','03')
.when(split_col.getItem(1) == 'abr','04')
.when(split_col.getItem(1) == 'mai','05')
.when(split_col.getItem(1) == 'jun','06')
.when(split_col.getItem(1) == 'jul','07')
.when(split_col.getItem(1) == 'ago','08')
.when(split_col.getItem(1) == 'set','09')
.when(split_col.getItem(1) == 'out','10')
.when(split_col.getItem(1) == 'nov','11')
.when(split_col.getItem(1) == 'dez','12'),sf.lit('-'),split_col.getItem(2)).alias('Data')
,'valor','procedimento','tipo','prestador','observacao','competencia')
print('Criado Dataframe com campo de data padronizado')

# Eliminando campos vazios na coluna procedimento e feito conversao para Decima na coluna valor
print('Tratando colunas procedimento e valor')
df_data = df_data\
.withColumn('procedimento',sf.when(df_data.procedimento.isNull(),"Nao Cadastrado").otherwise(df_data.procedimento))\
.withColumn('valor',sf.col('valor').cast(DecimalType(10,2))).alias('valor')\
.select('email','name','Data','valor','procedimento','tipo','prestador','observacao','competencia')
print('Colunas procedimento e valor padronizado')

print('Criada colunas de ID')
df_id = df_data\
.withColumn('e',sf.substring('email',0,3))\
.select(sf.concat('name',sf.lit('#'),'e').alias('id_cnt'),'name','Data','valor','procedimento','tipo','prestador','observacao','competencia')

#Escrevendo Dataframe final no arquivo CSV de saida
print('Escrevendo DataFrame tratado no arquivo de saida')
df_id.write.parquet('gs://dasa_saude/output_file/contas_{}.parquet'.format(day))

print('Fim da execução')
