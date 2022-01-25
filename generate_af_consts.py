#!/bin/python3.9

import json

DST_PATH = '../airflow/plugins/consts.py'
result = []

with open('metadata/indicators_worldbank.json', 'r') as f:
    for elem in json.load(f):
        result.append({
            'name': elem['data_table'],
            'id': elem['url_source'].split('/')[-1],
        })

with open(DST_PATH, 'w') as f:
    f.write('WORLDBANK_INDICATORS = {}'.format(result))
