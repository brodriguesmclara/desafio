# Challenge Dasa - Google Cloud
![Imgur](https://i.imgur.com/hCnoY13.png)
### Proposta do Desafio:
A Dasa me propôs esse desafio para conhecer um pouco mais sobre a minha forma de resolver problemas envolvendo engenharia de dados.

#### Objetivos
###### O desafio consistia em criar uma pipeline de dados com seus processode de ETL e criação de um DW. A tecnologia era opcional.
1. Identificar os campos que possam criar um id único para cada pessoa na base de cadastro;
2. Linkar a base de contas com a base de cadastro utilizando o id único criado com a base de cadastro;
3. Criar uma base única de prestadores gerando os id e linkar esses id na base de contas;
4. Apresentar as bases em um banco Data Warehouse;

#### Massa de dados
Foi disponibilizada uma base de dados com arquivos no formato csv e json, que se encontram na pasta [base_dados]
(https://github.com/brodriguesmclara/desafio/tree/main/base_dados "base_dados")

#### Observações
1. Você deve criar uma rotina onde seja possível o recebimento desses arquivos mensalmente;
2. Deve utilizar uma ferramenta baseada em ETL (Talend Open Source, Pentaho, Apache Bean, Azure Data Factory, Data Flow, etc);
3. O projeto pode ser criado em cloud ou on-premise;

#### Códigos 
Todos os códigos usados no desenvolvimento estão segregados por tipo de funcionalidade e disponibilizadas no git hub, se econtram nas pastas pyspark (https://github.com/brodriguesmclara/desafio/tree/main/pyspark), dag (https://github.com/brodriguesmclara/desafio/tree/main/dag) e terraform 
(https://github.com/brodriguesmclara/desafio/tree/main/terraform)

**Desenho da arquitetura:**

![GCP](https://i.imgur.com/YYdYzzA.png)

#### Cloud Storage

A ferramenta Cloud Storage foi escolhida como Data Lake na nossa arquitetura pois fornece armazenamento dos arquivos ou como um backup de segurança para aqueles que já estão guardados em dispositivos físicos. Isso tudo com a segurança de que seus registros mais importantes não serão perdidos, danificados ou acessados por pessoas sem autorização. O mesmo também oferece Performance otimizada, Infraestrutura virtual ilimitada, ótimo custo-benefício, sincronização instantânea entre todos os aparelhos, alta escalabilidade entre outras.

#### Cloud Dataproc
A arquitetura conta com uma camada de ETL no Cloud Dataproc que contemplará o uso do Spark que é uma ferramenta Big Data para processar grandes conjuntos de dados de forma paralela e distribuída, além de ser 100 vezes mais rápido pois processa tudo na memória.

#### Big Query
O BigQuery foi contemplado na nossa arquitetura porque é um data warehouse totalmente gerenciado e sem servidor que permite análises escalonáveis em petabytes de dados. É uma plataforma como serviço (PaaS) que oferece suporte a consultas usando ANSI SQL. Ele também possui recursos integrados de aprendizado de máquina.

#### Composer 
O fluxo de orquestração da pipeline será gerenciado pelo Composer, o mesmo terá o trabalho de criar um cluster Dataproc, executar um processo Spark e desligar o cluster assim que o processamento acabar, seguindo as melhores práticas do Google que faz menção sobre criar cluster no Dataproc de forma preemptiva, além de executar uma task que irá carregar os arquivos processados para o Big Query e chamará uma procedure que atualizará os dados para uma segunda camada TRUSTED com dados Particionados e Clusterizados para melhor desempenho e economia no momento da consulta de dados.

### Infraestrutura

![Terraform](https://i.imgur.com/C3p4BaE.png "Terraform")

Toda nossa infraestrutura será escrita com Terraform que é uma ferramenta para construir, alterar e configurar infraestrutura de maneira segura e eficiente. A ferramenta tem incontáveis benefícios que possibilitam criar toda a infraestrutura em ambiente de desenvolvimento e com alguns cliques conseguimos replicar tudo que foi feito para ambientes diferentes como Homologação ou Produção por exemplo, além de ser MultiCloud.

#### Deploy Terraform
Primeiramente iremos construir a infraestrutura do <b>Cloud Storage</b>
Segue imagem:
![Imgur](https://i.imgur.com/0CRp9Ee.png)

![Imgur](https://i.imgur.com/1zzaVd2.png)

Feito criação do bucket e subpastas.
![Imgur](https://i.imgur.com/NFimaRW.png)

![Imgur](https://i.imgur.com/yVL5pYo.png)

Construindo infraestrutura <b>Cloud BigQuery</b>

![Imgur](https://i.imgur.com/0CRp9Ee.png)

![Imgur](https://i.imgur.com/nOM8SRO.png)

Criado dataset.

![Imgur](https://i.imgur.com/43A1F0l.png)

### Desenvolvimento

#### Cloud Storage
  Foi criado um Lake para armazenar o histórico de arquivos, esses arquivos chegam na sua forma bruta dentro da pasta input_file (camada RAW) e a partir desse momento a pipeline inicia. Após o processo de ETL que será explicado a seguir, esses arquivos na sua forma bruta são enviados para uma pasta processados onde é criada uma subpasta com a data deste processamento, em paralelo esses arquivos após o processo de tratamento dos dados são enviados para uma pasta chamada output_file (camada trusted) onde estão prontos para a criação do DW.
  
  ![Imgur](https://i.imgur.com/WkQvJQs.png)
  
  ![Imgur](https://i.imgur.com/OjHvc4E.png)
  
  ![Imgur](https://i.imgur.com/VcyMjK4.png)
  
  #### Cloud Dataproc
  Os códigos pyspark estão no Cloud Storage no caminho dasa_saude/codigos.
  
  ![Imgur](https://i.imgur.com/LSXrI0Z.png)
  
  Assim que os arquivos chegam no Lake é instânciada um cluster efêmero DataProc para iniciar o processo de ETL. Neste cluster será executando 2 códigos pyspark.
  O código pyspark responsável pelos arquivos contas.csv faz a união dos 3 arquivos em apenas um dataframe, trata a coluna data para uma forma padrão corrigindo o mês em formato string para formato de número, converte os dados da coluna VALOR para decimal e na coluna PROCEDIMENTO, elimina os campos vazios inserindo os valors NAO CADASTRADO, criação de uma chave única que fará o link com a tabela cadastro, para a criação dessa chave única foi utilizado a coluna name concatenado com os 3 primeiros caracteres da coluna email gerando a coluna ID_CNT e por fim converte o arquivos para parquet, eliminando o risco de inferência de schema no momendo da carga no DW.
  No código pyspark responsável pelo arquivo cadastro.json, a primeira ação adotada é o flatting do arquivo para facilitar as consultas e visualização desta tabela no momento que for carregada no DW, foi criada uma coluna de chave para fazer link com a tabela de contas, foi utilizado a coluna name concatenado com os 3 primeiros caracteres da coluna email gerando a coluna ID_CAD e por fim a converte este arquivo para parquet.
  Após todo esse processo os aquivos de saída são enviados novamente para o Lake na pasta output_file e nesse momento serão enviados para o BigQuery para a criação de tabelas.
  
  ### BigQuery
  
  Foi criado um dataset chamado dasa_bi para criação das tabelas Contas e Cadastro. Para efeito de comparação foram criadas as tabelas Raw_Contas e Raw_Cadastro que são criadas a partir dos aquivos brutos.
  Segue evidência:
  #### Tabela Raw_Cadastro
  
  ![Imgur](https://i.imgur.com/YrcRBuv.png)
  ![Imgur](https://i.imgur.com/hzvgfRw.png)
  
  #### Tabela Raw_Contas
  
  ![Imgur](https://i.imgur.com/lwqGSxV.png)
  
  #### Tabela Cadastro
  Após o ETL a tabela Cadastro sofreu um flatting eliminando o array, e foi incluso um novo campo identificador único chamado id_cad que será a chave identificadora que linkará com a tabela Contas.
  
  ![Imgur](https://i.imgur.com/gkOX7g5.png)
  
  #### Tabela Contas
  
  Os join entre as tabelas Cadastro e Contas é feito pelos IDs id_cnt da tabela Contas e id_cad da tabela Cadastro.
  
  ![Imgur](https://i.imgur.com/sqRQcIx.png)
  
  #### Tabela Prestadores
  Foi criada uma Procedure que tem o objetivo de criar a tabela Prestadores a partir da tabela Contas, a chave única da tabela Prestadores é a id_prt e faz link com a tabela Contas pelo id_cnt.
  
  ![Imgur](https://i.imgur.com/rdyUK99.png)
  
  ### Composer
  O Cloud Composer é utilizado para fazer a automação dos processo e a movimentação dos dados, foi criado uma dag chamada dag_desafio_dasa.py que possui uma task de sensor, esse sensor monitora a pasta input_file no Cloud Storage e assim que os arquivos caem nessa pasta o sensor dispara o status de SUCCESS iniciando toda pipeline.
  Essa dag de automação possui as seguintes tasks:
  1. Sensor para verificação da entrada dos arquivos na pasta input_file;
  2. Criação do cluster efêmero no Dataproc, para o processo de ETL;
  3. Execução dos scripts pyspark, para a transformação dos arquivos contas.csv e cadastro.json, ambos executados de forma paralela;
  4. Delete do cluste;
  5. Carga desses arquivos já processados no DW e em paralelo a criação da subpasta processados dentro da input_file e a movimentação dos arquivos tratados para essa nova pasta;
  6. Execução da Procedure de criação da tabela Prestadores. 
  











