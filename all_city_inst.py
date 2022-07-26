import requests, json, urllib, os, sys, math

# Use the following GitHub page for a dictionary of ISO Country Codes: https://github.com/pageflt/iso-country-codes
from iso_country_codes import CC_inv as CC

def all_city_institutions(header):
    i = 1  ## counter
    cursor = "*"
    openalex_dir = r'C:\tmp\openalex'
    country_input = input( 'Enter a country to search: ' )
    country_conv = CC[country_input.upper().strip('\u200e')]
    country = country_conv.lower()
    apicall = ('https://api.openalex.org/institutions?filter=country_code:{}&per_page=200&{}&cursor=*'.format(country, header, cursor))
    works_count = (requests.get(apicall).json()['meta']['count'])
    page_count = math.ceil(works_count/200)
    isExist = os.path.exists(openalex_dir)
    if not isExist:
        os.makedirs(openalex_dir)
        print("Created new directory for your files")
    while True:
        cursor = "*"
        inst_list = []
        inst_list_file = []
        city = input("Enter city for a list of institutions: ")
        if city == 'quit':
            break
        for i in range(1, page_count):
            apicall = (
                'https://api.openalex.org/institutions?filter=country_code:{}&per_page=200&{}&cursor={}'.format(
                    country, header, cursor))
            f = urllib.request.urlopen(apicall)
            x = json.load(f)
            cursor = x['meta']['next_cursor']
            for i in x['results']:
                if i['geo']['city'] == city:
                    inst_list.append(i['display_name'])
            f.close()
        print('Number of Institutions in ' + city + ': ' + str(len(inst_list)))
        for i in inst_list:
            inst_list_file.append(str(i) + "\n")
            print(i)
        print("\n")
        with open(openalex_dir + "\\" + str(city) + ".txt", 'w') as file:
            file.writelines('Number of Institutions in ' + city + ': ' + str(len(inst_list_file)) + '\n\n')
            file.writelines(inst_list_file)


all_city_inst = all_city_institutions('mailto=smurphy13@iit.edu')