import requests

username = 'Rahul1125'
token = '60ef979ef27952fdda3633c4a6f37af3af6232cf'
domain_name = 'rahul1125.pythonanywhere.com'

def restartServer():
    response = requests.post(
        'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/'.format(
            username=username,domain_name=domain_name
        ),
        headers={'Authorization': 'Token {token}'.format(token=token)}
    )
    if response.status_code == 200:
        print('Restarting')
        print(response.content)
    else:
        print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))