import requests, json, urllib, os, sys, math, time
from datetime import date

## example doi: '10.1016/S0006-3207(02)00392-0'

def bibtext_oa_conversion(dois):
    for i in dois:
          openalex_dir = r'C:\tmp\openalex\DOI'

          apicall = ('https://api.openalex.org/works/doi={}'.format(i))
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
                                  'dissertation' : ('mastersthesis', 'phdthesis')}

          ## BibTeX Dictionary of mapped values

          bibtex_mapping = {'title'                : oa_work['title'],
                            'author'               : oa_work['authorships'][0]['author']['display_name'],
                            'publisher'            : oa_work['host_venue']['publisher'],
                            'doi'                  : oa_work['doi'],
                            'issn'                 : oa_work['host_venue']['issn'][0],
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

          bibtex_pretext = '@' + bibtex_entry_type_map[bibtex_entrytype] + '{' + bibtex_citekey + ","
          print(bibtex_pretext)
          file = open(openalex_dir + "\\" + str(date.today()) + ".bib", 'a', encoding='utf-8')
          file.writelines(bibtex_pretext + '\n')

          for i,j in bibtex_mapping.items():
                if j == 'null':
                      pass
                else:
                      line = str(i) + " = " + '{' + str(j) + "},"
                      print(line)
                      file.writelines(line + '\n')
          file.writelines("}\n\n")
          print("}")


my_dois = ('doi.org/10.1038/nature15254', 'doi.org/10.2217/fmb-2016-0070', 'doi.org/10.1038/nbt.3227')

bibtext_oa_conversion(my_dois)
