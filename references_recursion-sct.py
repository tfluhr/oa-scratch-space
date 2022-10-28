# Declare some stuff
import requests, json, urllib, os, sys, math, pandas, itertools
from datetime import date
headers = {'user-agent': 'mailto:sarah.thorngate@gmail.com'} 
current_year = date.today().year

#initiate containers to hold stuff
big_df = pandas.DataFrame(columns=['authorships', 'title', 'publication_year', 'biblio', 'referenced_works', 'cited_by_count', 'cited_by_api_url', 'OAID', 'doi'])
nope_list = []
#initiate a string to hold the list of concepts you'll used for screening
allconceptstring=""

####function to get the metadata for each work in a list of works, provided it shares at least one topic in common with the seed work.
def get_works(oaid_list):
    bigolstring = '|'.join(oaid_list)
    apicall = ('https://api.openalex.org/works?per-page=50&filter={}openalex:{}'.format(allconceptstring, bigolstring))
    dirtywork = urllib.request.urlopen(apicall)
    worksplus = json.load(dirtywork)
    works = worksplus['results']
    return works

#####function that gets metadata for works citing a list of works
#this generates a lot of refs real fast so it uses some filter parameters. 
#The default is that it only retrieves items that have been cited at least 10 times and that 
#match at least one 0 level topic and one lower level topic from the original seed article. 
def get_cites(oaid_list):
    cworks = []
    bigolstring = '|'.join(oaid_list)
    page = 1
    apicall = ('https://api.openalex.org/works?page={}&per-page=200&filter=cited_by_count:>10,{}{}cites:{}'.format(page, L0conceptstring, LLconceptstring, bigolstring))
    dirtywork = urllib.request.urlopen(apicall)
    worksplus = json.load(dirtywork)
    cworks.append(worksplus['results'])
    pages = math.ceil(worksplus['meta']['count'] / 200)
    for i in range(pages - 1):
        page = i + 2
        apicall = ('https://api.openalex.org/works?page={}&per-page=200&filter=cited_by_count:>10,{}{}cites:{}'.format(page, L0conceptstring, LLconceptstring, bigolstring))
        dirtywork = urllib.request.urlopen(apicall)
        worksplus = json.load(dirtywork)
        cworks.append(worksplus['results'])
    cworks_list = []
    for l in range(len(cworks)):
        for i in cworks[l]:
            cworks_list.append(i)
    return cworks_list
            
###########function that takes a list of references (as OAID) and citing works (full metadata), checks whether they meet inclusion parameters, and adds them to the appropriate df or list.
def check_references(reffed_list, citing_works):
    global big_df
    global nope_list
    ###referencedworks first. Check to see if we've already encountered this reference and call api if not.
    newworks = []
    newrefs = []
    for r in reffed_list:
        if r not in big_df.OAID.tolist() and r not in nope_list:
            newrefs.append(r)
    #split the list of new references up first because you have to do the api call in batches of no more than 50
    a = list(range(math.ceil(len(newrefs)/50)))
    for x in a:
        batch = newrefs[x*50:x*50 + 50]
        batchworks = get_works(batch)
        b = list(range(len(batchworks)))
        for y in b:
            newworks.append(batchworks[y])
    ###check to see if we've already encountered cited works next
    for c in citing_works:
        if c['id'] not in big_df.OAID.tolist() and c['id'] not in nope_list:
            newworks.append(c)   
    print("reffed and citers "+ str(len(newworks)))
    #Now we have a combined list of both referenced and citing works that we haven't encountered before, with full metadata. We'll further screen it by citation count and topic relevance.   
    listreflists = []
    check_citers = []
    for w in newworks:
        #calculate a ratio of citations to years since pub to use as a threshold filter
        yip = current_year - w['publication_year']
        expected_cites = yip*(2 + 2*yip)
        #if it meets the expected cites criteria, add it to the df, and add it's referenced works to a list, and add to the list for the cited by call
        #if not add it to the nope list.
        
        if w['cited_by_count'] > expected_cites:
            df = {
                'authorships': w['authorships'],
                'title': w['title'], 
                'publication_year': w['publication_year'],
                'biblio': w['biblio'],
                'referenced_works': w['referenced_works'], 
                'cited_by_count': w['cited_by_count'],
                'cited_by_api_url': w['cited_by_api_url'],
                'OAID': w['id'], 
                'doi': w['doi']
                }
            big_df = big_df.append(df, ignore_index = True)
            listreflists.append(w['referenced_works'])
            check_citers.append(w['id'])
        else:
            nope_list.append(w['id'])
    print("big_df "+ str(len(big_df)))
    print("listreflists " + str(len(listreflists)))
    print("check_citers " + str(len(check_citers)))
    print("nope_list " + str(len(nope_list)))
    #take the list of lists of references and merge them into a single deduped list for the next round. 
    reffed_list = list(set(list(itertools.chain.from_iterable(listreflists))))
    #batch process the citing works. these are trickier because there's no way to check for duplicates before making the API call.
    citing_works = []
    c = list(range(math.ceil(len(check_citers)/50)))
    print(c)
    for x in c:
        batch = check_citers[x*50:x*50 + 50]
        batchworks = get_cites(batch)
        b = list(range(len(batchworks)))
        for y in b:
            citing_works.append(batchworks[y])
        print("citing works " + str(len(citing_works)))
    return (reffed_list, citing_works)

####User inputs
#enter openalex url for a seed document
seed = ["https://openalex.org/W4225943155"]


##This stuff initiates things with the seed document
seedwork = get_works(seed)
seedlist = seedwork[0]['referenced_works']
seedconcepts = seedwork[0]['concepts']
allconcepts = []
L0concepts = []
LLconcepts = []
for i in list(range(len(seedconcepts))):
    allconcepts.append(seedconcepts[i]['id'])
    if seedconcepts[i]['level'] > 0 and float(seedconcepts[i]['score']) > 0.5:
        LLconcepts.append(seedconcepts[i]['id'])
    elif seedconcepts[i]['level'] == 0 and float(seedconcepts[i]['score']) > 0.3:
        L0concepts.append(seedconcepts[i]['id'])
allconceptstring = "concepts.id:" + '|'.join(allconcepts) + ","       
L0conceptstring = "concepts.id:" + '|'.join(L0concepts) + ","       
LLconceptstring = "concepts.id:" + '|'.join(LLconcepts) + ","   
seedcites = get_cites(seed)



test = check_references(seedlist, seedcites)
test1 = check_references(test[0], test[1])
test2 = check_references(test1[0], test1[1])






#while len(big_df) < 1000:
#    seedlist = check_references(seedlist)


#reffed_list = ["https://openalex.org/W2102028610"]
#testa = get_cites(reffed_list)

