import requests
from termcolor import colored

def verify(data):
    pass


def ouput_error(msg):
    print colored(msg, 'red')

def ouput_info(msg):
    print colored(msg, 'white')

def audit(url):

    payload = ''

    try:
        r = requests.get(url)
        r.raise_for_status()

    except requests.ConnectionError as e:
        ouptput_error(url+'     connect')

    except requests.HTTPError as e:
        print(self.domain+':'+str(e))

    except:
        print(url+':other error')

    return  False