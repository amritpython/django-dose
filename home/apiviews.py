from rest_framework import Response




def add_question_apiview(request):
    response = {'ok':False}
    try:
        response['ok'] = True
    except Exception as e:
        response['details'] = str(e)
    return Response(response)


















