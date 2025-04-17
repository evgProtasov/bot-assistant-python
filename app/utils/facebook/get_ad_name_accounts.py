import requests

async def get_ad_name_campaigns_by_account(account_id, access_token):
    url = f"https://graph.facebook.com/v12.0/act_{account_id}"
    
    params = {
        'access_token': access_token,
        'fields': 'campaigns{name}'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        ad_campaigns = []
        
        if 'campaigns' in data:
            for campaign in data['campaigns']['data']:
                ad_campaigns.append(campaign['id'])
        
        return ad_campaigns
    else:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")