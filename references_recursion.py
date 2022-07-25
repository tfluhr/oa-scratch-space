from oa_functions import *

# Declare some stuff
import requests, json, urllib, os, sys, math
header = "mailto=tfluhr@iit.edu"
uid = "I180949307"
doi = "https://openalex.org/W2018078426"
big_list = []
def get_works_referenced(doi):
    ## Construct API Call
    apicall = ('https://api.openalex.org/works/{}{}'.format(doi, header))
    #  Open api call url and assign to variabl
    dirtywork = urllib.request.urlopen(apicall)
    #  Convert to json
    work = json.load(dirtywork)
    print(apicall)
    # Some logic - if there is some references work, add to big list
    if work['referenced_works']:
        print("there are some referenced works")
    else:
        print("no more references")
    for r in work['referenced_works']:
        if r not in big_list:
            big_list.append(r)
    print(len(big_list))

blah = get_works_referenced(doi)

for i in big_list:
#   print(i)
        get_works_referenced(i)
