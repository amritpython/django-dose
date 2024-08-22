from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from .models import Shop
from shopify.utils import shop_url

import binascii
import json
import os
import re
import shopify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

class LoginView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        if Shop.objects.filter(shopify_domain=os.getenv('SHOP')).exists():
            context['exists'] = True
            context['shop'] = Shop.objects.get(shopify_domain=os.getenv('SHOP'))
        if request.GET.get("shop"):
            return authenticate(request)
        context['app_name'] = os.getenv('APP_NAME')
        return render(request, "shopify_app/login.html",context)

    def post(self, request):
        print(request)
        print(request.POST)
        print(request.GET)
        context = {}
        if request.POST.get('action') == 'install':
            if request.POST.get('install-secret') != os.getenv('INSTALL_SECRET'):
                return render(request,'shopify_app/login.html',{'app_name':os.getenv('APP_NAME'),'messages':["INSTALL_SECRET doesn't match"]})
            if request.POST.get('shop') != os.getenv('SHOP'):
                return render(request,'shopoify_app/login.html',{'app_name':os.getenv('APP_NAME'),'message':["Domain doesn't matching with SHOP(.env)"]})
            return authenticate(request)
        elif request.POST.get('action') == 'uninstall':
            if request.POST.get('uninstall-secret') != os.getenv('UNINSTALL_SECRET'):
                return render(request,'shopify_app/login.html',{'app_name':os.getenv('APP_NAME'),'messages':["UNINSTALL_SECRET doesn't match"],'exists':True})
            Shop.objects.filter(shopify_domain=request.POST.get('shop-domain')).delete()
            context['app_name'] = os.getenv('APP_NAME')
            return render(request,'shopify_app/login.html',context)


def callback(request):
    params = request.GET.dict()
    shop = params.get("shop")

    try:
        validate_params(request, params)
        access_token, access_scopes = exchange_code_for_access_token(request, shop)
        store_shop_information(access_token, access_scopes, shop)
        after_authenticate_jobs(shop, access_token)
    except ValueError as exception:
        messages.error(request, str(exception))
        return redirect(reverse("login"))

    redirect_uri = build_callback_redirect_uri(request, params)
    return redirect(redirect_uri)


@csrf_exempt
def uninstall(request):
    uninstall_data = json.loads(request.body)
    shop = uninstall_data.get("domain")
    Shop.objects.filter(shopify_domain=shop).delete()
    return HttpResponse(status=204)


# Login helper methods


def authenticate(request):
    try:
        shop = get_sanitized_shop_param(request)
        scopes, redirect_uri, state = build_auth_params(request)
        store_state_param(request, state)
        permission_url = _new_session(shop).create_permission_url(
            scopes, redirect_uri, state
        )
        return redirect(permission_url)
    except ValueError as exception:
        messages.error(request, str(exception))
        return redirect(reverse("login"))


def get_sanitized_shop_param(request):
    sanitized_shop_domain = shop_url.sanitize_shop_domain(
        request.GET.get("shop", request.POST.get("shop"))
    )
    if not sanitized_shop_domain:
        raise ValueError("Shop must match 'example.myshopify.com'")
    return sanitized_shop_domain


def build_auth_params(request):
    scopes = get_configured_scopes()
    redirect_uri = build_redirect_uri()
    state = build_state_param()

    return scopes, redirect_uri, state


def get_configured_scopes():
    return apps.get_app_config("shopify_app").SHOPIFY_API_SCOPES.split(",")


def build_redirect_uri():
    app_url = apps.get_app_config("shopify_app").APP_URL
    callback_path = reverse("callback")
    return "https://{app_url}{callback_path}".format(
        app_url=app_url, callback_path=callback_path
    )


def build_state_param():
    return binascii.b2a_hex(os.urandom(15)).decode("utf-8")


def store_state_param(request, state):
    request.session["shopify_oauth_state_param"] = state


def _new_session(shop_url):
    shopify_api_version = apps.get_app_config("shopify_app").SHOPIFY_API_VERSION
    shopify_api_key = apps.get_app_config("shopify_app").SHOPIFY_API_KEY
    shopify_api_secret = apps.get_app_config("shopify_app").SHOPIFY_API_SECRET

    shopify.Session.setup(api_key=shopify_api_key, secret=shopify_api_secret)
    return shopify.Session(shop_url, shopify_api_version)


# Callback helper methods


def validate_params(request, params):
    validate_state_param(request, params.get("state"))
    if not shopify.Session.validate_params(params):  # Validates HMAC
        raise ValueError("Invalid callback parameters")


def validate_state_param(request, state):
    if request.session.get("shopify_oauth_state_param") != state:
        raise ValueError("Anti-forgery state parameter does not match")

    request.session.pop("shopify_oauth_state_param", None)


def exchange_code_for_access_token(request, shop):
    session = _new_session(shop)
    access_token = session.request_token(request.GET)
    access_scopes = session.access_scopes

    return access_token, access_scopes


def store_shop_information(access_token, access_scopes, shop):
    shop_record = Shop.objects.get_or_create(shopify_domain=shop)[0]
    shop_record.shopify_token = access_token
    shop_record.access_scopes = access_scopes

    shop_record.save()


def build_callback_redirect_uri(request, params):
    base = request.session.get("return_to", reverse("root_path"))
    return "{base}?shop={shop}".format(base=base, shop=params.get("shop"))


# callback after_authenticate_jobs helper methods


def after_authenticate_jobs(shop, access_token):
    create_uninstall_webhook(shop, access_token)


def create_uninstall_webhook(shop, access_token):
    with shopify_session(shop, access_token):
        app_url = apps.get_app_config("shopify_app").APP_URL
        webhook = shopify.Webhook()
        webhook.topic = "app/uninstalled"
        webhook.address = "https://{host}/uninstall".format(host=app_url)
        webhook.format = "json"
        webhook.save()


def shopify_session(shopify_domain, access_token):
    api_version = apps.get_app_config("shopify_app").SHOPIFY_API_VERSION

    return shopify.Session.temp(shopify_domain, api_version, access_token)




def get_customer_details(customer_id):
    shop_name = os.getenv('SHOP')
    shopify_store = get_object_or_404(Shop, shopify_domain=shop_name)
    access_token = shopify_store.shopify_token
    print(access_token)
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }
    url = f"https://{shop_name}/admin/api/2024-07/customers/{customer_id}.json" 
    response = requests.get(url, headers=headers, timeout=600)
    response.raise_for_status()
    response_data = response.json()
    customers = response_data.get('customer', {})
    return customers



def get_product_details(product_id):
    shop_name = os.getenv('SHOP')
    shopify_store = get_object_or_404(Shop,shopify_domain=shop_name)
    access_token = shopify_store.shopify_token
    headers = {
        'Content-Type':'application/json',
        'X-Shopify-Access-Token':access_token
    }
    url = f'https://{shop_name}/admin/api/2024-07/products/{product_id}.json'
    response = requests.get(url, headers=headers,timeout=600)
    response.raise_for_status()
    response_data = response.json()
    return response_data.get('product',{})


def get_customer_orders(customer_id):
    shop_name = os.getenv('SHOP')
    shopify_store = get_object_or_404(Shop,shopify_domain=shop_name)
    access_token = shopify_store.shopify_token
    headers = {
        'Content-Type':'application/json',
        'X-Shopify-Access-Token':access_token
    }
    url = f'https://{shop_name}/admin/api/2024-07/customers/{customer_id}/orders.json'
    response = requests.get(url,headers=headers,timeout=600)
    response.raise_for_status()
    response_data = response.json()
    return response_data.get('orders',[])


def get_cart_info(customer_id):
    shop_name = os.getenv("SHOP")
    shopify_store = get_object_or_404(Shop,shopify_domain=shop_name)
    access_token = shopify_store.shopify_token
    headers = {
        'Content-Type':'application/json',
        'X-Shopify-Access-Token':access_token,
    }
    url = f'https://{shop_name}/admin/api/2024-07/checkouts.json'
    response = requests.get(url,headers=headers,timeout=600)
    response.raise_for_status()
    response_data = response.json()
    cart_list = response_data.get('checkouts')
    for cart in cart_list :
        if cart.get('customer').get('id') == int(customer_id):
            return cart
        else: print(len(cart.get('customer').get('id')),cart.get('customer').get('id') , customer_id, len(int(customer_id)))
    return None

def add_to_cart(customer_id,varient_id):
    shop_name = os.getenv('SHOP')
    shopify_store = get_object_or_404(Shop,shopify_domain=shop_name)
    access_token = shopify_store.shopify_token
    headers = {
        'Content-Type':'application/json',
        'X-Shopify-Access-Token': access_token
    }
    # user_cart = get_cart_info(customer_id=customer_id)
    # print(user_cart)
    # token = user_cart.get('token')
    url = f'https://{shop_name}/admin/api/2024-07/checkouts/{token}.json'
    response = requests.put(url=url,headers=headers,data=json.dumps())
    return response.json()



def create_order_webhook(shop, access_token):
    with shopify_session(shop, access_token):
        app_url = apps.get_app_config("shopify_app").APP_URL
        webhook = shopify.Webhook()
        webhook.topic = "orders/create"
        webhook.address = "https://{host}/orders_create".format(host=app_url)
        webhook.format = "json"
        webhook.save()
        
        
        
from home import roseway_helpers
from home import medicheck_helpers
from home.models import ShopifyUser

@csrf_exempt
def orders_create(request):
    if request.method == 'POST':
        try:
            order = json.loads(request.body)
            print('order : ',order)
            return HttpResponse(status=200)
            shop_name = request.headers.get('X-Shopify-Shop-Domain')
            shopify_store = get_object_or_404(Shop, shopify_domain=shop_name)
            access_token = shopify_store.shopify_token
            order_line_items = order['line_items']
            customer_id = ''
            customer_info = get_customer_details(customer_id=customer_id)
            customer = ShopifyUser.objects.get_or_create()
            customer.email = customer_info['email']
            customer.created_at = customer_info['created_at']
            customer.updated_at = customer_info['updated_at']
            customer.first_name = customer_info['first_name']
            customer.last_name = customer_info['last_name']
            customer.verified_email = customer_info['verified_email']
            customer.currency = customer_info['currency']
            customer.address_id = customer_info['default_address']['id']
            customer.address_firstname = customer_info['default_address']['first_name']
            customer.address_lastname = customer_info['default_address']['last_name']
            customer.address_company = customer_info['default_address']['company']
            customer.address_address_one = customer_info['default_address']['address1']
            customer.address_address_two = customer_info['default_address']['address2']
            customer.city = customer_info['default_address']['city']
            customer.address_province = customer_info['default_address']['province']
            customer.address_country = customer_info['default_address']['country']
            customer.address_zipcode = customer_info['default_address']['zip']
            customer.address_phone = customer_info['default_address']['phone']
            customer.address_provice_code = customer_info['default_address']['province_code']
            customer.address_country_code = customer_info['default_address']['country_code']
            customer.address_country_name = customer_info['default_address']['country_name']
            customer.save()
            roseway_payload = {
                'address1':customer.address_address_one,
                'address2':customer.address_address_two,
                'city':customer.address_city,
                'country':customer.address_country,
                'date_of_birth':'2000-01-01',
                'email':customer.email,
                'first_name':customer.first_name,
                'last_name':customer.last_name,
                'mobile_number':customer.phonenumber,
                'postcode':customer.address_zipcode,
                'prescribers':['66bc91fdfcfb9f487029edce'],
                'prescribers_notes':'',
                'title':'',
                'skin_size':''
            }
            roseway_helpers.create_patient(roseway_payload)
            medicheck_payload = {
                
            }
            # medicheck_helpers.create_patient()
            for orderlineitem in order_line_items:
				#API Code Implement
                pass
                        
            return HttpResponse(status=204)
        except json.JSONDecodeError as e:
            # Log the error
            #logger.error('Invalid JSON received: %s', e)
            return HttpResponse(status=400)
        except Exception as e:
            # Log any other error
            #logger.error('Error processing webhook: %s', e)
            return HttpResponse(status=500)
    else:
        # Return a 405 Method Not Allowed if the request method is not POST
        return HttpResponse(status=405)


