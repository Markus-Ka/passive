from .result_writing import check_existing_result
import requests


def launch_ip_search(ip_address):
    if ip_address == "127.0.0.1":
        check_own_ip()
    else:
        ip_info(ip_address)

def check_own_ip():
    headers = {
        'accept': '*/*',
        'accept-language': 'en',
        # 'content-length': '0',
        'dnt': '1',
        'origin': 'https://www.whatismyip.com',
        'priority': 'u=1, i',
        'referer': 'https://www.whatismyip.com/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    try:
        response = requests.post('https://api.whatismyip.com/wimi.php', headers=headers)
        data = response.json()

        if 'ip' in data:
            ip_info(data['ip'])
        else:
            print('IP key not found in the response.')

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except json.decoder.JSONDecodeError:
        print("Failed to decode JSON response.")
    except KeyError:
        print("Key 'ip' not found in the response data.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

 

    
def ip_info(ip_address):
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    data = response.json()
    
    status = data.get('status')
    if status == 404:
        print("Error: Not a valid IP address, this shouldnt happen, contact admin")
        return
    
    bogon = data.get('bogon')
    if bogon:
        print("Error: Bogon IP address")
        return
    
    
    result = f"ISP: {data.get('org', 'N/A')}\nCountry: {data['country']}\nRegion: {data['region']}\nCity: {data['city']}\nCity Lat,Lon:	{data['loc']}"
    print(result)
    check_existing_result(result)
    