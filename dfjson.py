import requests, json, pandas

from io import StringIO

url = "https://api.openalex.org/works?page=2&per-page=2"
headers = {'user-agent': 'mailto:sarah.thorngate@gmail.com'}

###API Call
response = requests.get(url, headers=headers)
print(response.status_code)

results = response.json()['results']

###Convert json to dataframe
def jdf(obj):
    #first it has to be a string
    s = json.dumps(obj, sort_keys=True, indent=4)
    df = pandas.read_json(StringIO(s))
    return df
    
results_df = jdf(results)

###Select the columns worth keeping into a new dataframe

cites_df = results_df[['id', 'cited_by_api_url', 'publication_year', 'referenced_works']].copy()











