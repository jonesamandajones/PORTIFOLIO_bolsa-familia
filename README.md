# bolsa-familia

### Entendendo a estrutura:

* Na pasta [**bolsaFamilia**](https://github.com/jonesamandajones/bolsa-familia/tree/main/bolsaFamilia) temos o arquivo [lambda_function.py](https://github.com/jonesamandajones/bolsa-familia/blob/main/bolsaFamilia/lambda_function.py) com o código que estamos
elaborando, e nos arquivos [make_parameters.py](https://github.com/jonesamandajones/bolsa-familia/blob/main/bolsaFamilia/make_parameters.py) e [s3_verify.py](https://github.com/jonesamandajones/bolsa-familia/blob/main/bolsaFamilia/s3_verify.py) o início da separação em módulos do programa (que ainda não foi feita, então pode ignorar ou continuar).

* Na pasta [codigosIbge](https://github.com/jonesamandajones/bolsa-familia/tree/main/codigosIbge) temos o arquivo [get_ibge_codes.py](https://github.com/jonesamandajones/bolsa-familia/blob/main/codigosIbge/get_ibge_codes.py) que puxa os dados da API do IBGE por região.
O arquivo [create_csv_codes.py](https://github.com/jonesamandajones/bolsa-familia/blob/main/codigosIbge/create_csv_codes.py) como o nome já diz, cria o ibge_codes.csv com todos os códigos IBGE contido nos dados, usados no eader do requerimento para a API gov.br no Lambda Function.

* Na pasta [docker](https://github.com/jonesamandajones/bolsa-familia/tree/main/docker) temos o docker-compose formatado para utilizar pyspark em nossas futuras análises. Os códigos nãoe estão testados, apenas mockados.
