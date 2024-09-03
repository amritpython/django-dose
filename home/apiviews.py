from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from home.models import *
from django.http import HttpResponse
import requests




@api_view(['GET'])
def currency_rate_update_apiview(request):
    response = {'ok':False}
    try:
        url = f"http://api.currencylayer.com/live?access_key={os.getenv('CURRENCYLAYER_API_KEY')}&source=GBP&currencies=USD&format=1"
        res = requests.get(url)
        exchange_rate_field , created = Extra.objects.get_or_create(field_name='GBPUSD_exchange_rate')
        quotes = res.json().get('quotes')
        if not quotes:raise Exception('invalid key,value quotes')
        exchange_rate = quotes.get('GBPUSD')
        if not exchange_rate: raise Exception('invalid key,value GBPUSD')
        exchange_rate_field.field_value = exchange_rate
        exchange_rate_field.save()
        response['api_response'] = res.json()
        response['ok'] = True
    except Exception as e:
        response['details'] = str(e)
    return Response(response)


@api_view(['GET'])
def product_fit_apiview(request):
    response = {'ok':False}
    try:
        customer_id = request.GET.get('customer_id')
        product_id = request.GET.get('product_id')
        if None in [customer_id,product_id]:raise Exception('both_fields_required( customer_id , product_id )')
        customer = ShopifyUser.objects.get(customer_id=customer_id)
        with open('store_resultpage_relation.json','r') as file:
            data = json.load(file)
        form_type = None
        for k,product_list in data.items():
            if product_list == product_id:
                form_type = k
                break
            if not isinstance(product_list,list):continue
            for id in product_list:
                if id == product_id:
                    form_type = k
                    break
        if not form_type:raise Exception('product_doesnt_exist_in store_resultpage_relation.json')
        response['form_type'] = form_type
        if form_type == 'bloodkit':
            response['is_allowed'] = True
        else:response['is_allowed'] = customer.is_form_filled(form_type=form_type)
        response['ok'] = True
    except Exception as e:
        response['details'] = str(e)
    print(response)
    return HttpResponse(content=json.dumps(response),content_type='application/json')



@api_view(['GET'])
def cart_apiview(request):
    response = {'ok':False}
    try:
        user = ShopifyUser.objects.get(customer_id=request.GET.get('customer_id'))
        cart = user.get_cart(user.last_access_session)
        operation = request.GET.get('operation')
        if operation == 'add':
            variant_id = request.GET.get('variant_id')
            if not variant_id: raise Exception('invalid variant_id')
            CartItem.objects.create(cart=cart,variant_id=variant_id,quantity=request.GET.get('quantity',1))
        elif operation == 'remove':
            variant_id = request.GET.get('variant_id')
            if not variant_id: raise Exception('invalid variant_id')
            CartItem.objects.filter(cart=cart,variant_id=variant_id).delete()
        elif operation == 'plus':
            variant_id = request.GET.get('variant_id')
            if not variant_id: raise Exception('invalid variant_id')
            item = CartItem.objects.get(cart=cart,variant_id=variant_id)
            item.quantity = item.quantity + 1
            item.save()
        elif operation == 'minus':
            variant_id = request.GET.get('variant_id')
            if not variant_id: raise Exception('invalid variant_id')
            item = CartItem.objects.get(cart=cart,variant_id=variant_id)
            if item.quantity > 0:
                item.quantity = item.quantity - 1
                item.save()
        elif operation == 'update':
            variant_id = request.GET.get('variant_id')
            item = CartItem.objects.get(cart=cart,variant_id=variant_id)
            item.quantity = int(request.GET.get('quantity',item.quantity))
            item.save()
        elif operation == 'empty':CartItem.objects.filter(cart=cart).delete()
        else: raise Exception('invalid operation')
    except Exception as e :
        response['details'] = str(e)
    return Response(response)




@api_view(['POST'])
def submit_answer_apiview(request):
    response = {'ok':False}
    try:
        user = ShopifyUser.objects.get(id=1)
        question_no = request.POST.get('question-no')
        form_type = request.POST.get('form-type')
        if question_no is None or form_type is None:raise Exception('both_fields_required(question-no,form-type)')
        form = Form.objects.get(user=user,form_type=form_type)
        question = form.get_question(question_no)
        question.answer_tag_used = request.POST.get('answer-tag-used')
        question.answer_value = request.POST.get('answer-value')
        question.answer_description = request.POST.get('answer-description')
        question.answer_json = request.POST.get('answer-json')
        question.is_answered = True
        question.save()
        if question_no != '8':form.is_opened = True
        else:form.is_opened,form.is_completed = False,True
        form.save()
        response['details'] = {
            'question':question.question_no,
            'value':question.question_value,
            'is_answered':question.is_answered,
            'answer_tag_used':question.answer_tag_used,
            'answer_value':question.answer_value,
            'answer_description':question.answer_description,
            'answer_json':question.answer_raw_json
        }
        response['ok'] = True
    except Exception as e:
        response['details'] = str(e)
    return Response(response)





