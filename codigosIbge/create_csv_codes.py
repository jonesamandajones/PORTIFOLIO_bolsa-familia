import json
import pandas as pd


regioes = [1, 2, 3, 4, 5]
data = []
for regiao in regioes:
    key = f'dados_ibge/dados_ibge_regiao={regiao}.json'

    with open(key, 'r') as ibge_data:

        data_dict = json.loads(ibge_data.read())
        index = len(data_dict) - 1

        for i in range(index):
            data.append(data_dict[i]['id'])

print(data)
df = pd.DataFrame(data)
csv_data = df.to_csv('ibge_codes.csv', index=False)








