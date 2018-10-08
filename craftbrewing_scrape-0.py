import requests
from bs4 import BeautifulSoup

url = 'https://craftbeermarket.ca/vancouver/fresh-beer'

craft_r = requests.get(url)
craft_soup = BeautifulSoup(craft_r.text, 'html.parser')

# Product listings are semi-formatted, manually, and grouped into "globs" of info that contain an arbitrary number of
# individual beer entries.
product_globs = craft_soup.findAll('div', {'class': 'laptop-4 unit items'})

beerpars = dict(name='', desc='', orig='', volumes='', prices='')
beerlist = []

gcounter = 0 # Count the globs
for glob in product_globs:
    gcounter += 1
    # Reset line counter for each glob
    n = 0
    nelements = glob.contents.__len__()  # WTF is this format?
    while n < nelements:
        if glob.contents[n].name == 'h3':
            print('New beer found at {0}!'.format(n))
            name = glob.contents[n].text
            n += 1
            filledfields = 1
            while filledfields < 5:
                if glob.contents[n].name == 'p':
                    strval = glob.contents[n].text
                    if filledfields == 1:
                        desc = strval; filledfields += 1
                    elif filledfields == 2:
                        orig = strval; filledfields += 1
                    elif filledfields == 3:
                        volumes = strval; filledfields += 1
                    elif filledfields == 4:
                        prices = strval; filledfields += 1
                else:
                    filledfields += 1

            print("Beer {0} assignment complete".format(name))
            beerlist.append({'name': name,
                             'desc': desc,
                             'orig': orig,
                             'volumes': volumes,
                             'prices': prices})  # Have to append a nameless dictionary;
            #  otherwise, the dict. items change as the original variable changes.

            n += 1

print('Total globs analyzed: {0}'.format(gcounter))
print('Total beers captured: {0}'.format(len(beerlist)))



# file_path = 'yelp-{loc}-2.txt'.format(loc=loc)
# with open(file_path, "a") as textfile:
#     businesses = yelp_soup.findAll('div', {'class': 'biz-listing-large'})
#     for biz in businesses:
#         #print(biz)
#         title = biz.findAll('a', {'class': 'biz-name'})[0].text
#         print(title)
#         second_line = ""
#         first_line = ""
#         try:
#             address = biz.findAll('address')[0].contents
#             for item in address:
#                 if "br" in str(item):
#                     #print(item.getText())
#                     second_line += item.getText().strip(" \n\t\r")
#                 else:
#                     #print(item.strip(" \n\t\r"))
#                     first_line = item.strip(" \n\t\r")
#             print(first_line)
#             print(second_line)
#         except:
#             pass
#         print('\n')
#         try:
#             phone = biz.findAll('span', {'class': 'biz-phone'})[0].getText().strip(" \n\t\r")
#         except:
#             phone = None
#         print(phone)
#         page_line = "{title}\n{address_1}\n{address_2}\n{phone}\n\n".format(
#                 title=title,
#                 address_1=first_line,
#                 address_2=second_line,
#                 phone = phone
#             )
#         textfile.write(page_line)
