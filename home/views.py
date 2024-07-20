from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.apps import apps
from django.views.decorators.clickjacking import xframe_options_exempt
from shopify_app.decorators import known_shop_required, latest_access_scopes_required
from home.models import ShopifyUser,Form



def brows_step_form_view(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request,'brows_step_form.html')

def chemo_therapy_step_form_view(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request,'chemo_therapy_step_form.html')

def female_hair_loss_view(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request,'female_hair_loss.html')

def hair_shedding_step_form_view(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request,'haiir_shedding_step_form.html')

def types_of_hair_loss_view(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request,'Type-of-hair-loss.html')

def lashes_step_form_view(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request,'lashes_step_form.html')

def male_pattern_step_form_view(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request,'male_pattern_step_form.html')

def men_beard_step_form_view(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request,'men_beard_step_form.html')

def traction_rela_ted_step_form_view(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request,'traction_rela_ted_step-form.html')




class HomeView(View):
    # @xframe_options_exempt
    # @known_shop_required
    # @latest_access_scopes_required
    def get(self, request, *args, **kwargs):
        # context = {
        #     "shop_origin": kwargs.get("shopify_domain"),
        #     "api_key": apps.get_app_config("shopify_app").SHOPIFY_API_KEY,
        #     "scope_changes_required": kwargs.get("scope_changes_required"),
        # }
        # return render(request, "home/Type-of-hair-loss.html", context)
        return render(request, "Type-of-hair-loss.html")
    
    
    def post(self,request,*args,**kwargs):
        print(request.POST)
        # user = ShopifyUser()
        # form = Form.objects.get(user=user,form_type=request.POST.get('form-type'))
        # form.checkbox_1 = True if request.POST.get('checkbox_1') == 'on' else False
        # form.checkbox_2 = True if request.POST.get('checkbox_2') == 'on' else False
        # form.checkbox_3 = True if request.POST.get('checkbox_3') == 'on' else False
        # form.checkbox_4 = True if request.POST.get('checkbox_4') == 'on' else False
        # form.checkbox_5 = True if request.POST.get('checkbox_5') == 'on' else False
        # form.checkbox_6 = True if request.POST.get('checkbox_6') == 'on' else False
        # form.checkbox_7 = True if request.POST.get('checkbox_7') == 'on' else False
        # form.checkbox_8 = True if request.POST.get('checkbox_8') == 'on' else False
        easy = {
            'female_pattern_hair_loss':'female_hair_loss.html',
            'male_pattern_hair_loss':'male_pattern_step_form.html',
            'beard':'men_beard_step_form.html',
            'lashes':'lashes_step_form.html',
            'brows':'brows_step_form.html',
            'post_chemotheraphy_hair_loss':'chemo_therapy_step_form.html',
            'traction_related_hair_loss':'traction_rela_ted_step_form.html',
            'hair_shedding':'haiir_shedding_step_form.html'
        }
        return render(request,easy[request.POST.get('form-type')])

