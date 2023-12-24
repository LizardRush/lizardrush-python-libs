import os
import requests
import LizardLibs.rushParser.parse as rush_parser

TOKEN_FILE = 'LizardLibs/OAuthApp/token.rush'
GITHUB_API = 'https://api.github.com'

def store_token(token):
    token_content = f'<RTYPE token>\n--begin--\n{token}\n--end--\n'

    with open(TOKEN_FILE, 'w', encoding='utf-8') as file:
        file.write(token_content)

def get_token():
    if os.path.exists(TOKEN_FILE):
        parsed_data = rush_parser.parse_rush_file(TOKEN_FILE)
        tokens = parsed_data.get('<RTYPE token>', [])
        if tokens:
            return tokens[0]
    return None

def get_raw_content(user, repo, path):
    token = get_token()
    if token:
        headers = {'Authorization': f'token {token}'}
        url = f'{GITHUB_API}/repos/{user}/{repo}/contents/{path}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['content']
    return None

def create_file(user, repo, path, content):
    token = get_token()
    if token:
        headers = {'Authorization': f'token {token}'}
        url = f'{GITHUB_API}/repos/{user}/{repo}/contents/{path}'
        data = {
            'message': 'Creating via OAuthApp',
            'content': content
        }
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 201:
            return True
    return False

def delete_file(user, repo, path):
    token = get_token()
    if token:
        headers = {'Authorization': f'token {token}'}
        url = f'{GITHUB_API}/repos/{user}/{repo}/contents/{path}'
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            return True
    return False
