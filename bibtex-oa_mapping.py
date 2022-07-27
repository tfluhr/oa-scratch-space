import requests, json, urllib, os, sys, math, time
from urllib.error import URLError
from datetime import date

## example doi: 'doi.org/10.1016/S0006-3207(02)00392-0'

def get_citations(doi):
    ## Construct API Call
    apicall = ('https://api.openalex.org/works/{}'.format(doi))
    #  Open api call url and assign to variable
    dirtywork = urllib.request.urlopen(apicall)
    #  Convert to json
    work = json.load(dirtywork)
    cited_ref_api = work['cited_by_api_url']
    dirtywork.close()
    print(cited_ref_api)
    doubledirtywork = urllib.request.urlopen(str(cited_ref_api))
    tripledirtywork = json.load(doubledirtywork)
    reference_list = []
    for ref in tripledirtywork['results']:
        reference_list.append(ref['doi'])
    return reference_list

def bibtext_oa_conversion(dois):
    openalex_dir = r'C:\tmp\openalex\DOI'
    numrefs = len(dois)
    counter = 0
    while counter < numrefs:
          for i in dois:
              counter += 1
              if i == None:
                  print("No DOI Found for citation number " + str(counter))
                  continue
              apicall = ('https://api.openalex.org/works/{}'.format(i))
              f = urllib.request.urlopen(apicall)
              oa_work = json.load(f)
              oa_work_pub_date = date.fromisoformat(oa_work['publication_date'])

              ## mapping data from OpenAlex fields to BibTeX fields
              bibtex_entrytype = (oa_work['type'])
              bibtex_citekey = oa_work['authorships'][0]['author']['display_name'].split()[-1] +\
                               str(oa_work['publication_year']) +\
                               str((oa_work['title']).split()[0])

              ## BibTeX entry type mapping. OpenAlex uses the Crossref controlled vocabulary for works types, but this field is
              ## under development by the OpenAlex team. This is my best approximation for a crosswalk between
              ## BibTeX and OpenAlex (Crossref) works types.
              bibtex_entry_type_map = {'journal-article' : 'article',
                                       ('book-section', 'monograph') : 'book',
                                       ('book-track', 'book-part', 'book-chapter', 'book-series') : 'inbook',
                                       ('proceedings-article', 'proceedings-series') : 'inproceedings',
                                      'dissertation' : 'phdthesis'}

              ## BibTeX Dictionary of mapped values

              bibtex_mapping = {'title'                : oa_work['title'],
                                'author'               : oa_work['authorships'][0]['author']['display_name'],
                                'publisher'            : oa_work['host_venue']['publisher'],
                                'doi'                  : oa_work['doi'],
                                'issn'                 : oa_work['host_venue']['issn_l'],
                                'journal'              : oa_work['host_venue']['display_name'],
                                'month'                : oa_work_pub_date.strftime("%b").lower(),
                                'number'               : oa_work['biblio']['issue'],
                                'pages'                : str(oa_work['biblio']['first_page']) + str(oa_work['biblio']['last_page']),
                                'type'                 : oa_work['type'],
                                'url'                  : oa_work['host_venue']['url'],
                                'volume'               : oa_work['biblio']['volume'],
                                'year'                 : oa_work['publication_year']}

              ## create a folder for output files if one doesn't exist
              isExist = os.path.exists(openalex_dir)
              if not isExist:
                  os.makedirs(openalex_dir)
                  print("Created new directory for your files")

              ## Try to put together a BibTeX citation

              def is_in_bibtex_entry(my_key):
                  for key, val in bibtex_entry_type_map.items():
                      if my_key in key:
                          return val

              bibtex_pretext = '@' + str(is_in_bibtex_entry(bibtex_entrytype)) + '{' + bibtex_citekey + ","
              # print(bibtex_pretext)
              file = open(openalex_dir + "\\" + str(date.today()) + ".bib", 'a', encoding='utf-8')
              file.writelines(bibtex_pretext + '\n')

              for i,j in bibtex_mapping.items():
                    if i == None:
                          continue
                    elif j == None:
                          continue
                    else:
                          line = str(i) + " = " + '{' + str(j) + "},"
                          # print(line)
                          file.writelines(line + '\n')
              file.writelines("}\n\n")
              # print("}")
          print("Citation export complete.")



my_citations = get_citations('doi.org/10.1016/S0006-3207(02)00392-0')
bibtext_oa_conversion(my_citations)

