from .result_writing import check_existing_result
import requests
from bs4 import BeautifulSoup
import re

def launch_username_search(args):
    username = args
    if args[0] == "@": # it should be removed in my opinion
        username = args[1:]

    result_text = f"Instagram : {'yes' if instagram_check(username) else 'no'}\n"
    result_text += f"X : {'yes' if x_check(username) else 'no'}\n"
    result_text += f"Reddit : {'yes' if reddit_check(username) else 'no'}\n"
    result_text += f"Steam : {'yes' if steam_check(username) else 'no'}\n"
    result_text += f"TikTok : {'yes' if tiktok_check(username) else 'no'}"
    print(result_text)
    check_existing_result(result_text)
    
    
def instagram_check(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        if soup.find('meta', property="og:description"):
            return True
        else:
            return False
    elif response.status_code == 404:
        return False
    else:
        print(f"Could not determine the status of username '{username}' (status code: {response.status_code}).")

    
def x_check(username):
    token = x_get_token()
    return x_check_username(username, token)


def x_get_token():
    headers = {
    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    }
    response = requests.post('https://api.twitter.com/1.1/guest/activate.json', headers=headers)
    data = response.json()
    return data.get("guest_token")


def x_check_username(username, token):
    
    cookies = {
    'guest_id': '172614502512142982',
    'night_mode': '2',
    'gt': token,
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en',
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'content-type': 'application/json',
        # 'cookie': 'guest_id=172614502512142982; night_mode=2; gt=token,
        'dnt': '1',
        'origin': 'https://x.com',
        'priority': 'u=1, i',
        'referer': 'https://x.com/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'x-client-transaction-id': 'ijPF7wNqk2MM11UcTXp7fy7usv+nn10KRnJFFHuFaR5kMaaX6T70cQq2ohVJqghmqBn0GYjLuQ9jTJ9YbeoYStPe4KfyiQ',
        'x-guest-token': token,
        'x-twitter-active-user': 'yes',
        'x-twitter-client-language': 'en',
    }

    params = {
        'variables': f'{{"screen_name":"{username}","withSafetyModeUserFields":true}}',
        'features': '{"hidden_profile_subscriptions_enabled":true,"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_is_identity_verified_enabled":true,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"responsive_web_twitter_article_notes_tab_enabled":true,"subscriptions_feature_can_gift_premium":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
        'fieldToggles': '{"withAuxiliaryUserLabels":false}',
    }

    response = requests.get(
        'https://api.x.com/graphql/Yka-W8dz7RaEuQNkroPkYw/UserByScreenName',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    
    data = response.json()
    try:
        result = data["data"]["user"]["result"]["legacy"]["screen_name"]
        return True
    except:
        return False
    
def reddit_check(username):
    url = "https://www.reddit.com/api/username_available.json"
    params = {'user': username}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return not response.json()  # True if available, False if taken. Flip with "not"
    else:
        print(f"Reddit check Error: {response.status_code}")
        return False

def steam_check(username):

    cookies = {
        'sessionid': 'a301b59cef69e3374f2b899b',
        'steamCountry': 'EE%7Cf2ede99bb667edee1f534e609c775f70',
        'timezoneOffset': '10800,0',
        'cookieSettings': '%7B%22version%22%3A1%2C%22preference_state%22%3A2%2C%22content_customization%22%3Anull%2C%22valve_analytics%22%3Anull%2C%22third_party_analytics%22%3Anull%2C%22third_party_content%22%3Anull%2C%22utm_enabled%22%3Atrue%7D',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en',
        'Connection': 'keep-alive',
        # 'Cookie': 'sessionid=a301b59cef69e3374f2b899b; steamCountry=EE%7Cf2ede99bb667edee1f534e609c775f70; timezoneOffset=10800,0; cookieSettings=%7B%22version%22%3A1%2C%22preference_state%22%3A2%2C%22content_customization%22%3Anull%2C%22valve_analytics%22%3Anull%2C%22third_party_analytics%22%3Anull%2C%22third_party_content%22%3Anull%2C%22utm_enabled%22%3Atrue%7D',
        'DNT': '1',
        'Referer': 'https://steamcommunity.com/search/users/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'text': username,
        'filter': 'users',
        'sessionid': 'a301b59cef69e3374f2b899b',
        'steamid_user': 'false',
        'page': '1',
    }

    response = requests.get('https://steamcommunity.com/search/SearchCommunityAjax', params=params, cookies=cookies, headers=headers)

    
    
    if response.status_code == 200:
        data = response.json()
        soup = BeautifulSoup(data["html"], 'lxml')

        if soup.find('a', text=re.compile(username, re.IGNORECASE)):
            return True
        else:
            return False
    elif response.status_code == 404:
            print("elif")
            return False
    else:
        print(f"Could not determine the status of username '{username}' (status code: {response.status_code}).")
        

        
def tiktok_check(username):

    cookies = {
        'tt_csrf_token': 'CzTzeqky-ELlVognh71_b77UteLhfQ_YSuHo',
        'tt_chain_token': 'k+B6/l7p4nvCQs5et7RvkA==',
        'ak_bmsc': '95FC3DFC048DFBDCCD615B72342A9FDC~000000000000000000000000000000~YAAQy2kRYJb9QEeSAQAAQnTZRxka+OhVs3lebskGoMxe+VoRQaZ5Bu2cSCMhNYwtvhhdUn94o1UknIZXPyjzscP7j/CC55uqQUIco7gVBkRiQweZMJR3dnaDNPZ+pueCsvKNMeE2XAbKow9vnpfRe4lMBCc+zDI0396ySWo/3TiLUHKOpO/g/Tour0m61ZcDSVYo1RTQyObqENvIQCaNyJfvXJ422Cj5PoxJ4ahO79IEpFIdVPqucZ6/C+/nWvrhHHQEmKSzKH8cL65gwsSxaituhMWnNOeWufuxKMwBnBXVdn4/uzqgJxVfY4C/TVtpQbkoctdF1WTTTaX/xuvSLIdcNnIRrC9BABK6Zm4jEXAWAwx4MS5r7KxO2W0KFvv3gWCBaPV3nHdxP7Y=',
        'tiktok_webapp_theme_source': 'system',
        'tiktok_webapp_theme': 'dark',
        'delay_guest_mode_vid': '5',
        'ttwid': '1%7CiK9-UDPPMuMQ7Hx2YmMM4E7w65fafb0rurLePpfF_xI%7C1727782288%7C20904a863ea3ebead2a002a0d827f5ff20b6b1408a055e0de3b7fe7920c89742',
        'msToken': 'bOcIM5alySZVolyMj7f0RuXqkhhVIypWPMWKEV6dJ5hTDFhtpHgYxwFkTAQ51obzBvnnpSTilEdtcC2BLXyGL_9BAw7NOmwORFzEF-qX0hzDyJymW9Zd09FOc4DQHigmL3Im3uGPCSuLKnqWNvYT7X9B',
        'msToken': 'd77CVRzhAM65ueuVl62JnwqT-yzLLe6O7kpbBq_m0t7aY1ykmzlvcOXEkrT2idcrMU-DwOhFaCDGvhpIevHzJqe6qvj8C3rCI-LnocZu22PIdcNmRuAHh7Xgz_2C2g==',
        'perf_feed_cache': '{%22expireTimestamp%22:1727953200000%2C%22itemIds%22:[%227398830661538254110%22%2C%227389726259217042721%22%2C%227389629516882218272%22]}',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en',
        'cache-control': 'max-age=0',
        # 'cookie': 'tt_csrf_token=CzTzeqky-ELlVognh71_b77UteLhfQ_YSuHo; tt_chain_token=k+B6/l7p4nvCQs5et7RvkA==; ak_bmsc=95FC3DFC048DFBDCCD615B72342A9FDC~000000000000000000000000000000~YAAQy2kRYJb9QEeSAQAAQnTZRxka+OhVs3lebskGoMxe+VoRQaZ5Bu2cSCMhNYwtvhhdUn94o1UknIZXPyjzscP7j/CC55uqQUIco7gVBkRiQweZMJR3dnaDNPZ+pueCsvKNMeE2XAbKow9vnpfRe4lMBCc+zDI0396ySWo/3TiLUHKOpO/g/Tour0m61ZcDSVYo1RTQyObqENvIQCaNyJfvXJ422Cj5PoxJ4ahO79IEpFIdVPqucZ6/C+/nWvrhHHQEmKSzKH8cL65gwsSxaituhMWnNOeWufuxKMwBnBXVdn4/uzqgJxVfY4C/TVtpQbkoctdF1WTTTaX/xuvSLIdcNnIRrC9BABK6Zm4jEXAWAwx4MS5r7KxO2W0KFvv3gWCBaPV3nHdxP7Y=; tiktok_webapp_theme_source=system; tiktok_webapp_theme=dark; delay_guest_mode_vid=5; ttwid=1%7CiK9-UDPPMuMQ7Hx2YmMM4E7w65fafb0rurLePpfF_xI%7C1727782288%7C20904a863ea3ebead2a002a0d827f5ff20b6b1408a055e0de3b7fe7920c89742; msToken=bOcIM5alySZVolyMj7f0RuXqkhhVIypWPMWKEV6dJ5hTDFhtpHgYxwFkTAQ51obzBvnnpSTilEdtcC2BLXyGL_9BAw7NOmwORFzEF-qX0hzDyJymW9Zd09FOc4DQHigmL3Im3uGPCSuLKnqWNvYT7X9B; msToken=d77CVRzhAM65ueuVl62JnwqT-yzLLe6O7kpbBq_m0t7aY1ykmzlvcOXEkrT2idcrMU-DwOhFaCDGvhpIevHzJqe6qvj8C3rCI-LnocZu22PIdcNmRuAHh7Xgz_2C2g==; perf_feed_cache={%22expireTimestamp%22:1727953200000%2C%22itemIds%22:[%227398830661538254110%22%2C%227389726259217042721%22%2C%227389629516882218272%22]}',
        'dnt': '1',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    response = requests.get(f'https://www.tiktok.com/@{username}', cookies=cookies, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        if soup.find(text=lambda t: t and f'"uniqueId":"{username}"' in t):
            return True
        else:
            return False
    elif response.status_code == 404:
            print("elif")
            return False
    else:
        print(f"Could not determine the status of username '{username}' (status code: {response.status_code}).")
