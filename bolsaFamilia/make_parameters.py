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
