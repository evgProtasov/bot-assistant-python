import requests

async def get_facebook_campaign_statistics(access_token, account_id):
    url = f"https://graph.facebook.com/v12.0/act_{account_id}/insights"
    
    params = {
        'access_token': access_token,
        'fields': 'campaign_id,campaign_name,impressions,clicks,spend,ctr,cpm,cpc,reach',
        'date_preset': 'last_30d',
        'level': 'campaign'
    }
    
    all_data = []
    current_url = url
    
    all_data = []
    current_url = url
    
    try:
        while current_url:
            response = requests.get(current_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data:
                all_data.extend(data['data'])
            else:
                print("Нет данных в ответе.")
                break
            
            current_url = data.get("paging", {}).get("after")
            
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
        return {"error": str(http_err)}
    except requests.exceptions.RequestException as req_err:
        print(f"Ошибка запроса: {req_err}")
        return {"error": str(req_err)}
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {"error": str(e)}

    return all_data
