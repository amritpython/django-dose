import eroseway

api_client = eroseway.APIClient(
    clinic_id="66bc91a74ffb45af3fff7080",
    api_key="Cs8GdIBeuMnDGOWfKk1elDlaeCniacwLC_l8hiL9W6jnzfI07uF1AwINQqJ_p_6tiRLuBhKuxIVAlxUV_xX4Wg",
    api_secret="a_lrpNp_WkBCZROhAWE3r1vREWkttZMjnZXQ_KJ0Em9mYN5QvYGJRDWHkqaKWGp0S57E3szZx_p1XOWHgJSRvg",
    api_base_url='https://api.staging.eroseway.com'
)

request = ''




def create_patient(data):
    """data={
        'address1': 'Eight B',
        'address2': '',
        'city': 'Delhi',
        'country': 'India',
        'county': 'India',
        'date_of_birth': '2000-01-01',
        'email': 'developer@tbi.com',
        'first_name': 'Developer',
        'last_name': '3',
        'mobile_number': '9876543210',
        'postcode': '123 456',
        'prescribers': ['66bc91fdfcfb9f487029edce'],
        'prescribers_notes': 'These are my notes .\nThis is next line of Note',
        'title': 'Mr',
        'skin_size': '2'
    }
    """
    return api_client(
        'PUT',
        'patient',
        data = data
    )


def get_patients():
    return api_client('GET', 'clinic-users')





