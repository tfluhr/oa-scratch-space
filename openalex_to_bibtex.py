import requests, json, urllib, os, sys, math, time
from urllib.error import URLError
from datetime import date

## example doi: 'doi.org/10.1016/S0006-3207(02)00392-0'

def get_citations(id):
    ## Construct API Call
    apicall = ('https://api.openalex.org/works/{}'.format(id))
    #  Open api call url and assign to variable
    dirtywork = urllib.request.urlopen(apicall)
    #  Convert to json
    work = json.load(dirtywork)
    cited_ref_api = str(work['cited_by_api_url']) + '&per_page=200'
    dirtywork.close()
    print(cited_ref_api)
    doubledirtywork = urllib.request.urlopen(str(cited_ref_api))
    tripledirtywork = json.load(doubledirtywork)
    reference_list = []
    for ref in tripledirtywork['results']:
        reference_list.append(ref['id'])
    return reference_list

def bibtext_oa_conversion(oaid):
    apicall = ('https://api.openalex.org/works/{}'.format(oaid))
    f = urllib.request.urlopen(apicall)
    oa_work = json.load(f)
    oa_work_pub_date = date.fromisoformat(oa_work['publication_date'])

    ## mapping data from OpenAlex fields to BibTeX fields
    bibtex_entrytype = (oa_work['type'])
    bibtex_citekey = oa_work['authorships'][0]['author']['display_name'].split()[-1] + \
                     str(oa_work['publication_year']) + \
                     str((oa_work['title']).split()[0])

    ## BibTeX entry type mapping. OpenAlex uses the Crossref controlled vocabulary for works types, but this field is
    ## under development by the OpenAlex team. This is my best approximation for a crosswalk between
    ## BibTeX and OpenAlex (Crossref) works types.
    bibtex_entry_type_map = {'journal-article': 'article',
                             ('book-section', 'monograph'): 'book',
                             ('book-track', 'book-part', 'book-chapter', 'book-series'): 'inbook',
                             ('proceedings-article', 'proceedings-series'): 'inproceedings',
                             'dissertation': 'phdthesis'}

    def is_in_bibtex_entry(my_key):
        for key, val in bibtex_entry_type_map.items():
            if my_key == None:
                return 'null'
            elif my_key in key:
                return val

    ## BibTeX Dictionary of mapped values

    bibtex_mapping = {'title': oa_work['title'],
                      'author': oa_work['authorships'][0]['author']['display_name'],
                      'publisher': oa_work['host_venue']['publisher'],
                      'doi': oa_work['doi'],
                      'issn': oa_work['host_venue']['issn_l'],
                      'journal': oa_work['host_venue']['display_name'],
                      'month': oa_work_pub_date.strftime("%b").lower(),
                      'number': oa_work['biblio']['issue'],
                      'pages': str(oa_work['biblio']['first_page']) + ', ' + str(oa_work['biblio']['last_page']),
                      'type': is_in_bibtex_entry(oa_work['type']),
                      'url': oa_work['host_venue']['url'],
                      'volume': oa_work['biblio']['volume'],
                      'year': oa_work['publication_year']}

    ## Try to put together a BibTeX citation
    bibtex_pretext = '@' + str(is_in_bibtex_entry(bibtex_entrytype)) + '{' + bibtex_citekey + ",\n"

    bibtex_citation_str = bibtex_pretext

    for i, j in bibtex_mapping.items():
        if i == None:
            continue
        elif j == None:
            continue
        else:
            line = str(i) + " = " + '{' + str(j) + "},\n"
            bibtex_citation_str += line
    bibtex_citation_str += '}'

    return bibtex_citation_str





# my_citations = get_citations('doi.org/10.1016/S0006-3207(02)00392-0')

openalex_dir = r'C:\tmp\openalex\DOI'
file = open(openalex_dir + "\\" + str(date.today()) + ".bib", 'a', encoding='utf-8')

openalexid = 'https://openalex.org/W2000785263'

oarefs = get_citations('https://openalex.org/W2000785263')

for i in oarefs:
    bibtex_citation = bibtext_oa_conversion(i)
    print(bibtex_citation)
    file.writelines(bibtex_citation + "\n\n")

