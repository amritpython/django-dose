from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.apps import apps
from django.views.decorators.clickjacking import xframe_options_exempt
from shopify_app.decorators import known_shop_required, latest_access_scopes_required
from home.models import ShopifyUser,Form,Question
from shopify_app.models import Shop
from shopify_app.views import get_product_details,get_customer_details
from shopify_app.views import get_customer_orders
from django.contrib.auth import login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dotenv import load_dotenv
import os,datetime
import json,requests
import random


dose_directory_url = '/dose_directory'




def custom_auth(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated: return redirect('https://'+os.getenv('SHOP'))
        request.user.cart = request.user.get_cart(sessionid=request.session.session_key)
        print('cart set : ',request.user.cart)
        return view_func(request, *args, **kwargs) if Shop.objects.filter(shopify_domain=os.getenv('SHOP')).exists() else redirect('/login')
    return wrapper


@custom_auth
def email_subscribe_view(request):
    print(request.POST)
    url = f"https://{os.getenv('shop')}/admin/api/2024-04/customers.json"
    payload = json.dumps({
        "customer": {
            "first_name": request.POST.get('email').split('@')[0],
            # "last_name": '@'+request.POST.get('email').split('@')[1],
            "email": request.POST.get('email'),
            "verified_email": True,
            "addresses": [
                {
                    "address1": "123 Oak St",
                    "city": "Ottawa",
                    "province": "ON",
                    "phone": "555-1212",
                    "zip": "123 ABC",
                    "last_name": "Lastnameson",
                    "first_name": "Mother",
                    "country": "CA"
                }
            ],
            "password": "newpass",
            "password_confirmation": "newpass",
            "send_email_welcome": False,
            "email_marketing_consent": {
                "state": "subscribed"
            }
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': Shop.objects.get(shopify_domain=os.getenv('SHOP')).shopify_token
    }
    response = HttpResponseRedirect(request.headers.get('Referer',request.user.shop))
    try:
        store_response = requests.post(url, headers=headers,data=payload)
        print(store_response.text)
        if 'has already been taken' in store_response.text:response.set_cookie('error','Email Already Used.')
        elif 'is invalid' in store_response.text:response.set_cookie('error','Email is Invalid.')
        else:response.set_cookie('success','Email Subscribed Successfully.') 
    except Exception as e:
        response.set_cookie('error','Something Went Wrong.')
    return response


def logout_view(request):
    if request.user.is_authenticated:logout(request)
    return redirect('https://'+os.getenv('SHOP')+'/account/logout')

@custom_auth
def dose_directory_view(request):
    context = {}
    return render(request,'dose_directory.html',context)

@custom_auth
def consulation_result_view(request,id):
    context = {}
    with open('products.json','r') as file:
        products = json.load(file)
    if not Form.objects.filter(id=int(id)).exists():return redirect('/')
    form = Form.objects.get(id=int(id))
    if form.form_type == 'male_pattern_hair_loss' and form.get_question(4).answer_value in ['Stage 6','Stage 7']:
        return redirect('/dose_directory')
    product_ids = products[form.form_type]    
    products = []
    for product_id in product_ids:
        details = get_product_details(product_id)
        description = str(details['body_html'])
        description = description.removeprefix('<p>')
        description = description.removesuffix('<!---->')
        description = description.removesuffix('\n')
        description = description.removesuffix('</p>')
        details['description'] = description
        price = details['variants'][0]['price']
        # GBP to us dollar
        price = float(price) * 1.28197
        # 2% conversion fee
        price = price + (price * 0.02)
        # nearest price
        price = int(round(price))
        details['variants'][0]['price'] = price
        products.append(details)
    context['form'] = form
    context['products'] = products
    return render(request,'result_page.html',context)

def my_account_view(request):
    if not Shop.objects.filter(shopify_domain=os.getenv('SHOP')).exists():
        return redirect('/login')
    context = {}
    customer_id = request.GET.get('id')
    if customer_id:
        logout(request)
        try:
            customer_info = get_customer_details(customer_id=customer_id)
            customer , created = ShopifyUser.objects.get_or_create(customer_id=customer_id,username=customer_id)
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
            customer.address_city = customer_info['default_address']['city']
            customer.address_province = customer_info['default_address']['province']
            customer.address_country = customer_info['default_address']['country']
            customer.address_zipcode = customer_info['default_address']['zip']
            customer.address_phone = customer_info['default_address']['phone']
            customer.address_provice_code = customer_info['default_address']['province_code']
            customer.address_country_code = customer_info['default_address']['country_code']
            customer.address_country_name = customer_info['default_address']['country_name']
            customer.save()
            login(request,customer)
            user = customer
            request.user = customer
        except Exception as e:
            print('\n'+str(e)+'\n')
            return redirect('https://'+os.getenv('SHOP'))
    user = request.user
    request.user.cart = request.user.get_cart(sessionid=request.session.session_key)
    if request.method == 'POST':
        print(request.POST)
    user_forms = Form.objects.filter(user=user).order_by('-id')
    customer_orders = get_customer_orders(request.user.customer_id)
    for order in customer_orders:order['updated_at_formatted'] = datetime.datetime.strptime(order['updated_at'][:10],'%Y-%m-%d').strftime('%B %-d, %Y')
    
    all_records = user_forms
    p = Paginator(all_records,10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
        records = page_obj.object_list
    except PageNotAnInteger:
        page_obj = p.page(1)
        records = page_obj.object_list
    except EmptyPage:
        page_obj = p.page(p.num_pages)
        page_number = 1
        records = []
    context['user_forms'] = records
    context['page_obj'] = page_obj
    current_page = int(request.GET.get('page',1))
    context['reqs'] = [1,2,3,page_obj.paginator.num_pages,current_page,current_page+1,current_page-1]
    context['dots'] = [4,page_obj.paginator.num_pages-1]
    context['customer_orders'] = customer_orders
    return render(request,'my_account.html',context)

@custom_auth
def brows_step_form_view(request):
    context = {}
    user = request.user
    form = Form.objects.get(id=int(request.GET.get('id')),user=user)
    if form.is_completed:return redirect(f'/consulation_result/{form.id}')
    if request.method == 'POST' and request.POST.get('action') == 'back':
        form.ongoing_question = form.ongoing_question - 1
        if form.ongoing_question == 0 : form.ongoing_question = 1
        form.save()
    elif request.method == 'POST':
        print(request.POST)
        question_no = request.POST.get('question-no')
        question = form.get_question(question_no)
        question.answer_tag_used = request.POST.get('answer-tag-used')
        if question.answer_tag_used == 'radio':
            question.answer_value = request.POST.get('answer-value')
        elif question.answer_tag_used == 'checkbox':
            checkbox_values = eval(request.POST.get('checkbox-values'))
            checked_indexes = []
            for key in request.POST:
                if request.POST.get(key) == 'on':
                    checked_indexes.append(int(key))
            raw_json = {}
            answer_value = ''
            for i,v in enumerate(checkbox_values):
                raw_json[i] = {
                    'checked': True if i in checked_indexes else False,
                    'value': v
                }
                if i in checked_indexes:answer_value += str(v + ', ')
            question.answer_value = answer_value
            question.answer_raw_json = raw_json
        question.is_answered = True
        question.save()
        form.is_opened = True
        form.ongoing_question = int(request.POST.get('question-no')) + 1
        form.save()
        if form.ongoing_question == 9 :
            form.ongoing_question = 1
            form.is_completed = True
            form.product_recommendation_message = f"""Please note that with more extensive or severe hair loss you may require stronger prescription medication. Please see our DOSE DIRECTORY for recommended Dermatologists if no improvement is seen after 6 months of use."""
            form.save()
            return render(request,'tq_brows.html',{'form':form})
    question = form.get_question(str(form.ongoing_question))
    if question.is_answered:context['answer_value'] = question.answer_value
    context['question_no'] = str(form.ongoing_question)
    context['steps_range'] = range(form.ongoing_question)
    context['steps_active_range'] = range(8-form.ongoing_question)
    context['form'] = form
    return render(request,'brows_step_form.html',context)
@custom_auth
def chemo_therapy_step_form_view(request):
    context = {}
    user = request.user
    form = Form.objects.get(id=int(request.GET.get('id')),user=user)
    if form.is_completed:return redirect(f'/consulation_result/{form.id}')
    if request.method == 'POST' and request.POST.get('action') == 'back':
        form.ongoing_question = form.ongoing_question - 1
        if form.ongoing_question == 0 : form.ongoing_question = 1
        form.save()
    elif request.method == 'POST':
        print(request.POST)
        question_no = request.POST.get('question-no')
        question = form.get_question(question_no)
        question.answer_tag_used = request.POST.get('answer-tag-used')
        if question.answer_tag_used == 'radio':
            question.answer_value = request.POST.get('answer-value')
        elif question.answer_tag_used == 'checkbox':
            checkbox_values = eval(request.POST.get('checkbox-values'))
            checked_indexes = []
            for key in request.POST:
                if request.POST.get(key) == 'on':
                    checked_indexes.append(int(key))
            raw_json = {}
            answer_value = ''
            for i,v in enumerate(checkbox_values):
                raw_json[i] = {
                    'checked': True if i in checked_indexes else False,
                    'value': v
                }
                if i in checked_indexes:answer_value += str(v + ', ')
            question.answer_value = answer_value
            question.answer_raw_json = raw_json
        question.is_answered = True
        question.save()
        form.is_opened = True
        form.ongoing_question = int(request.POST.get('question-no')) + 1
        form.save()
        if form.ongoing_question == 9 :
            form.ongoing_question = 1
            form.is_completed = True
            form.product_recommendation_message = f"""Please note that with more extensive or severe hair loss you may require stronger prescription medication. Please see our DOSE DIRECTORY for recommended Dermatologists if no improvement is seen after 6 months of use."""
            form.save()
            return render(request,'tq_chemo.html',{'form':form})
    question = form.get_question(str(form.ongoing_question))
    if question.is_answered:context['answer_value'] = question.answer_value
    context['question_no'] = str(form.ongoing_question)
    context['steps_range'] = range(form.ongoing_question)
    context['steps_active_range'] = range(8-form.ongoing_question)
    context['form'] = form
    return render(request,'chemo_therapy_step_form.html',context)
@custom_auth
def female_pattern_hair_loss_view(request):
    context = {}
    user = request.user
    form = Form.objects.get(id=int(request.GET.get('id')),user=user)
    if form.is_completed:return redirect(f'/consulation_result/{form.id}')
    if request.method == 'POST' and request.POST.get('action') == 'back':
        question_7 = form.get_question(7)   
        if form.ongoing_question == 9 and 'I am pre-menopausal and am not pregnant' in question_7.answer_value:
            form.ongoing_question = form.ongoing_question - 1
        form.ongoing_question = form.ongoing_question - 1
        if form.ongoing_question == 0 : form.ongoing_question = 1
        form.save()
    elif request.method == 'POST':
        print(request.POST)
        question_no = request.POST.get('question-no')
        question = form.get_question(question_no)
        question.answer_tag_used = request.POST.get('answer-tag-used')
        if question.answer_tag_used == 'radio':
            question.answer_value = request.POST.get('answer-value')
            print(question.answer_value)
            if 'I am pre-menopausal and am not pregnant' in question.answer_value:
                form.ongoing_question = form.ongoing_question + 1
                question_8 = form.get_question(8)   
                question_8.answer_value = None
                question_8.save()
                form.save()
        elif question.answer_tag_used == 'checkbox':
            checkbox_values = eval(request.POST.get('checkbox-values'))
            checked_indexes = []
            for key in request.POST:
                if request.POST.get(key) == 'on':
                    checked_indexes.append(int(key))
            raw_json = {}
            answer_value = ''
            for i,v in enumerate(checkbox_values):
                raw_json[i] = {
                    'checked': True if i in checked_indexes else False,
                    'value': v
                }
                if i in checked_indexes:answer_value += str(v + ', ')
            question.answer_value = answer_value
            question.answer_raw_json = raw_json
        question.is_answered = True
        question.save()
        form.is_opened = True
        form.ongoing_question = form.ongoing_question + 1
        form.save()
        if form.ongoing_question == 11 :
            form.ongoing_question = 1
            form.is_completed = True
            form.save()
            answer_values = ''
            for question in Question.objects.filter(form=form):
                answer_values += question.answer_value_str
            # stage 1   yes breast cancer
            if 'Stage 1' in answer_values and 'breast cancer' in answer_values:
                form.product_recommendation_message = 'There are many other causes which can contribute to hair loss and or thinning. These may include nutritional deficiencies, thyroid disease and hormone imbalances. These can be easily checked by a convenient home blood testing kit through our partner lab THRIVA.'
                form.save()
                return render(request,'Female/stage_1_yes_bc.html',{'form':form,'answer_values':answer_values})
            # stage 1   no breast cancer
            elif 'Stage 1' in answer_values and 'brest cancer' not in answer_values:
                form.product_recommendation_message = 'There are many other causes which can contribute to hair loss and or thinning. These may include nutritional deficiencies, thyroid disease and hormone imbalances. These can be easily checked by a convenient home blood testing kit through our partner lab THRIVA.'
                form.save()
                return render(request,'Female/stage_1_no_bc.html',{'form':form,'answer_values':answer_values})
            # stage 2 or 3   yes breast cancer
            elif ('Stage 2' in answer_values or 'Stage 3' in answer_values) and 'breast cancer' in answer_values:
                form.product_recommendation_message = 'There are many other causes which can contribute to hair loss and or thinning. These may include nutritional deficiencies, thyroid disease and hormone imbalances. These can be easily checked by a convenient home blood testing kit through our partner lab THRIVA.'
                form.save()
                return render(request,'Female/stage_2_3_yes_bc.html',{'form':form,'answer_values':answer_values})
            # stage 2 or 3   no breast cancer
            elif ('Stage 2' in answer_values or 'Stage 3' in answer_values) and 'breast cancer' not in answer_values:
                form.product_recommendation_message = 'There are many other causes which can contribute to hair loss and or thinning. These may include nutritional deficiencies, thyroid disease and hormone imbalances. These can be easily checked by a convenient home blood testing kit through our partner lab THRIVA.'
                form.save()
                return render(request,'Female/stage_2_3_no_bc.html',{'form':form,'answer_values':answer_values})
            # stage 4 yes breast cancer
            elif 'Stage 4' in answer_values and 'breast cancer' in answer_values:
                form.product_recommendation_message = 'There are many other causes which can contribute to hair loss and or thinning. These may include nutritional deficiencies, thyroid disease and hormone imbalances. These can be easily checked by a convenient home blood testing kit through our partner lab THRIVA.'
                form.save()
                return render(request,'Female/stage_4_yes_bc.html',{'form':form,'answer_values':answer_values}) 
            # stage 4 no breast cancer
            elif 'Stage 4' in answer_values and 'breast cancer' not in answer_values:
                form.product_recommendation_message = 'There are many other causes which can contribute to hair loss and or thinning. These may include nutritional deficiencies, thyroid disease and hormone imbalances. These can be easily checked by a convenient home blood testing kit through our partner lab THRIVA.'
                form.save()
                return render(request,'Female/stage_4_no_bc.html',{'form':form,'answer_values':answer_values})
            # stage 5 yes breast cancer
            elif 'Stage 5' in answer_values and 'breast cancer' in answer_values:
                form.product_recommendation_message = 'There are many other causes which can contribute to hair loss and or thinning. These may include nutritional deficiencies, thyroid disease and hormone imbalances. These can be easily checked by a convenient home blood testing kit through our partner lab THRIVA.'
                form.save()
                return render(request,'Female/stage_5_yes_bc.html',{'form':form,'answer_values':answer_values})
            # stage 5 no breast cancer
            elif 'Stage 5' in answer_values and 'breast cancer' not in answer_values:
                form.product_recommendation_message = 'There are many other causes which can contribute to hair loss and or thinning. These may include nutritional deficiencies, thyroid disease and hormone imbalances. These can be easily checked by a convenient home blood testing kit through our partner lab THRIVA.'
                form.save()
                return render(request,'Female/stage_5_no_bc.html',{'form':form,'answer_values':answer_values})
            return redirect(f'/consulation_result/{form.id}')
    question = form.get_question(str(form.ongoing_question))
    if question.is_answered:context['answer_value'] = question.answer_value
    context['question_no'] = str(form.ongoing_question)
    context['steps_range'] = range(form.ongoing_question)
    context['steps_active_range'] = range(10-form.ongoing_question)
    context['form'] = form
    return render(request,'female_hair_loss.html',context)
@custom_auth
def hair_shedding_step_form_view(request):
    context = {}
    user = request.user
    form = Form.objects.get(id=int(request.GET.get('id')),user=user)
    if form.is_completed:return redirect(f'/consulation_result/{form.id}')
    if request.method == 'POST' and request.POST.get('action') == 'back':
        form.ongoing_question = form.ongoing_question - 1
        if form.ongoing_question == 0 : form.ongoing_question = 1
        form.save()
    elif request.method == 'POST':
        print(request.POST)
        question_no = request.POST.get('question-no')
        question = form.get_question(question_no)
        question.answer_tag_used = request.POST.get('answer-tag-used')
        if question.answer_tag_used == 'radio':
            question.answer_value = request.POST.get('answer-value')
        elif question.answer_tag_used == 'checkbox':
            checkbox_values = eval(request.POST.get('checkbox-values'))
            checked_indexes = []
            for key in request.POST:
                if request.POST.get(key) == 'on':
                    checked_indexes.append(int(key))
            raw_json = {}
            answer_value = ''
            for i,v in enumerate(checkbox_values):
                raw_json[i] = {
                    'checked': True if i in checked_indexes else False,
                    'value': v
                }
                if i in checked_indexes:answer_value += str(v + ', ')
            question.answer_value = answer_value
            question.answer_raw_json = raw_json
        question.is_answered = True
        question.save()
        form.is_opened = True
        form.ongoing_question = int(request.POST.get('question-no')) + 1
        form.save()
        if form.ongoing_question == 10 :
            form.ongoing_question = 1
            form.is_completed = True
            form.product_recommendation_message = f"""DOSE SHEDDING will help to stabilise the hair cycle and reduce shedding, however with more extensive hair loss you may require stronger prescription medication. Please visit our DOSE DIRECTORY for recommended Dermatologists if no improvement is seen after 6 months of use.
Most cases of telogen effluvium (increased hair shedding) are completely reversible once the trigger factor is identified and corrected. Common contributing causes include nutritional deficiencies, thyroid disease and hormone imbalances. These can be easily checked by a convenient home blood testing kit through our partner lab THRIVA """
            form.save()
            return render(request,'tq_hair_shedding.html',{'form':form})
    question = form.get_question(str(form.ongoing_question))
    if question.is_answered:context['answer_value'] = question.answer_value
    context['question_no'] = str(form.ongoing_question)
    context['steps_range'] = range(form.ongoing_question)
    context['steps_active_range'] = range(9-form.ongoing_question)
    context['form'] = form
    return render(request,'haiir_shedding_step_form.html',context)
@custom_auth
def types_of_hair_loss_view(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request,'Type-of-hair-loss.html')
@custom_auth
def lashes_step_form_view(request):
    context = {}
    user = request.user
    form = Form.objects.get(id=int(request.GET.get('id')),user=user)
    if form.is_completed:return redirect(f'/consulation_result/{form.id}')
    if request.method == 'POST' and request.POST.get('action') == 'back':
        form.ongoing_question = form.ongoing_question - 1
        if form.ongoing_question == 0 : form.ongoing_question = 1
        form.save()
    elif request.method == 'POST':
        print(request.POST)
        question_no = request.POST.get('question-no')
        question = form.get_question(question_no)
        question.answer_tag_used = request.POST.get('answer-tag-used')
        if question.answer_tag_used == 'radio':
            question.answer_value = request.POST.get('answer-value')
        elif question.answer_tag_used == 'checkbox':
            checkbox_values = eval(request.POST.get('checkbox-values'))
            checked_indexes = []
            for key in request.POST:
                if request.POST.get(key) == 'on':
                    checked_indexes.append(int(key))
            print(checked_indexes)
            raw_json = {}
            answer_value = ''
            for i,v in enumerate(checkbox_values):
                raw_json[i] = {
                    'checked': True if i in checked_indexes else False,
                    'value': v
                }
                if i in checked_indexes:answer_value += str(v + ', ')
            question.answer_value = answer_value
            question.answer_raw_json = raw_json
        question.is_answered = True
        question.save()
        form.is_opened = True
        form.ongoing_question = int(request.POST.get('question-no')) + 1
        form.save()
        if form.ongoing_question == 9 :
            form.ongoing_question = 1
            form.is_completed = True
            form.product_recommendation_message = f"""Please note that with more extensive or severe hair loss you may require stronger prescription medication. Please see our DOSE DIRECTORY for recommended dermatologists if no improvement is seen after 6 months of use."""
            form.save()
            return render(request,'tq_lashes.html',{'form':form})
    question = form.get_question(str(form.ongoing_question))
    if question.is_answered:context['answer_value'] = question.answer_value
    context['question_no'] = str(form.ongoing_question)
    context['steps_range'] = range(form.ongoing_question)
    context['steps_active_range'] = range(8-form.ongoing_question)
    context['form'] = form
    return render(request,'lashes_step_form.html',context)
@custom_auth
def male_pattern_hair_loss_view(request):
    context = {}
    user = request.user
    form = Form.objects.get(id=int(request.GET.get('id')),user=user)
    if form.is_completed:return redirect(f'/consulation_result/{form.id}')
    if request.method == 'POST' and request.POST.get('action') == 'back':
        form.ongoing_question = form.ongoing_question - 1
        if form.ongoing_question == 0 : form.ongoing_question = 1
        form.save()
    elif request.method == 'POST':
        print(request.POST)
        question_no = request.POST.get('question-no')
        question = form.get_question(question_no)
        question.answer_tag_used = request.POST.get('answer-tag-used')
        if question.answer_tag_used == 'radio':
            question.answer_value = request.POST.get('answer-value')
        elif question.answer_tag_used == 'checkbox':
            checkbox_values = eval(request.POST.get('checkbox-values'))
            checked_indexes = []
            for key in request.POST:
                if request.POST.get(key) == 'on':
                    checked_indexes.append(int(key))
            raw_json = {}
            answer_value = ''
            for i,v in enumerate(checkbox_values):
                raw_json[i] = {
                    'checked': True if i in checked_indexes else False,
                    'value': v
                }
                if i in checked_indexes:answer_value += str(v + ', ')
            question.answer_value = answer_value
            question.answer_raw_json = raw_json
        question.is_answered = True
        question.save()
        form.is_opened = True
        form.ongoing_question = int(request.POST.get('question-no')) + 1
        form.save()
        if form.ongoing_question == 9 :
            form.ongoing_question = 1
            form.is_completed = True
            form.save()
            stage_question = form.get_question(4)
            common = 'common'
            if stage_question.answer_value in ['Stage 1','Stage 2']:
                return render(request,'Male/stage_1_2.html',{'form':form,'answer_value':stage_question.answer_value})
            elif stage_question.answer_value in ['Stage 3','Stage 4','Stage 5']:
                return render(request,'Male/stage_3_4_5.html',{'form':form,'answer_value':stage_question.answer_value})
            elif stage_question.answer_value in ['Stage 6','Stage 7','Stage 8']:
                return render(request,'Male/stage_6_7.html',{'form':form,'answer_value':stage_question.answer_value})
            return redirect(f'/consulation_result/{form.id}')
    question = form.get_question(str(form.ongoing_question))
    if question.is_answered:context['answer_value'] = question.answer_value
    context['question_no'] = str(form.ongoing_question)
    context['steps_range'] = range(form.ongoing_question)
    context['steps_active_range'] = range(8-form.ongoing_question)
    context['form'] = form
    return render(request,'male_pattern_step_form.html',context)
@custom_auth
def men_beard_step_form_view(request):
    context = {}
    user = request.user
    form = Form.objects.get(id=int(request.GET.get('id')),user=user)
    if form.is_completed:return redirect(f'/consulation_result/{form.id}')
    if request.method == 'POST' and request.POST.get('action') == 'back':
        form.ongoing_question = form.ongoing_question - 1
        if form.ongoing_question == 0 : form.ongoing_question = 1
        form.save()
    elif request.method == 'POST':
        print(request.POST)
        question_no = request.POST.get('question-no')
        question = form.get_question(question_no)
        question.answer_tag_used = request.POST.get('answer-tag-used')
        if question.answer_tag_used == 'radio':
            question.answer_value = request.POST.get('answer-value')
        elif question.answer_tag_used == 'checkbox':
            checkbox_values = eval(request.POST.get('checkbox-values'))
            checked_indexes = []
            for key in request.POST:
                if request.POST.get(key) == 'on':
                    checked_indexes.append(int(key))
            raw_json = {}
            answer_value = ''
            for i,v in enumerate(checkbox_values):
                raw_json[i] = {
                    'checked': True if i in checked_indexes else False,
                    'value': v
                }
                if i in checked_indexes:answer_value += str(v + ', ')
            question.answer_value = answer_value
            question.answer_raw_json = raw_json
        question.is_answered = True
        question.save()
        form.is_opened = True
        form.ongoing_question = int(request.POST.get('question-no')) + 1
        form.save()
        if form.ongoing_question == 9 :
            form.ongoing_question = 1
            form.is_completed = True
            form.product_recommendation_message = 'Please note that with more extensive or severe hair loss you may require stronger prescription medication. Please see our DOSE DIRECTORY (hyperlink) for recommended dermatologists if no improvement is seen after 6 months of use.'
            form.save()
            return render(request,'tq_beard.html',{'form':form})
    question = form.get_question(str(form.ongoing_question))
    if question.is_answered:context['answer_value'] = question.answer_value
    context['question_no'] = str(form.ongoing_question)
    context['steps_range'] = range(form.ongoing_question)
    context['steps_active_range'] = range(8-form.ongoing_question)
    context['form'] = form
    return render(request,'men_beard_step_form.html',context)
@custom_auth
def traction_rela_ted_step_form_view(request):
    context = {}
    user = request.user
    form = Form.objects.get(id=int(request.GET.get('id')),user=user)
    if form.is_completed:return redirect(f'/consulation_result/{form.id}')
    if request.method == 'POST' and request.POST.get('action') == 'back':
        form.ongoing_question = form.ongoing_question - 1
        if form.ongoing_question == 0 : form.ongoing_question = 1
        form.save()
    elif request.method == 'POST':
        print(request.POST)
        question_no = request.POST.get('question-no')
        question = form.get_question(question_no)
        question.answer_tag_used = request.POST.get('answer-tag-used')
        if question.answer_tag_used == 'radio':
            question.answer_value = request.POST.get('answer-value')
        elif question.answer_tag_used == 'checkbox':
            checkbox_values = eval(request.POST.get('checkbox-values'))
            checked_indexes = []
            for key in request.POST:
                if request.POST.get(key) == 'on':
                    checked_indexes.append(int(key))
            raw_json = {}
            answer_value = ''
            for i,v in enumerate(checkbox_values):
                raw_json[i] = {
                    'checked': True if i in checked_indexes else False,
                    'value': v
                }
                if i in checked_indexes:answer_value += str(v + ', ')
            question.answer_value = answer_value
            question.answer_raw_json = raw_json
        question.is_answered = True
        question.save()
        form.is_opened = True
        form.ongoing_question = int(request.POST.get('question-no')) + 1
        form.save()
        if form.ongoing_question == 11 :
            form.ongoing_question = 1
            form.is_completed = True
            form.product_recommendation_message = f"""Please note that with more extensive or severe hair loss you may require stronger prescription medication. Please see our DOSE DIRECTORY for recommended Dermatologists if no improvement is seen after 6 months of use."""
            form.save()
            return render(request,'tq_traction.html',{'form':form})
    question = form.get_question(str(form.ongoing_question))
    if question.is_answered:context['answer_value'] = question.answer_value
    context['question_no'] = str(form.ongoing_question)
    context['steps_range'] = range(form.ongoing_question)
    context['steps_active_range'] = range(10-form.ongoing_question)
    context['form'] = form
    return render(request,'traction_rela_ted_step-form.html',context)



class HomeView(View):
    # @xframe_options_exempt
    #@known_shop_required
    @latest_access_scopes_required
    def get(self, request, *args, **kwargs):
        print('req received')
        if not Shop.objects.filter(shopify_domain=os.getenv('SHOP')).exists():
            return redirect('/login')
        else:print('Using shop domain : ',os.getenv('SHOP'))
        customer_id = request.GET.get('id')
        if customer_id:
            logout(request)
            try:
                customer_info = get_customer_details(customer_id=customer_id)
                customer , created = ShopifyUser.objects.get_or_create(customer_id=customer_id,username=customer_id)
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
                login(request,customer)
                request.user = customer
            except Exception as e:
                print('\n'+str(e)+'\n')
                return redirect('https://'+os.getenv('SHOP'))
        request.user.cart = request.user.get_cart(sessionid=request.session.session_key)
        context = {
            "shop_origin": kwargs.get("shopify_domain"),
            "api_key": apps.get_app_config("shopify_app").SHOPIFY_API_KEY,
            "scope_changes_required": kwargs.get("scope_changes_required"),
            'customer':request.user,
        }
        # return render(request,'Type-of-hair-loss.html',context)
        if not request.user.is_authenticated:return redirect('https://'+os.getenv('SHOP'))
        cookies = dict(pair.split('=', 1) for pair in request.headers.get('cookie').split('; '))
        
        if cookies.get('success') not in ['',None,'None','\"\"']:
            context['success'] = cookies.get('success')
            print('success',cookies.get('success'))
        if cookies.get('error') not in ['',None,'None','\"\"']:
            context['error'] = cookies.get('error')
            print('error',cookies.get('error'))

        rendered_template = render(request,'Type-of-hair-loss.html',context)
        response = HttpResponse(rendered_template.content)
        if context.get('success') is not None:response.set_cookie('success','')
        elif context.get('error') is not None:response.set_cookie('error','')
        return response
    
    
    def post(self,request,*args,**kwargs):
        print(request.user)
        user = request.user
        form = Form.objects.create(user=user,form_type=request.POST.get('form-type'))
        form.checkbox_1 = True if request.POST.get('checkbox-1') == 'on' else False
        form.checkbox_2 = True if request.POST.get('checkbox-2') == 'on' else False
        form.checkbox_3 = True if request.POST.get('checkbox-3') == 'on' else False
        form.checkbox_4 = True if request.POST.get('checkbox-4') == 'on' else False
        form.checkbox_5 = True if request.POST.get('checkbox-5') == 'on' else False
        form.checkbox_6 = True if request.POST.get('checkbox-6') == 'on' else False
        form.checkbox_7 = True if request.POST.get('checkbox-7') == 'on' else False
        form.checkbox_8 = True if request.POST.get('checkbox-8') == 'on' else False
        form.is_opened = True
        form.save()
        return redirect(str('/'+request.POST.get('form-type')+f'?id={form.id}'))

