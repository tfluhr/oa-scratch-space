import requests, json, urllib, os, sys, math

## Use the following GitHub page for a dictionary of ISO Country Codes: https://github.com/pageflt/iso-country-codes
from iso_country_codes import CC_inv as CC

def all_city_institutions(header):
    i = 1  ## counter

    ## the cursor stores info about the page number of the API call
    cursor = "*"

    ## output directory
    openalex_dir = r'C:\tmp\openalex'

    ## ask for a country name; convert it to uppercase letters
    ## then retrieve the ISO country code
    ## and feed it to the API call
    country_input = input( 'Enter a country to search: ' )
    if country_input == 'quit':
        exit()
    country_conv = CC[country_input.upper().strip('\u200e')]
    country = country_conv.lower()


    ## first API call to get the number of results and pages
    apicall = ('https://api.openalex.org/institutions?filter=country_code:{}&per_page=200&{}&cursor=*'.format(country, header, cursor))
    works_count = (requests.get(apicall).json()['meta']['count'])
    page_count = math.ceil(works_count/200)

    ## create a folder for output files if one doesn't exist
    isExist = os.path.exists(openalex_dir)
    if not isExist:
        os.makedirs(openalex_dir)
        print("Created new directory for your files")

    ## main loop
    while True:

        ## reset the cursor key
        cursor = "*"

        ## empty lists that will contain institution names
        inst_list = []
        inst_list_file = []

        ## ask for a city name
        city = input("Enter city for a list of institutions: ")
        if city == 'quit':
            exit()

        ## loop to make an API call for each page of results from the initial country query
        ## save institution names that match the city query in a list object
        for i in range(1, page_count):
            apicall = (
                'https://api.openalex.org/institutions?filter=country_code:{}&per_page=200&{}&cursor={}'.format(
                    country, header, cursor))
            f = urllib.request.urlopen(apicall)
            x = json.load(f)

            ## set the cursor to pull the next page of results
            cursor = x['meta']['next_cursor']

            ## check the results for matches to the city query and add them to the list object
            for i in x['results']:
                if i['geo']['city'] == city:
                    inst_list.append(i['display_name'])

            ## close the JSON file when all matching results have been extracted
            f.close()

        ## print the total number of results
        print('Number of Institutions in ' + city + ': ' + str(len(inst_list)))

        ## save the entries in the main list to a new list that includes carriage returns for
        ## output to .txt
        for i in inst_list:
            inst_list_file.append(str(i) + "\n")
            print(i)
        print("\n")

        ## save the contents of the list to a .txt file named for the city query
        with open(openalex_dir + "\\" + str(city) + ".txt", 'w') as file:
            file.writelines('Number of Institutions in ' + city + ': ' + str(len(inst_list_file)) + '\n\n')
            file.writelines(inst_list_file)


all_city_inst = all_city_institutions('mailto=smurphy13@iit.edu')
