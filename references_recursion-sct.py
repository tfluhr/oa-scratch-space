# Declare some stuff
import requests, json, urllib, os, sys, math, pandas

header = "mailto=sarah.thorngate@gmail.com"
seed = "https://openalex.org/W2073788864"
big_df = pandas.DataFrame(columns=['OAID', 'count', 'references'])
nope_list = []

def get_work(oaid):
    ## Construct API Call
    apicall = ('https://api.openalex.org/works/{}{}'.format(oaid, header))
    #  Open api call url and assign to variable
    dirtywork = urllib.request.urlopen(apicall)
    #  Convert to json
    work = json.load(dirtywork)
    print(apicall)
    return work

def check_references(reflist):
    global big_df
    for r in reflist:
        if r not in big_df.OAID.tolist() and r not in nope_list:
            rwork = get_work(r)
            if rwork['cited_by_count'] > 2000:
                df = {'OAID': r, 'count': 0, 'references': rwork['referenced_works']}
                big_df = big_df.append(df, ignore_index = True)
                print(len(big_df))
            else:
                nope_list.append(r)
                print(len(nope_list))

#get things started with the seed document                
work = get_work(seed)
check_references(work['referenced_works'])

#then loop through each work's references
for i in big_df.references.tolist():
    check_references(i)




