from django.db.models.signals import post_save
from django.dispatch import receiver
from home.models import *



@receiver(post_save,sender=ShopifyUser)
def create_user_forms(sender,instance,created,**kwargs):
    for form_type in Form.FORM_CHOICES:
        Form.objects.create(
            user = instance,
            form_type = form_type[0],
            ongoing_question = 1,
        )


@receiver(post_save,sender=Form)
def create_form_questions(sender,instance,created,**kwargs):
    if instance.form_type == 'male_pattern_hair_loss':
        # Question 1 
        Question.objects.create(
            form = instance,
            question_no = 1,
            question_value = '1) Age – please tick relevant box',
        )
        # Question 2
        Question.objects.create(
            form = instance,
            question_no = 2,
            question_value = '2) Previous products and treatments used – please tick all that apply',
        )
        # Question 3 
        Question.objects.create(
            form = instance,
            question_no = 3,
            question_value = '3) Where do you get your hair loss advice from? ',
        )
        # Question 4
        Question.objects.create(
            form = instance,
            question_no = 4,
            question_value = '4) Please rate the severity of your hair loss based on the standardised Hamilton Norwood Scale'
        )
        # Question 5 
        Question.objects.create(
            form = instance,
            question_no = 5,
            question_value = '5) Are you allergic to Minoxidil?'
        )
        # Question 6
        Question.objects.create(
            form = instance,
            question_no = 6,
            question_value = '6) Do you have any of the following on your scalp • Redness • Inflammation • Open cuts/wounds on the scalp'
        )
        # Question 7 
        Question.objects.create(
            form = instance,
            question_no = 7,
            question_value = '7) How much does your hair loss affect you? (0 = not affected at all, 10 = significantly affected) 0 – 1 - 2 – 3 – 4 - 5 – 6 – 7 – 8 – 9 – 10'
        )
        # Question 8
        Question.objects.create(
            form = instance,
            question_no = 8,
            question_value = '8) How does the hair loss make you feel? Tick all that apply  • Sad  • Angry  • Helpless  • Embarrassed  • Guilty  • Worthless  • Unattractive  • Old  • Anxious  • Lonely  • Frustrated  • Overwhelmed  • Scared'
        )












