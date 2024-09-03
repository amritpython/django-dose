from django.apps import AppConfig
import os 
import requests
from dotenv import load_dotenv

load_dotenv()


class HomeConfig(AppConfig):
    name = 'home'
    
    def ready(self):
        import home.signals
        
        from home.models import Extra
        print('exists: ',Extra.objects.filter(field_name='GBPUSD_exchange_rate').exists())
        if not Extra.objects.filter(field_name='GBPUSD_exchange_rate').exists():
            url = f"http://api.currencylayer.com/live?access_key={os.getenv('CURRENCYLAYER_API_KEY')}&source=GBP&currencies=USD&format=1"
            res = requests.get(url)
            exchange_rate_field , created = Extra.objects.get_or_create(field_name='GBPUSD_exchange_rate')
            quotes = res.json().get('quotes')
            if not quotes:
                print('error at exchange rate updation',res.json())
                return
            exchange_rate = quotes.get('GBPUSD')
            if not exchange_rate:
                print('error at exchange rate updation',res.json())
                return
            exchange_rate_field.field_value = exchange_rate
            exchange_rate_field.save()
            print('Exrange rate updated.')
        else:
            print('Exchange rate Exists')
