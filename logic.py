from urllib.parse import urlparse, parse_qsl
#Validate url
def url_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False
#Url Anchor
def anchor(url):
    if url.fragment == '':
        return ''
    else:
        return url.fragment
#Url Port

def port(url):
    if url.scheme == 'https':
        return '443'
    elif url.scheme == 'http':
        return '80'
    else:
        return 'Unknown'

#List of split queries

def split_queries(url):
    a = parse_qsl(url.query, keep_blank_values=True)
    if a == []:
        return ''
    else:
        b = []
        for i in a:
            b.append(f'{i[0]}={i[1]}')
        return b

