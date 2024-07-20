from django.db import models

# Create your models here.



class ShopifyUser(models.Model):
    name = models.CharField(max_length=255,blank=True)
    # username = models.CharField(max_length=255,blank=True)
    # shopify_id = models.CharField(max_length=255,blank=True)
    
    
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

class Question(models.Model):
    form = models.ForeignKey(Form,on_delete=models.CASCADE)
    question_no = models.IntegerField(blank=True)
    question_value = models.TextField(blank=True)
    is_answered = models.BooleanField(default=False)
    answer_tag_used = models.CharField(max_length=255,blank=True)
    answer_value = models.CharField(max_length=255,blank=True)
    answer_description = models.TextField()
    answer_raw_json = models.TextField()
    







