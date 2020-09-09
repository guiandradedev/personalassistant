import requests

def get_onecat():
    '''
    Returns an URL with gatíneo single image
    '''
    print("Gatíneo encontrado.")

    query = 'https://api.thecatapi.com/v1/images/search'
    resp = requests.get(query)
    url = resp.json()[0]['url']
    
    return url
