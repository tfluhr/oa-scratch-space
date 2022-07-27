import requests, json, urllib
from datetime import datetime, date

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

    ## call the OpenAlex api for a JSON of the work metadata
    apicall = ('https://api.openalex.org/works/{}'.format(oaid))
    f = urllib.request.urlopen(apicall)
    oa_work = json.load(f)
    oa_work_pub_date = date.fromisoformat(oa_work['publication_date'])

    ### MAPPING DATA FROM OPENALEX TO BIBTEX FIELDS ###

    ## "type" field value error handling
    def is_in_bibtex_entry(my_key):
        for key, val in bibtex_entry_type_map.items():
            if my_key == None:
                return 'null'
            elif my_key in key:
                return val

    ## set up "author" field value
    def get_author():
        author_field = ''
        if oa_work['authorships']:
            author_field = str(oa_work['authorships'][0]['author']['display_name'])
            return author_field
        else:
            author_field == 'null'
            return author_field


    ## BibTeX entry "type" mapping. OpenAlex uses the Crossref controlled vocabulary for works "types", but this field is
    ## under development by the OpenAlex team. This is my best approximation for a crosswalk between
    ## BibTeX and OpenAlex (Crossref) works "types".
    bibtex_entry_type_map = {'journal-article': 'article',
                             ('book-section', 'monograph'): 'book',
                             ('book-track', 'book-part', 'book-chapter', 'book-series'): 'inbook',
                             ('proceedings-article', 'proceedings-series'): 'inproceedings',
                             'dissertation': 'phdthesis'}


    ## check for the presence of page numbers and set up the "page numbers" fields
    oa_first_page = oa_work['biblio']['first_page']
    oa_last_page = oa_work['biblio']['last_page']
    oa_page_numbers_draft = str(oa_first_page) + ', ' + str(oa_last_page)
    oa_page_numbers = ''

    if oa_page_numbers_draft == 'None, None':
        oa_page_numbers = 'null'
    else:
        oa_page_numbers = oa_page_numbers_draft

    ## BibTeX Dictionary of mapped values
    bibtex_mapping = {'title': oa_work['title'],
                      'author': get_author(),
                      'publisher': oa_work['host_venue']['publisher'],
                      'doi': oa_work['doi'],
                      'issn': oa_work['host_venue']['issn_l'],
                      'journal': oa_work['host_venue']['display_name'],
                      'month': oa_work_pub_date.strftime("%b").lower(),
                      'number': oa_work['biblio']['issue'],
                      'pages': oa_page_numbers,
                      'type': is_in_bibtex_entry(oa_work['type']),
                      'url': oa_work['host_venue']['url'],
                      'volume': oa_work['biblio']['volume'],
                      'year': oa_work['publication_year']}


    ### CONSTRUCTING THE BIBTEX CITATION ###

    ## set up the citation key and pretext

    if get_author():
        bibtex_citekey = get_author().split()[-1] + \
                         str(oa_work['publication_year']) + \
                         str((oa_work['title']).split()[0])
    else:
        bibtex_citekey = str(oa_work['title'].split()[0]) + \
                     str(oa_work['publication_year']) + \
                     str((oa_work['title']).split()[-1])

    bibtex_entrytype = (oa_work['type'])
    bibtex_pretext = '@' + str(is_in_bibtex_entry(bibtex_entrytype)) + '{' + bibtex_citekey + ",\n"
    bibtex_citation_str = bibtex_pretext

    ## error handling for missing data in the OpenAlex JSON and
    ## constructing the BibTeX citation string
    for i, j in bibtex_mapping.items():
        if i == None:
            continue
        elif j == None or j == 'null':
            continue
        else:
            line = str(i) + " = " + '{' + str(j) + "},\n"
            bibtex_citation_str += line
    bibtex_citation_str += '}'

    ## return the completed BibTeX citation as a string
    return bibtex_citation_str





# my_citations = get_citations('doi.org/10.1016/S0006-3207(02)00392-0')

openalex_dir = r'C:\tmp\openalex\DOI'
now = datetime.now()
filename = now.strftime('%d-%m-%y-%H-%M-%S')
file = open(openalex_dir + "\\" + str(filename) + ".bib", 'a', encoding='utf-8')

openalexid = input('Enter a DOI, OpenAlex, MAG, PMID, or PMCID: ')

oarefs = get_citations(openalexid)

print(oarefs)

for i in oarefs:
    bibtex_citation = bibtext_oa_conversion(i)
    print(bibtex_citation)
    file.writelines(bibtex_citation + "\n\n")
