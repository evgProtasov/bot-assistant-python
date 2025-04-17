import json
import requests

async def get_ads_statistics(access_token, account_id, ad_ids):
    url = f"https://graph.facebook.com/v12.0/act_{account_id}/insights"
    
    filtering = json.dumps([{
        "field": "ad.id",
        "operator": "IN",
        "value": ad_ids
    }])
    
    params = {
        'access_token': access_token,
        'fields': 'ad_id,ad_name,impressions,clicks,spend,ctr,cpm,cpc,reach',
        'filtering': filtering,  # Передаем сериализованный JSON
        'date_preset': 'last_30d',
        'level': 'ad'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        print(f"URL: {url}")
        print(f"Params: {params}")
        raise Exception(f"Error fetching ad statistics: {response.status_code} - {response.text}")