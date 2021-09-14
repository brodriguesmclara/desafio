# Challenge Rox - Google Cloud
[![Rox partner](https://i.imgur.com/oOCOEM9.png "Rox partner")](https://roxpartner.com/ "Rox partner")

### Proposta do Desafio:
A Rox me propôs esse desafio para conhecer um pouco mais sobre a minha forma de resolver problemas envolvendo engenharia de dados.

#### Objetivos
###### Um dos requisitos do desafio é usar uma nuvem pública (Azure, AWS, GCP).
1. Fazer a modelagem conceitual dos dados
2. Criação da infraestrutura necessária
3. Criação de todos os artefatos necessários para carregar os arquivos para o banco criado
4. Desenvolvimento de scripts para análise de dados
5. Criar um relatório em qualquer ferramenta de visualização de dados. (Opcional)

#### Massa de dados
Foi disponibilizada uma massa de dados de uma empresa que produz bicicletas, os arquivos foram fornecidos no formato csv e se encontram na pasta [data_files](https://github.com/gdelmondes/challenge-rox/tree/dev/data_files "data_files")

#### Modelagem
`Em desenvolvimento`

#### Infraestrutura

[![Terraform](https://i.imgur.com/C3p4BaE.png "Terraform")](https://www.terraform.io/ "Terraform")

Toda a infraestrutura do projeto foi desenvolvida em terraform para que seja facilmente replicável e até mesmo facilitar a migração para outras nuvens, se for o caso.

**Abaixo temos um desenho da arquitetura:**

`Em desenvolvimento`

#### Artefatos

`Em desenvolvimento`

#### Scripts SQL
Todos os scripts estão na pasta [sql](https://github.com/gdelmondes/challenge-rox/tree/dev/sql "sql"),  abaixo segue o enunciado usado para desenvolver as consultas e a query como resposta

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







