import requests
from home.models import Extra
import json
import datetime


medicheck_client_id = "dose-hair-api-test"
medicheck_client_secret = "56JhcpvwESWJMioWhQhYEO8yfU6C2KOo"

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
    return response.json()


def create_patient(payload):
    """data="""
    url = "https://patient.api.staging.medichecks.io/Patient"
    token = get_barear_token()
    print('medi token : ',token)
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization":f"Bearer {token}"
    }
    response = requests.post(url, json=payload, headers=headers)
    """{"id":"2024353073","meta":{"versionId":"1","lastUpdated":"2024-08-21 08:52:01 +0000 UTC"},"extension":[{"url":"https://fhir.medichecks.com/patient-ethnicity","valueString":"WHITE_BRITISH"},{"url":"https://fhir.medichecks.com/patient-sex-at-birth","valueString":"male"}],"identifier":[{"use":"official","type":{"coding":[{"system":"https://terminology.hl7.org/CodeSystem/v2-0203","code":"MR"}]},"system":"https://fhir.medichecks.com/patient-identifier","value":"2024353073"}],"active":true,"name":[{"family":"Doe","given":["John"],"prefix":["Dr"]}],"telecom":[{"system":"email","value":"John.Doe@organization.com"},{"system":"phone","value":"07123456789"}],"gender":"male","birthDate":"2000-01-01","address":[{"use":"home","type":"both","line":["12 Example Street","2 floor, apartment 3","Block 2"],"city":"Nottingham","district":"Nottinghamshire","postalCode":"NX0 1WX","country":"United Kingdom"}],"generalPractitioner":[{"reference":"Organization/5145"}],"managingOrganization":{"reference":"Organization/0"},"resourceType":"Patient"}"""
    return response.json()

















































