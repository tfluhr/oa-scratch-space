# Declare some stuff
import requests, json, urllib, os, sys, math, pandas
from datetime import date

header = "mailto=sarah.thorngate@gmail.com"
seed = "https://openalex.org/W4225943155"
big_df = pandas.DataFrame(columns=['OAID', 'count', 'references'])
nope_list = []
current_year = date.today().year


def get_work(oaid):
    ## Construct API Call
    apicall = ('https://api.openalex.org/works/{}{}'.format(oaid, header))
    #  Open api call url and assign to variable
    dirtywork = urllib.request.urlopen(apicall)
    #  Convert to json
    work = json.load(dirtywork)
    #print(apicall)
    return work

def check_references(reflist):
    global big_df
    for r in reflist:
        if r in big_df.OAID.tolist():
            print("good match")
            #get index of r in list
            #use index to increment count
            #big_df.count = big_df.count + 1
        elif r in nope_list:
            print("bad match")
        elif r not in big_df.OAID.tolist() and r not in nope_list:
            rwork = get_work(r)
            #calculate a ratio of citations to years since pub to use as a threshold filter
            yip = current_year - rwork['publication_year']
            expected_cites = yip*(5 + 5*yip)
            if rwork['cited_by_count'] > expected_cites:
                df = {'OAID': r, 'count': 1, 'references': rwork['referenced_works']}
                big_df = big_df.append(df, ignore_index = True)
                print("yes " + str(len(big_df)))
            else:
                nope_list.append(r)
                print("no " + str(len(nope_list)))

#get things started with the seed document                
work = get_work(seed)
check_references(work['referenced_works'])

#then loop through each work's references
#Why is this only going one time through? I want it to go through multiple times. 
for x in range(2):
    print("**********************************************")
    for i in big_df.references:
        check_references(i)

    




