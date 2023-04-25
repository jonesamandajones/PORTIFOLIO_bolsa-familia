import requests
import json


regioes = [1, 2, 3, 4, 5]
for regiao in regioes:
    url = f'https://servicodados.ibge.gov.br/api/v1/localidades/regioes/{regiao}/municipios'

    r = requests.get(url=url)

    with open(f'dados_ibge/dados_ibge_regiao={regiao}.json', 'w') as f:
        f.write(json.dumps(r.json(), ensure_ascii=False, indent=4))