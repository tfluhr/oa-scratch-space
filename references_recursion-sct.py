# Declare some stuff
import requests, json, urllib, os, sys, math, pandas, itertools
from datetime import date

headers = {'user-agent': 'mailto:sarah.thorngate@gmail.com'} 
seed = ["https://openalex.org/W4225943155"]
big_df = pandas.DataFrame(columns=['OAID', 'count', 'references'])
nope_list = []
current_year = date.today().year

def get_works(oaid_list):
    ## Construct API Call
    bigolstring = '|'.join(oaid_list)
    apicall = ('https://api.openalex.org/works?per-page=50&filter=openalex:{}'.format(bigolstring))
    print(apicall)
    dirtywork = urllib.request.urlopen(apicall)
    worksplus = json.load(dirtywork)
    works = worksplus['results']
    return works
    
def check_references(reflist):
    global big_df
    global nope_list
    newrefs = []
    print(len(newrefs))
    for r in reflist:
        if r in big_df.OAID.tolist():
            print("good match")
            #get index of r in list
            #use index to increment count
            #big_df.count = big_df.count + 1
        elif r in nope_list:
            print("bad match")
        if r not in big_df.OAID.tolist() and r not in nope_list:
            newrefs.append(r)
            #print(len(newrefs))
            #need to come back and limit this to 50...also should maximize it so that 50 items get sent each time
    print(len(newrefs))
    #let's say newrefs is 51 items long, so we need to send two batches
    listreflists = []
    a = list(range(math.ceil(len(newrefs)/50)))
    for x in a:
        batch = newrefs[x*50:x*50 + 50]
        rworks = get_works(batch)
            #I'll need to rewrite this to iterate through each work in rworks
            #calculate a ratio of citations to years since pub to use as a threshold filter
        for w in rworks:
            yip = current_year - w['publication_year']
            expected_cites = yip*(4 + 4*yip)
            if w['cited_by_count'] > expected_cites:
                df = {'OAID': w['id'], 'count': 1, 'references': w['referenced_works']}
                big_df = big_df.append(df, ignore_index = True)
                listreflists.append(w['referenced_works'])
            else:
                nope_list.append(w['id'])
                print("no " + str(len(nope_list)))
    mergedrefs = list(set(list(itertools.chain.from_iterable(listreflists))))
    return mergedrefs


#1 Get the references from the seed document as a list
seedwork = get_works(seed)
seedlist = seedwork[0]['referenced_works']
#2 get them and check to see if they meet parameters for inclusion
#2a add them to big df if so, to nope list if no
take1 = check_references(seedlist)
#3 for each new item in big_df, check the reference list and include/exclude
####need to rewrite this as a loop with some sort of stop limit
take2 = check_references(take1)
take3 = check_references(take2)
take4 = check_references(take3)

