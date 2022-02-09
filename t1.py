import trafilatura
import pandas as pd
# from .settings import DEFAULT_CONFIG, DOWNLOAD_THREADS, TIMEOUT

path = 'C:/Users/carol/Desktop/grab/grab/trafilatura/'
file = 'C:/Users/carol/Desktop/grab/grab/trafilatura/lot1.csv'

df = pd.read_csv(file).fillna('')


df = df[['index', 'base_url', 'final_url']]

results = pd.DataFrame()
for k,v in enumerate(df.values):


    downloaded = trafilatura.fetch_url(v[2])
    cleaned_body = trafilatura.extract(downloaded)
    try:
        cleaned_body = cleaned_body.replace('\n', '. ').replace('|', '').replace('  ',' ').replace('...', '.').replace('..', '.').strip('.')
    except:
        cleaned_body = ''
    elem = [k, v[0], v[1], v[2],  cleaned_body]
    temp = pd.DataFrame(elem).T
    results = pd.concat([results, temp], axis=0)
    if k % 500 == 0:
        print(k, 'done !')
        results.to_csv(path +'results/' + 'lot1_' + str(k) + '_.csv')
results.rename(columns=dict(zip(results.columns,['k', 'index', 'base_url', 'final_url', 'bocy_cleaned'])),inplace=True)
results.to_csv(path + 'final_lot1.csv')