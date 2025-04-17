import requests

async def get_account_currency(access_token, account_id):
    url = f"https://graph.facebook.com/v12.0/act_{account_id}"
    
    params = {
        'access_token': access_token,
        'fields': 'currency'
    }
    
    response = requests.get(url, params=params, timeout=10)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")