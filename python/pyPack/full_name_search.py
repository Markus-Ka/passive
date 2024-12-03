from .result_writing import check_existing_result
import requests
from bs4 import BeautifulSoup
import json


def launch_full_name_search(args):
    name_array = args[1].split()
    name_string = ''
    i = 0
    while i < len(name_array):
        if i != 0:
            name_string += ' '
        name_string += name_array[i]
        i += 1

    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    params = {
        'what': name_string,
        'where': '',
    }

    response = requests.get('https://www.whitepages.be/Search/Person/', params=params, headers=headers)

    if response.status_code == 200:    
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            results = soup.find_all('div', {"itemprop": "itemListElement"})
            result_string = ''
            i = 1
            for result in results:

                small_result = result.get('data-small-result')
                
                if small_result:
                    small_result_data = json.loads(small_result)
                    full_name = small_result_data.get('title')
                    phone = small_result_data.get('phone')

                    name_parts = full_name.split()
                    
                    first_name = name_parts[0]
                    if first_name.lower() != name_array[0].lower():
                        continue                
                    
                    last_name = name_parts[-1]
                    if last_name.lower() != name_array[-1].lower():
                        continue
                    
                    middle_names = name_parts[1:-1] if len(name_parts) > 2 else []

                    address = result.find('span', {"class": "wg-address"}).text.strip()
                    
                    result_string += f"First name: {first_name}\n"
                    if middle_names:
                        for idx, middle_name in enumerate(middle_names, 1):
                            result_string += f"Middle name_{idx}: {middle_name}\n"
                    result_string += f"Last name: {last_name}\n"
                    result_string += f"Address: {address}\n"
                    result_string += f"Number: {phone}\n"
                    result_string +="\n"  
                    
                    if i == 1:
                        print(f"First name: {first_name}")
                        if middle_names:
                            for idx, middle_name in enumerate(middle_names, 1):
                                print(f"Middle name_{idx}: {middle_name}")
                        print(f"Last name: {last_name}")
                        print(f"Address: {address}")
                        print(f"Number: {phone}")
                        print("\n")
                    i +=1
        
        except AttributeError:
            print("Could not find results attribute")
        
    print(f"There was {i} results, full list is saved in .txt")    
    check_existing_result(result_string)  
