import pandas as pd
df = pd.read_csv('wal_data.csv')
#print (df)
js = df.to_json(orient='records')

import json
# jd = { 'data': js}
# with open('datahack.json', 'w') as outfile:
# 	json.dump(jd,outfile)
print (js)