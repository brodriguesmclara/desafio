# Challenge Dasa - Google Cloud
[![Dasa](https://i.imgur.com/BNvzBDfm.png "Dasa")]
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
2.Deve utilizar uma ferramenta baseada em ETL (Talend Open Source, Pentaho, Apache Bean, Azure
Data Factory, Data Flow, etc);
3.O projeto pode ser criado em cloud ou on-premise;

#### Infraestrutura

### Cloud Storage

A ferramenta Cloud Storage foi escolhida como Data Lake na nossa arquitetura pois fornece armazenamento dos arquivos ou como um backup de segurança para aqueles que já estão guardados em dispositivos físicos. Isso tudo com a segurança de que seus registros mais importantes não serão perdidos, danificados ou acessados por pessoas sem autorização. O mesmo também oferece Performance otimizada, Infraestrutura virtual ilimitada, ótimo custo-benefício, sincronização instantânea entre todos os aparelhos, alta escalabilidade entre outras.

### Cloud Dataproc
A arquitetura conta com uma camada de ETL no Cloud Dataproc que contemplará o uso do Spark que é uma ferramenta Big Data para processar grandes conjuntos de dados de forma paralela e distribuída, além de ser 100 vezes mais rápido pois processa tudo na memória.

### Big Query
O BigQuery foi contemplado na nossa arquitetura porque é um data warehouse totalmente gerenciado e sem servidor que permite análises escalonáveis em petabytes de dados. É uma plataforma como serviço (PaaS) que oferece suporte a consultas usando ANSI SQL. Ele também possui recursos integrados de aprendizado de máquina.

### Composer 
O fluxo de orquestração da pipeline será gerenciado pelo Composer, o mesmo terá o trabalho de criar um cluster Dataproc, executar um processo Spark e desligar o cluster assim que o processamento acabar, seguindo as melhores práticas do Google que faz menção sobre criar cluster no Dataproc de forma preemptiva, além de executar uma task que irá carregar os arquivos processados para o Big Query e chamará uma procedure que atualizará os dados para uma segunda camada TRUSTED com dados Particionados e Clusterizados para melhor desempenho e economia no momento da consulta de dados.

[![Terraform](https://i.imgur.com/C3p4BaE.png "Terraform")](https://www.terraform.io/ "Terraform")

Toda a infraestrutura do desafio foi desenvolvida em terraform e feito o deploy na provedora de nuvem pública GCP.

**Abaixo temos um desenho da arquitetura:**

[![GCP](https://i.imgur.com/YYdYzzA.png)

#### Deploy Terraform
Segue abaixo as evidências da criação da infraestrutura feita via Terraform.



#### Códigos 
Todos os códigos usados no desenvolvimento estão segregados por tipo de funcionalidade e disponibilizadas no git hub, se econtram nas pastas pyspark (https://github.com/brodriguesmclara/desafio/tree/main/pyspark), dag (https://github.com/brodriguesmclara/desafio/tree/main/dag) e terraform 
(https://github.com/brodriguesmclara/desafio/tree/main/terraform)

*Escreva uma query que retorna a quantidade de linhas na tabela Sales.SalesOrderDetail pelo campo SalesOrderID, desde que tenham pelo menos três linhas de detalhes.*

`Em desenvolvimento`

*Escreva uma query que ligue as tabelas Sales.SalesOrderDetail, Sales.SpecialOfferProduct e Production.Product e retorne os 3 produtos (Name) mais vendidos (pela soma de OrderQty), agrupados pelo número de dias para manufatura (DaysToManufacture).*

`Em desenvolvimento`

*Escreva uma query ligando as tabelas Person.Person, Sales.Customer e Sales.SalesOrderHeader de forma a obter uma lista de nomes de clientes e uma contagem de pedidos efetuados.*

`Em desenvolvimento`

*Escreva uma query usando as tabelas Sales.SalesOrderHeader, Sales.SalesOrderDetail e Production.Product, de forma a obter a soma total de produtos (OrderQty) por ProductID e OrderDate.*

`Em desenvolvimento`

*Escreva uma query mostrando os campos SalesOrderID, OrderDate e TotalDue da tabela Sales.SalesOrderHeader. Obtenha apenas as linhas onde a ordem tenha sido feita durante o mês de setembro/2011 e o total devido esteja acima de 1.000. Ordene pelo total devido decrescente.*

`Em desenvolvimento`

#### Relatório
`Em desenvolvimento`







