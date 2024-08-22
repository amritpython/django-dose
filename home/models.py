from django.db import models
import json
from django.contrib.auth.models import AbstractUser
from dotenv import load_dotenv
import os 


# Create your models here.



class ShopifyUser(AbstractUser):
    USERNAME_FIELD = 'customer_id'
    customer_id = models.CharField(max_length=255,blank=True,null=True,unique=True)
    email = models.CharField(max_length=255,blank=True,null=True)
    created_at = models.CharField(max_length=255,blank=True,null=True)
    updated_at = models.CharField(max_length=255,blank=True,null=True)
    first_name = models.CharField(max_length=255,blank=True,null=True)
    last_name = models.CharField(max_length=255,blank=True,null=True)
    verified_email = models.BooleanField(default=False)
    currency = models.CharField(max_length=255,blank=True,null=True)
    phonenumber = models.CharField(max_length=255,blank=True,null=True)
    
    # default address
    address_id = models.CharField(max_length=255,blank=True,null=True)
    address_firstname = models.CharField(max_length=255,blank=True,null=True)
    address_lastname = models.CharField(max_length=255,blank=True,null=True)
    address_company = models.CharField(max_length=255,blank=True,null=True)
    address_address_one = models.CharField(max_length=255,blank=True,null=True)
    address_address_two = models.CharField(max_length=255,blank=True,null=True)
    address_city = models.CharField(max_length=255,blank=True,null=True)
    address_province = models.CharField(max_length=255,blank=True,null=True)
    address_country = models.CharField(max_length=255,blank=True,null=True)
    address_zipcode = models.CharField(max_length=255,blank=True,null=True)
    address_phone = models.CharField(max_length=255,blank=True,null=True)
    address_provice_code = models.CharField(max_length=255,blank=True,null=True)
    address_country_code = models.CharField(max_length=255,blank=True,null=True)
    address_country_name = models.CharField(max_length=255,blank=True,null=True)
    
    
    @property
    def shop(self):
        return 'https://'+os.getenv('SHOP')
    
    def __str__(self):
        return f'{self.id}. {self.customer_id} {self.first_name} {self.last_name}'
    
    def get_cart(self,sessionid):
        obj , created = Cart.objects.get_or_create(user=self,sessionid=sessionid)
        return obj
    
    
    
    
class Cart(models.Model):
    user = models.ForeignKey(ShopifyUser,on_delete=models.CASCADE)
    sessionid = models.CharField(max_length=255,blank=True,null=True)
    
    @property
    def items_count(self):
        return CartItem.objects.filter(cart=self).count()

    def add_variant(self,variant_id):
        obj , created = CartItem.objects.get_or_create(cart=self,variant_id=variant_id)
        obj.quantity = obj.quantity + 1
        obj.save()
        
    @property
    def items(self):
        return CartItem.objects.filter(cart=self)
    
    @property
    def items_quantity(self):
        quantity = 0
        items = CartItem.objects.filter(cart=self)
        for item in items: quantity += item.quantity
        return quantity


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    variant_id = models.CharField(max_length=255,blank=False)
    quantity = models.IntegerField(default=0)
    
    @property
    def quantity_range(self):
        return range(self.quantity)
    
    
class Form(models.Model):
    FORM_CHOICES = [
        ('female_pattern_hair_loss','female_pattern_hair_loss'),
        ('male_pattern_hair_loss','male_pattern_hair_loss'),
        ('beard','beard'),
        ('lashes','lashes'),
        ('brows','brows'),
        ('post_chemotheraphy_hair_loss','post_chemotheraphy_hair_loss'),
        ('traction_related_hair_loss','traction_related_hair_loss'),
        ('hair_shedding','hair_shedding'),
    ]
    CHECKBOX_META = {
        'checkbox_1':'I am over 18',
        'checkbox_2':'I confirm that the answers I provide are factual and accurate',
        'checkbox_3':'I am aware that the online consultation has been devised by Consultant Dermatologist and Trichoderm, Dr Sharon Wong to assess my suitability for DOSE products',
        'checkbox_4':'I understand that online consultations are not as accurate as in person assessments and inherently carries some limitations',
        'checkbox_5':'I understand that DOSE products contain prescription medications that are for my personal use only. I will not share my treatment with any other individuals',
        'checkbox_6':'I must stop all DOSE products if pregnant',
        'checkbox_7':'I understand that as with any treatment, responses will vary between individuals',
        'checkbox_8':'GDPR compliance/data usage – by ticking you give consent to the collection of this data which will be used for marketing and service development',
    }
    user = models.ForeignKey(ShopifyUser,on_delete=models.CASCADE)
    form_type = models.CharField(max_length=255,choices=FORM_CHOICES,blank=True)
    ongoing_question = models.IntegerField(default=1)
    is_opened = models.BooleanField(default=False)
    checkbox_1 = models.BooleanField(default=False)
    checkbox_2 = models.BooleanField(default=False)
    checkbox_3 = models.BooleanField(default=False)
    checkbox_4 = models.BooleanField(default=False)
    checkbox_5 = models.BooleanField(default=False)
    checkbox_6 = models.BooleanField(default=False)
    checkbox_7 = models.BooleanField(default=False)
    checkbox_8 = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    product_recommendation_message = models.TextField(null=True,blank=True)
    
    def get_question(self,question_no):
        return Question.objects.get(form=self,question_no=int(question_no))
    
    @property
    def formatted_form_type(self):
        format = {
            'female_pattern_hair_loss':'Female Pattern Hair Loss',
            'male_pattern_hair_loss':'Male Pattern Hair Loss',
            'beard':'Beard',
            'lashes':'Lashes',
            'brows':'Brows',
            'post_chemotheraphy_hair_loss':'Post Chemotheraphy Hair Loss',
            'traction_related_hair_loss':'Traction Related Hair Loss',
            'hair_shedding':'Hair Shedding',
        }
        return format[self.form_type]
    
    def __str__(self):
        return f'{self.id}.   {self.form_type}    {self.user.customer_id}'

class Question(models.Model):
    form = models.ForeignKey(Form,on_delete=models.CASCADE)
    question_no = models.IntegerField(blank=True)
    question_value = models.TextField(blank=True)
    is_answered = models.BooleanField(default=False)
    answer_tag_used = models.CharField(max_length=255,blank=True,null=True)
    answer_value = models.CharField(max_length=255,blank=True,null=True)
    answer_description = models.TextField(null=True)
    answer_raw_json = models.TextField(null=True)
    
    @property
    def raw_json(self):
        try:return json.loads(self.answer_raw_json)
        except:return {}

    @property
    def answer_value_str(self):
        return self.answer_value if self.answer_value else ''
    

class Extra(models.Model):
    field_name = models.CharField(max_length=255,blank=True,null=True)
    field_value = models.TextField(max_length=255,blank=True,null=True)

    
    
    







