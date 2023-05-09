# **Projeto de análise de dados Bolsa-familia**

---

## Este é o resultado parcial do projeto de análise dos dados do Bolsa-Família disponibilizados na API do Portal da Transparência do Governo Federal 
()https://api.portaldatransparencia.gov.br/swagger-ui.html#/



#### Por ser um projeto de grande proporção, dividi em etapas afim de organizar meu trabalho, otimizar os custos e facilitar o entendimento de terceiros. 
#### A divisão se dá em 3 etapas:
#### * Ingestão de dados
#### * Utilização do **Athena** AWS para análise dos dados no **S3** AWS
#### * Criação de **Júpyter notebook** para geração de gráficos via **Pyspark** e **Matplotlib**

#### Neste momento, o projeto encontra-se no processo de **ingestão de dados**.

#### Iniciei o projeto estudando a API de dados do Governo Federal e escolhi os dados do programa Bolsa-Família afim de focar nas variáveis:
#### * Município
#### * Total gasto no mês

#### Para isso, foi preciso encontrar a variável ***Código IBGE***, disponível na API de localidades do portal do IBGE. Então fiz um código no Lambda Function AWS em Python para percorrer os dados de municípios desta API, inicialmente ingerindo os dados separados por região (Norte, Nordeste, Centro-oeste, Sudeste e Sul) e em seguida retirando somente os códigos desejados para finalmente salvá-los em um CSV.

#### Também utilizando o Lambda Function da AWS, criei outro código em Python que segue em loop os passos abaixo:
#### * Cria o header de requerimento da API do Governo a partir de lista de ano/mês dentro do espaço de tempo escolhido (2012 a 2022), do código IBGE retirado da lista criada em CSV e com a paginação (por padrão, 1);
#### * Verifica no S3 da AWS se já foi criado o arquivo com os parâmetros do header criado
#### * Acessa o segredo salvo no Secrets Manager com o token de acesso à API
#### * Faz o requerimento utilizando biblioteca Requests à API com o token e header gerado
#### * Salva o objeto recebido no S3 da AWS clusterizando por código IBGE, ano e mês


### Entendendo a estrutura:

* Na pasta [**bolsaFamilia**](https://github.com/jonesamandajones/bolsa-familia/tree/main/bolsaFamilia) temos o arquivo [lambda_function.py](https://github.com/jonesamandajones/bolsa-familia/blob/main/bolsaFamilia/lambda_function.py) com o código que estamos
elaborando, e nos arquivos [make_parameters.py](https://github.com/jonesamandajones/bolsa-familia/blob/main/bolsaFamilia/make_parameters.py) e [s3_verify.py](https://github.com/jonesamandajones/bolsa-familia/blob/main/bolsaFamilia/s3_verify.py) o início da separação em módulos do programa (que ainda não foi feita, então pode ignorar ou continuar).

* Na pasta [codigosIbge](https://github.com/jonesamandajones/bolsa-familia/tree/main/codigosIbge) temos o arquivo [get_ibge_codes.py](https://github.com/jonesamandajones/bolsa-familia/blob/main/codigosIbge/get_ibge_codes.py) que puxa os dados da API do IBGE por região.
O arquivo [create_csv_codes.py](https://github.com/jonesamandajones/bolsa-familia/blob/main/codigosIbge/create_csv_codes.py) como o nome já diz, cria o ibge_codes.csv com todos os códigos IBGE contido nos dados, usados no eader do requerimento para a API gov.br no Lambda Function.

* Na pasta [docker](https://github.com/jonesamandajones/bolsa-familia/tree/main/docker) temos o docker-compose formatado para utilizar pyspark em nossas futuras análises. Os códigos nãoe estão testados, apenas mockados.
