import requests, json, urllib, os
from datetime import datetime, date

def get_citations(id):
    ## Construct API Call
    apicall = ('https://api.openalex.org/works?filter=author.id:{}&per_page=200'.format(id))
    #  Open api call url and assign to variable
    dirtywork = urllib.request.urlopen(apicall)
    #  Convert to json
    work = json.load(dirtywork)
    citations = []
    for i in work['results']:
        citation_call = (i['cited_by_api_url'])
        call_request = urllib.request.urlopen(citation_call)
        citation_work = json.load(call_request)
        for j in citation_work['results']:
            authors = []
            for k in j['authorships']:
                authors.append(k['author']['id'])
            if id not in authors and j['id'] not in citations:
                citations.append(j['id'])
            authors = []


    return citations

print('Number of non-self-cited works: ' + str(len(get_citations('A2302606219'))))
for i in get_citations('A2302606219'):
    print(i)