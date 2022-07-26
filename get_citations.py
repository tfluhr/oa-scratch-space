import json, requests, urllib

def get_citations():
    ## Construct API Call
    doi = input("Enter a DOI, OpenAlex, MAG, PMID, or PMCID: ")
    apicall = ('https://api.openalex.org/works/{}'.format(doi))
    #  Open api call url and assign to variable
    dirtywork = urllib.request.urlopen(apicall)
    #  Convert to json
    work = json.load(dirtywork)
    reference_list = []
    for ref in work['referenced_works']:
        reference_list.append(ref)
    return reference_list

referenced_work = get_citations()

print(len(referenced_work), referenced_work)
