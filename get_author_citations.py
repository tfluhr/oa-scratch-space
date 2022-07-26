import requests, json, urllib, os
from datetime import datetime, date

## This function accepts an author OAID and returns a list of referencing works that are not self-citations.
## It also checks author display names and flags works that have authors with different OAIDs but the same 
## display name.

## The function returns a list with three elements:
## Element 1: A list containing works that are clear non-self-citations.
## Element 2: A string that warns the user about citations which may be self-citations.
## Element 3: A list of citations that may be self-citations based on author display name.

def get_citations(id):
    ## Get author display name
    apicall_name = ('https://api.openalex.org/{}'.format(id))
    #  Open api call url and assign to variable
    name_dirtywork = urllib.request.urlopen(apicall_name)
    #  Convert to json
    name_work = json.load(name_dirtywork)
    display_name = name_work['display_name']

    ## Construct API Call
    apicall = ('https://api.openalex.org/works?filter=author.id:{}&per_page=200'.format(id))
    #  Open api call url and assign to variable
    dirtywork = urllib.request.urlopen(apicall)
    #  Convert to json
    work = json.load(dirtywork)
    citations = []
    citations_flag = []
    citations_caution = 'CAUTION: The following works may be self-citations based on one or more author names. Please check authorships.'

   ## Check each referencing work for a self-citation.
    for i in work['results']:
        citation_call = (i['cited_by_api_url'])
        call_request = urllib.request.urlopen(citation_call)
        citation_work = json.load(call_request)
        for j in citation_work['results']:
            authors = []
            authors_flag = []
            for k in j['authorships']:
                ## Check to see if any works have an author with the same display name but a different OAID
                if k['author']['id'] != ('https://openalex.org/' + str(id)) and k['author']['display_name'] == display_name:
                    authors_flag.append(j['id'])
                else:
                    authors.append(k['author']['id'])
            if id not in authors and j['id'] not in citations:
                if j['id'] in authors_flag and j['id'] not in citations:
                    if j['id'] not in citations_flag:
                        citations_flag.append(j['id'])
                else:
                    citations.append(j['id'])
            authors = []
            authors_flag = []
    output = [citations, citations_caution, citations_flag]
    return output

my_author = 'A2302606219'
print('Number of non-self-cited works: ' + str(len(get_citations(my_author)[0])) + len(get_citations(my_author[2])))
for i in get_citations(my_author)[0]:
    print(i)
print(get_citations(my_author)[1])
for i in get_citations(my_author)[2]:
    print(i)
