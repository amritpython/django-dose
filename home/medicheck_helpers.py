import requests
from home.models import Extra
import json
import datetime
import os
from dotenv import load_dotenv
load_dotenv()


medicheck_client_id = os.getenv('MEDICHECK_CLIENT_ID')
medicheck_client_secret = os.getenv('MEDICHECK_CLIENT_SECRET')

def generate_bearer_token():
    url = 'https://newauth.staging.medichecks.io/realms/plasma/protocol/openid-connect/token'
    headers = {
        'accept':'application/json',
        'content-type':'application/x-www-form-urlencoded'
    }
    payload = f'grant_type=client_credentials&client_id={medicheck_client_id}&client_secret={medicheck_client_secret}'
    response = requests.post(url=url,headers=headers,data=payload)
    return response.json()['access_token']

def get_barear_token():
    medicheck_barear , created = Extra.objects.get_or_create(field_name='medicheck_barear')
    if created:medicheck_barear.field_value = """{}"""
    decoded = json.loads(medicheck_barear.field_value)
    if decoded.get('expire_on') is None or datetime.datetime.strptime(decoded.get('expire_on'),"%Y-%m-%d %H:%M:%S.%f") < datetime.datetime.now():
        new_barear_token = generate_bearer_token()
        medicheck_barear.field_value = json.dumps({
            'token':new_barear_token,
            'expire_on':str(datetime.datetime.now() + datetime.timedelta(seconds=294))
        })
        medicheck_barear.save()
        return new_barear_token
    return json.loads(medicheck_barear.field_value).get('token')


def get_patients():
    url = "https://patient.api.staging.medichecks.io/Patient"
    headers = {
        "accept": "application/json",
        "Authorization":f"Bearer {get_barear_token()}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_patient_id(email:str):
    url = f"https://patient.api.staging.medichecks.io/Patient?count=1&search={email}"
    headers = {
        'accept':'application/json',
        'Authorization':f'Bearer {get_barear_token()}'
    }
    response = requests.get(url,headers=headers)
    response.raise_for_status()
    return response.json()['entry'][0]['resource']['id'] 



def create_patient(customer) -> str:
    """data="""
    url = "https://patient.api.staging.medichecks.io/Patient"
    payload = {
                "resourceType": "Patient",
                "active": True,
                "name": [
                    {
                        "given": [customer.first_name],
                        "prefix": ['Mr'],
                        "family": customer.last_name
                    }
                ],
                "gender": "male",
                "extension": [
                    {
                    "url": "https://fhir.medichecks.com/patient-ethnicity",
                    "valueString": "OTHER"
                    },
                    {
                    "url": "https://fhir.medichecks.com/patient-sex-at-birth",
                    "valueString": "male"
                    }
                ],
                "telecom": [
                    {
                    "system": "email",
                    "use": "mobile",
                    "value": customer.email
                    },
                    {
                    "system": "phone",
                    "use": "mobile",
                    "value": f'0{customer.address_phone}'
                    }
                ],
                "address": [
                    {
                    "country": customer.address_country,
                    "line": [
                        customer.address_address_one,
                        customer.address_address_two,
                    ],
                    "type": "both",
                    "use": "home",
                    "city": customer.address_city,
                    "district": "",
                    "postalCode": customer.address_zipcode
                    }
                ],
                "birthDate": "2000-01-01"
                }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization":f"Bearer {get_barear_token()}"
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    """{"id":"2024353073","meta":{"versionId":"1","lastUpdated":"2024-08-21 08:52:01 +0000 UTC"},"extension":[{"url":"https://fhir.medichecks.com/patient-ethnicity","valueString":"WHITE_BRITISH"},{"url":"https://fhir.medichecks.com/patient-sex-at-birth","valueString":"male"}],"identifier":[{"use":"official","type":{"coding":[{"system":"https://terminology.hl7.org/CodeSystem/v2-0203","code":"MR"}]},"system":"https://fhir.medichecks.com/patient-identifier","value":"2024353073"}],"active":true,"name":[{"family":"Doe","given":["John"],"prefix":["Dr"]}],"telecom":[{"system":"email","value":"John.Doe@organization.com"},{"system":"phone","value":"07123456789"}],"gender":"male","birthDate":"2000-01-01","address":[{"use":"home","type":"both","line":["12 Example Street","2 floor, apartment 3","Block 2"],"city":"Nottingham","district":"Nottinghamshire","postalCode":"NX0 1WX","country":"United Kingdom"}],"generalPractitioner":[{"reference":"Organization/5145"}],"managingOrganization":{"reference":"Organization/0"},"resourceType":"Patient"}"""
    if 'email already exist' in response.text:
        return get_patient_id(customer.email)
    print('medicheck create patient : ',response.text)
    return response.json()['id']


def get_products():
    url = "https://product.api.staging.medichecks.io/v1/products"
    headers = {
        'accept':'application/json',
        'authorization':f'Bearer {get_barear_token()}'
    }
    response = requests.get(url,headers=headers)
    response.raise_for_status()
    res_json = response.json()
    return res_json


def get_orders():
    url = "https://service-request.api.staging.medichecks.io/ServiceRequest"
    headers = {
        "accept":"application/json",
        "authorization": f"Bearer {get_barear_token()}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    res_json = response.json()
    orders = res_json.get('entry')
    formatted_orders = [{
        'token':get_barear_token()
    }]
    for order in orders:
        
        order_note = ''
        if order['resource'].get('note'):
            for note in order['resource']['note']:
                order_note += note['text']
        formatted_orders.append({
            'order_id':order['resource']['id'],
            'patient_name':order['resource']['subject']['extension'][0]['valueHumanName']['text'],
            'instructions':order['resource']['text']['div'],
            'created_at':order['resource']['extension'][0]['valueDateTime'].replace('T',' '),
            'order_value':order['resource']['extension'][2]['valueMoney']['value'],
            'order_currency':order['resource']['extension'][2]['valueMoney']['currency'],
            'payment_code':order['resource']['extension'][3]['valueCoding']['code'],
            'payment_status':order['resource']['extension'][3]['valueCoding']['display'],
            'order_note':order_note,
            'status':order['resource']['status'],
            'resource_type':order['resource']['resourceType']
            
        })
    return formatted_orders



def create_order(customer,product_id,note):
    url = "https://service-request.api.staging.medichecks.io/ServiceRequest"
    headers = {
        "accept":"application/json",
        "authorization": f"Bearer {get_barear_token()}"
    }
    payload = {
        "status": "active",
        "intent": "order",
        "subject": {
            "identifier": {
            "value": customer.medicheck_patient_id,
            "system": "https://fhir.medichecks.com/subject-identifier"
            }
        },
        "code": {
            "coding": [
            {
                "code": product_id,
                "system": "https://fhir.medichecks.com/product-identifier"
            }
            ]
        },
        "orderDetail": [
            {
            "coding": [
                {
                "code": "nurse-home-visit",
                "system": "https://fhir.medichecks.com/sample-type-identifier"
                }
            ]
            }
        ],
        "resourceType": "ServiceRequest",
        "note": [
            {
            "text": note
            }
        ]
    }
    print('medicheck payload : ',payload)
    response = requests.post(url,json=payload,headers=headers)
    response.raise_for_status()
    return response.json()

















































