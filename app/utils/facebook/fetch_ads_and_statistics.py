from app.utils.facebook.get_ads_by_campaign import get_ads_by_campaign
from app.utils.facebook.get_ads_statistics import get_ads_statistics
from app.utils.get_adsets_by_compaign import get_adsets_by_campaign

async def fetch_ads_and_statistics(access_token, account_id, campaign_id):
    # Получаем объявления
    adsets_response = await get_adsets_by_campaign(access_token, account_id, campaign_id)
    
    # Получаем объявления
    ads_response = await get_ads_by_campaign(access_token, account_id, campaign_id)
    
    if 'data' in ads_response and ads_response['data']:
        ad_ids = [ad['id'] for ad in ads_response['data']]
        
        # Получаем статистику по объявлениям
        stats_response = await get_ads_statistics(access_token, account_id, ad_ids)
        
        return {
            'adsets': adsets_response.get('data', []),
            'ads': ads_response['data'],
            'statistics': stats_response.get('data', [])
        }
    else:
        return {
            'adsets': adsets_response.get('data', []),
            'ads': [],
            'statistics': []
        }