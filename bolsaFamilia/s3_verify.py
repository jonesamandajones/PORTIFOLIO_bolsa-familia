import boto3
import json
import requests
import pandas as pd
import io

from botocore.exceptions import ClientError


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

