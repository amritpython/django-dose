import eroseway
import os
from dotenv import load_dotenv       
import json

load_dotenv()



api_client = eroseway.APIClient(
    clinic_id = os.getenv('ROSEWAY_CLINIC_ID'),
    api_key = os.getenv('ROSEWAY_API_KEY'),
    api_secret = os.getenv('ROSEWAY_API_SECRET'),
    api_base_url = os.getenv('ROSEWAY_BASE_URL')
)

def get_users():
    return api_client('GET','clinic-users')

def get_patients():
    return api_client('GET','patients')

def get_products():
    api_products = api_client(
        'GET',
        'products',
        params={
            'attributes': [
                '_id',
                'active_product_ingredients',
                'description',
                'name'
            ]
        }
    )
    return api_products


def create_patient(customer):
    payload = {
        'address1':customer.address_address_one,
        'address2':customer.address_address_two,
        'city':customer.address_city,
        'country':customer.address_country,
        'date_of_birth':'2000-01-01',
        'email':customer.email,
        'first_name':customer.first_name,
        'last_name':customer.last_name,
        'mobile_number':customer.address_phone,
        'postcode':customer.address_zipcode,
        'prescribers':[os.getenv('ROSEWAY_PRESCRIBING_USER')],
        'prescribers_notes':'',
        'title':'',
        'skin_size':''
    }
    patient = api_client(
        'PUT',
        'patient',
        data = payload
    )
    return patient.get('_id')


def get_orders():
    web_orders = api_client(
        'GET',
        'web-orders',
        {
            'attributes': [
                'status',
                'ref'
            ]
        }
    )
    return web_orders


def get_prescription(prescription_id):
    prescription = api_client('GET', f'prescriptions/{prescription_id}')
    print(prescription)
    return


def create_order(customer,product_id):
    prescription = api_client(
        'PUT',
        'prescriptions',
        data={
            'clinic_user': os.getenv('ROSEWAY_CLINIC_USER'),
            'patient': customer.roseway_patient_id ,
            'prescribing_user': os.getenv('ROSEWAY_PRESCRIBING_USER'),
            'notes': 'Dose Order',
            'prescription_items': json.dumps([
                            {
                                "product": product_id,
                                "number_of_repeats": 1,
                                "pack_size": 1,
                                "line_item_amount": 1,
                                "usage_instructions": "As directed"
                            }
                        ])
        }
    )
    prescription_id = prescription.get('_id')
    web_order = api_client(
        'POST',
        f'prescriptions/{prescription_id}/authorise',
        data={
            'do_not_issue_web_order': 'False'
        }
    )
    print('web order : ',web_order)
    if not web_order.get('_id',None):
        raise Exception('_id not found in web order')
    return web_order
    