import json
import requests

async def get_adsets_by_campaign(access_token, account_id, campaign_id):
    url = f"https://graph.facebook.com/v12.0/act_{account_id}/adsets"
    
    filtering = json.dumps([{
        "field": "campaign.id",
        "operator": "EQUAL",
        "value": campaign_id
    }])
    
    params = {
        'access_token': access_token,
        'fields': 'id,name,campaign_id,status,daily_budget,lifetime_budget',
        'filtering': filtering
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        print(f"URL: {url}")
        print(f"Params: {params}")
        raise Exception(f"Error fetching adsets: {response.status_code} - {response.text}")