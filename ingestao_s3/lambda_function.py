import boto3
import json
import requests
import pandas as pd
import io


from botocore.exceptions import ClientError


def get_secret():

    secret_name = "token-gov"
    region_name = "us-east-1"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    header = json.loads(get_secret_value_response['SecretString'])
    return header

def get_data_from_gov(header, parameters, url):

    data = requests.get(url=url, headers=header, params=parameters)
    return data

def read_ibge_codes():
    ibge_codes = []
    bucket = 'bucket-bolsa-familia'
    s3 = boto3.resource('s3')
    object_key = 'dados_ibge/ibge_codes.csv'
    obj = s3.Object(bucket, object_key)
    data = obj.get()['Body'].read()
    ibge_codes.append(
        pd.read_csv(
            io.BytesIO(data), header=0, delimiter=',', low_memory=False, usecols=[0]))

    return ibge_codes


def make_list_codigoIbge(ibge_codes):
    df_ibge = ibge_codes[0]
    list_code = []
    for row in range(len(df_ibge)):
        list_code.append(df_ibge.iloc[row][0])
    return list_code


def year_list():
    anos = []
    ano = ''
    for year in range(2010, 2023):
        ano = str(year)
        anos.append(ano)
        year +=1
    return anos


def multiply_year_for_100(anos):
    anos_mult = []
    for y in anos:
        y = int(y)*100
        anos_mult.append(y)
    return anos_mult


def make_list_of_mesAno(anos_mult):
    contador = 0
    mes = list(range(1, 13))
    list_mesAno = []
    while contador < len(anos_mult):
        for y in anos_mult:
            for m in mes:
                ano_soma_mes = lambda y, m: y + m
                list_mesAno.append(ano_soma_mes(y, m))
        contador +=1
    return list_mesAno


def list_obj_in_s3():
    s3 = boto3.client('s3')
    obj_in_s3 = []
    kwargs = {'Bucket': 'bucket-bolsa-familia',
              'Prefix': 'bolsa'}
    while True:
        objects = s3.list_objects_v2(**kwargs)

        for obj in objects['Contents']:
            obj_in_s3.append(obj['Key'])

        try:
            kwargs['ContinuationToken'] = objects['NextContinuationToken']

        except KeyError:
            break
    return obj_in_s3


def file_to_verify(codigoIbge, mesAno):

    file_to_ver = f'bolsa_familia/codigo_ibge={codigoIbge}/ano={mesAno[:4]}/mes={mesAno[4:]}/data_{codigoIbge}_{mesAno}.json'
    return file_to_ver


def verify_mesAno_s3(list_mesAno, list_update_codes, obj_in_s3):

    codigoIbge = list_update_codes[0]
    str_list_date = [str(dat) for dat in list_mesAno]
    list_date_update = [date for date in str_list_date if file_to_verify(codigoIbge, date) not in obj_in_s3]

    return list_date_update


def verify_codigoIbge_s3(list_code, obj_in_s3):

    mesAno = '202212'
    str_list_code = [str(cod) for cod in list_code]
    list_code_update = [code for code in str_list_code if file_to_verify(codigoIbge=code, mesAno=mesAno) not in obj_in_s3]

    return list_code_update


def define_parameters(list_code, list_mesAno):

                parameters = {'codigoIbge': list_code[0],
                            'mesAno': int(list_mesAno[0]),
                            'pagina': 1}
                return parameters


def create_file(parameters, data):

    s3 = boto3.client('s3')
    bucket = 'bucket-bolsa-familia'
    str_mesAno = str(parameters['mesAno'])
    codigoIbge = parameters['codigoIbge']
    name_file = f'bolsa_familia/codigo_ibge={codigoIbge}/ano={str_mesAno[:4]}/mes={str_mesAno[4:]}/data_{codigoIbge}_{str_mesAno}.json'
    bytes_data = bytes(json.dumps(data.json(), ensure_ascii=False), encoding='utf8')
    saved_data = s3.put_object(Bucket=bucket, Key=name_file, Body=bytes_data)

    return saved_data


def lambda_handler():
    contador = 1
    header = get_secret()
    url = 'https://api.portaldatransparencia.gov.br/api-de-dados/bolsa-familia-por-municipio'
    anos = year_list()
    anos_mult = multiply_year_for_100(anos=anos)
    list_mesAno = make_list_of_mesAno(anos_mult=anos_mult)
    ibge_codes = read_ibge_codes()
    list_code = make_list_codigoIbge(ibge_codes=ibge_codes)

    while contador < len(list_mesAno):
        obj_in_s3 = list_obj_in_s3()
        listcode_update = verify_codigoIbge_s3(list_code=list_code, obj_in_s3=obj_in_s3)
        print(f'list code update: {listcode_update[0]}')
        list_mesAno_update = verify_mesAno_s3(list_mesAno=list_mesAno, list_update_codes=listcode_update, obj_in_s3=obj_in_s3)
        print(f'list mesano update: {list_mesAno_update[0]}')
        parameters = define_parameters(list_code=listcode_update, list_mesAno=list_mesAno_update)
        print(f'parameters: {parameters}')
        data = get_data_from_gov(header=header, parameters=parameters, url=url)
        saved_data = create_file(parameters=parameters, data=data)
        contador += 1
        if contador == 1700:
            break
    return saved_data





