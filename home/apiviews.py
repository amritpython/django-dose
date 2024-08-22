from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from home.models import *




@api_view(['GET'])
def add_variant_apiview(request):
    response = {'ok':False}
    try:
        cart = request.user.get_cart(request.session.session_key)
        cart.add_variant(request.GET.get('variant_id'))
        cart.save()
        print('cart items : ',cart.items)
        response['ok'] = True
    except Exception as e:
        response['deatils'] = str(e)
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




















