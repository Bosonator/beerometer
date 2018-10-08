import requests
from bs4 import BeautifulSoup

url = 'https://craftbeermarket.ca/vancouver/fresh-beer'

craft_r = requests.get(url)
craft_soup = BeautifulSoup(craft_r.text, 'html.parser')

# Product listings are semi-formatted, manually, and grouped into "globs"
# of info that contain an arbitrary number of individual beer entries.
product_globs = craft_soup.findAll('div', {'class': 'laptop-4 unit items'})

beerpars = dict(name='', desc='', orig='', volumes='', prices='')
beerlist = []

gcount = 0  # Count the globs

for glob in product_globs:
    gcount += 1


    n = 0  # list counter, reset for each new glob
    b = 0  # beer counter, several beers in a glob
    d = 0  # dict items counter, for filling beerpar
    nelements = glob.contents.__len__()  # total list elements; WTF is this format?

    while n < nelements:
        if glob.contents[n].name == 'h3':
            b += 1
            print('New beer found at glob {0}, list position{1}!'.format(gcount, n))
            name = glob.contents[n].text
            d = 1  # Start counting entries in beerpars dict

        if glob.contents[n].name == 'p':  # Skip lines until a <p> heading is hit, then parse further.
            strval = glob.contents[n].text

            if d == 1:
                desc = glob.contents[n].text
            elif d == 2:
                orig = glob.contents[n].text
            elif d == 3:
                volumes = glob.contents[n].text
            elif d == 4:
                prices = glob.contents[n].text
                beerlist.append({'name': name.lstrip(),
                                 'desc': desc.lstrip(),
                                 'orig': orig.lstrip(),
                                 'volumes': volumes.lstrip(),
                                 'prices': prices.lstrip()})  # Have to append a nameless dictionary;
                #  otherwise, the dict. items change as the original variable changes.
                print("Info. assignment complete, {0}".format(name))
            else:
                print('More content than "beerpars" dict entries. (Beer: {0})'.format(name))

            d += 1

        n += 1  # Increment list counter, glob contents

    # Finished all list items in glob.

# Finished all globs.
print('Total globs analyzed: {0}'.format(gcount))
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
