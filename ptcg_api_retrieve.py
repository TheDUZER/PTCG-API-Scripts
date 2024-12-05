import os, requests
#import additional libraries for request timing as needed. Be a good person

"""
This script connects to https://pokemontcg.io through its API and downloads
an image scan of EVERY English Pokemon card and sorts them into
directories by set
"""

api_key = "insertapikeyhereorinanotherfileorwhatever"
cur_page = 1
headers = {'X-Api-Key': api_key}

#create main directory for file output
if 'output' not in os.listdir(os.path.curdir):
    os.mkdir(os.path.join(os.path.curdir, 'output'))

#breaks when request pagination ends
while True:
    card_data = requests.get(f"https://api.pokemontcg.io/v2/cards?page={cur_page}",
                             headers=headers)
    card_data_json = card_data.json()
    #issues break when 0 cards are left. not sure why I didn't do return False...
    if card_data_json['count'] == 0:
        print('Complete.')
        break
    print(f'Current Page: {cur_page}')
    #write image data to directory, plus text cleaning as needed
    for cards in card_data_json['data']:
        current_set = cards['set']['name'].replace(':', '')
        #make new subdirectory if current set directory does not exist
        if current_set not in os.listdir(os.path.join(os.path.curdir, "output")):
            os.mkdir(os.path.join(os.path.curdir, "output", current_set))
        if cards['id'].replace('?', '') + '_' + cards['name'].replace('?', '') + '.png' not in \
            os.listdir(os.path.join(os.path.curdir, "output", current_set)):
            new_card = requests.get(cards['images']['large'],
                                    headers=headers)
            #write serial data to image file
            with open(os.path.join(os.path.curdir, "output", current_set, 
                                   cards['id'].replace('?', '') + '_' + cards['name'].replace(\
                                        '?', '') + '.png'), 'wb+') as card_file:
                card_file.write(new_card.content)
    cur_page += 1