import re,requests

def get_url(address):
    contents = requests.get(address).json()
    url = contents['url']
    
    return url

def get_image_url(address):
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url(address)
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    
    return url

def get_onedogo():
    '''
    Returns an URL with dogo single image
    '''
    print("Dogo encontrado.")
    url = get_image_url('https://random.dog/woof.json')
    return url

