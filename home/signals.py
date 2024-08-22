from django.db.models.signals import post_save
from django.dispatch import receiver
from home.models import *



@receiver(post_save,sender=Form)
def create_form_questions(sender,instance,**kwargs):
    if instance.form_type == 'male_pattern_hair_loss':
        # Question 1 
        Question.objects.get_or_create(
            form = instance,
            question_no = 1,
            question_value = '1) Age – please tick relevant box',
        )
        # Question 2
        Question.objects.get_or_create(
            form = instance,
            question_no = 2,
            question_value = '2) Previous products and treatments used – please tick all that apply',
        )
        # Question 3 
        Question.objects.get_or_create(
            form = instance,
            question_no = 3,
            question_value = '3) Where do you get your hair loss advice from? ',
        )
        # Question 4
        Question.objects.get_or_create(
            form = instance,
            question_no = 4,
            question_value = '4) Please rate the severity of your hair loss based on the standardised Hamilton Norwood Scale'
        )
        # Question 5 
        Question.objects.get_or_create(
            form = instance,
            question_no = 5,
            question_value = '5) Are you allergic to Minoxidil?'
        )
        # Question 6
        Question.objects.get_or_create(
            form = instance,
            question_no = 6,
            question_value = '6) Do you have any of the following on your scalp • Redness • Inflammation • Open cuts/wounds on the scalp'
        )
        # Question 7 
        Question.objects.get_or_create(
            form = instance,
            question_no = 7,
            question_value = '7) How much does your hair loss affect you? (0 = not affected at all, 10 = significantly affected) 0 – 1 - 2 – 3 – 4 - 5 – 6 – 7 – 8 – 9 – 10'
        )
        # Question 8
        Question.objects.get_or_create(
            form = instance,
            question_no = 8,
            question_value = '8) How does the hair loss make you feel? Tick all that apply  • Sad  • Angry  • Helpless  • Embarrassed  • Guilty  • Worthless  • Unattractive  • Old  • Anxious  • Lonely  • Frustrated  • Overwhelmed  • Scared'
        )
        
    elif instance.form_type == 'female_pattern_hair_loss':
        # Question 1 
        Question.objects.get_or_create(
            form = instance,
            question_no = 1,
            question_value = '1) Age – please tick relevant box',
        )
        # Question 2
        Question.objects.get_or_create(
            form = instance,
            question_no = 2,
            question_value = '2) Previous products and treatments used – please tick all that apply',
        )
        # Question 3 
        Question.objects.get_or_create(
            form = instance,
            question_no = 3,
            question_value = '3) Where do you get your hair loss advice from? ',
        )
        # Question 4
        Question.objects.get_or_create(
            form = instance,
            question_no = 4,
            question_value = '4) Please rate the severity of your hair loss based on the standardised Hamilton Norwood Scale'
        )
        # Question 5 
        Question.objects.get_or_create(
            form = instance,
            question_no = 5,
            question_value = '5) Are you allergic to Minoxidil?'
        )
        # Question 6
        Question.objects.get_or_create(
            form = instance,
            question_no = 6,
            question_value = '6) Do you have any of the following on your scalp • Redness • Inflammation • Open cuts/wounds on the scalp'
        )
        # Question 7 
        Question.objects.get_or_create(
            form = instance,
            question_no = 7,
            question_value = '7) Please select as appropriate'
        )
        # Question 8 
        Question.objects.get_or_create(
            form = instance,
            question_no = 8,
            question_value = '8) I have a personal or family history of breast cancer '
        )
        # Question 9
        Question.objects.get_or_create(
            form = instance,
            question_no = 9,
            question_value = '9) How much does your hair loss affect you? (0 = not affected at all, 10 = significantly affected) 0 – 1 - 2 – 3 – 4 - 5 – 6 – 7 – 8 – 9 - 10'
        )
        # Question 10
        Question.objects.get_or_create(
            form = instance,
            question_no = 10,
            question_value = '10) How does the hair loss make you feel? Tick all that apply'
        )

    elif instance.form_type == 'beard':
        # Question 1 
        Question.objects.get_or_create(
            form = instance,
            question_no = 1,
            question_value = '1) Age – please tick relevant box',
        )
        # Question 2
        Question.objects.get_or_create(
            form = instance,
            question_no = 2,
            question_value = '2) Previous products and treatments used – please tick all that apply',
        )
        # Question 3 
        Question.objects.get_or_create(
            form = instance,
            question_no = 3,
            question_value = '3) Where do you get your hair loss advice from? ',
        )
        # Question 4
        Question.objects.get_or_create(
            form = instance,
            question_no = 4,
            question_value = '4) Please tick the box that best describes your pattern of beard hair loss'
        )
        # Question 5 
        Question.objects.get_or_create(
            form = instance,
            question_no = 5,
            question_value = '5) Are you allergic to Minoxidil?'
        )
        # Question 6
        Question.objects.get_or_create(
            form = instance,
            question_no = 6,
            question_value = '6) Do you have any of the following on the skin under your beard'
        )
        # Question 7 
        Question.objects.get_or_create(
            form = instance,
            question_no = 7,
            question_value = '7) How much does your hair loss affect you?'
        )
        # Question 8 
        Question.objects.get_or_create(
            form = instance,
            question_no = 8,
            question_value = '8) How does the hair loss make you feel? Tick all that apply'
        )
    
    elif instance.form_type == 'lashes':
        # Question 1 
        Question.objects.get_or_create(
            form = instance,
            question_no = 1,
            question_value = '1) Age – please tick relevant box',
        )
        # Question 2
        Question.objects.get_or_create(
            form = instance,
            question_no = 2,
            question_value = '2) Previous products and treatments used – please tick all that apply',
        )
        # Question 3 
        Question.objects.get_or_create(
            form = instance,
            question_no = 3,
            question_value = '3) Where do you get your hair loss advice from? ',
        )
        # Question 4
        Question.objects.get_or_create(
            form = instance,
            question_no = 4,
            question_value = '4) Please tick the box that best describes the pattern of hair loss on your lashes'
        )
        # Question 5 
        Question.objects.get_or_create(
            form = instance,
            question_no = 5,
            question_value = '5) Do you have any of the following?'
        )
        # Question 6
        Question.objects.get_or_create(
            form = instance,
            question_no = 6,
            question_value = '6) Are you allergic to Latanoprost?'
        )
        # Question 7 
        Question.objects.get_or_create(
            form = instance,
            question_no = 7,
            question_value = '7) How much does your hair loss affect you?'
        )
        # Question 8 
        Question.objects.get_or_create(
            form = instance,
            question_no = 8,
            question_value = '8) How does the hair loss make you feel?'
        )

    elif instance.form_type == 'brows':
        # Question 1 
        Question.objects.get_or_create(
            form = instance,
            question_no = 1,
            question_value = '1) Age – please tick relevant box',
        )
        # Question 2
        Question.objects.get_or_create(
            form = instance,
            question_no = 2,
            question_value = '2) Previous products and treatments used – please tick all that apply',
        )
        # Question 3 
        Question.objects.get_or_create(
            form = instance,
            question_no = 3,
            question_value = '3) Where do you get your hair loss advice from? ',
        )
        # Question 4
        Question.objects.get_or_create(
            form = instance,
            question_no = 4,
            question_value = '4) Please tick the box that best describes your pattern of brow hair loss'
        )
        # Question 5 
        Question.objects.get_or_create(
            form = instance,
            question_no = 5,
            question_value = '5) Are you allergic to Minoxidil ?'
        )
        # Question 6
        Question.objects.get_or_create(
            form = instance,
            question_no = 6,
            question_value = '6) Do you have any of the following affecting the skin around your eye brows ?'
        )
        # Question 7 
        Question.objects.get_or_create(
            form = instance,
            question_no = 7,
            question_value = '7) How much does your hair loss affect you ?'
        )
        # Question 8 
        Question.objects.get_or_create(
            form = instance,
            question_no = 8,
            question_value = '8) How does the hair loss make you feel ?'
        )

    elif instance.form_type == 'post_chemotheraphy_hair_loss':
        # Question 1 
        Question.objects.get_or_create(
            form = instance,
            question_no = 1,
            question_value = '1) Age – please tick relevant box',
        )
        # Question 2
        Question.objects.get_or_create(
            form = instance,
            question_no = 2,
            question_value = '2) Previous products and treatments used – please tick all that apply',
        )
        # Question 3 
        Question.objects.get_or_create(
            form = instance,
            question_no = 3,
            question_value = '3) Where do you get your hair loss advice from? ',
        )
        # Question 4
        Question.objects.get_or_create(
            form = instance,
            question_no = 4,
            question_value = '4) Please tick as appropriate'
        )
        # Question 5 
        Question.objects.get_or_create(
            form = instance,
            question_no = 5,
            question_value = '5) Are you allergic to Minoxidil ?'
        )
        # Question 6
        Question.objects.get_or_create(
            form = instance,
            question_no = 6,
            question_value = '6) Do you have any of the following on your scalp ?'
        )
        # Question 7 
        Question.objects.get_or_create(
            form = instance,
            question_no = 7,
            question_value = '7) How much does your hair loss affect you ?'
        )
        # Question 8 
        Question.objects.get_or_create(
            form = instance,
            question_no = 8,
            question_value = '8) How does the hair loss make you feel ?'
        )
    
    elif instance.form_type == 'traction_related_hair_loss':
        # Question 1 
        Question.objects.get_or_create(
            form = instance,
            question_no = 1,
            question_value = '1) Age – please tick relevant box',
        )
        # Question 2
        Question.objects.get_or_create(
            form = instance,
            question_no = 2,
            question_value = '2) Previous products and treatments used – please tick all that apply',
        )
        # Question 3 
        Question.objects.get_or_create(
            form = instance,
            question_no = 3,
            question_value = '3) Where do you get your hair loss advice from? ',
        )
        # Question 4
        Question.objects.get_or_create(
            form = instance,
            question_no = 4,
            question_value = '4) Please tick as appropriate'
        )
        # Question 5 
        Question.objects.get_or_create(
            form = instance,
            question_no = 5,
            question_value = '5) What hairstyling practices have you used in the past ?'
        )
        # Question 6
        Question.objects.get_or_create(
            form = instance,
            question_no = 6,
            question_value = '6) What hairstyling practices do you currently use ?'
        )
        # Question 7 
        Question.objects.get_or_create(
            form = instance,
            question_no = 7,
            question_value = '7) Are you allergic to Minoxidil ?'
        )
        # Question 8 
        Question.objects.get_or_create(
            form = instance,
            question_no = 8,
            question_value = '8) Do you have any of the following on your scalp ?'
        )
        # Question 9 
        Question.objects.get_or_create(
            form = instance,
            question_no = 9,
            question_value = 'How much does your hair loss affect you ?'
        )
        # Question 10
        Question.objects.get_or_create(
            form = instance,
            question_no = 10,
            question_value = 'How does the hair loss make you feel? '
        )
        
    elif instance.form_type == 'hair_shedding':
        # Question 1 
        Question.objects.get_or_create(
            form = instance,
            question_no = 1,
            question_value = '1) Age – please tick relevant box',
        )
        # Question 2
        Question.objects.get_or_create(
            form = instance,
            question_no = 2,
            question_value = '2) Previous products and treatments used – please tick all that apply',
        )
        # Question 3 
        Question.objects.get_or_create(
            form = instance,
            question_no = 3,
            question_value = '3) Where do you get your hair loss advice from? ',
        )
        # Question 4
        Question.objects.get_or_create(
            form = instance,
            question_no = 4,
            question_value = '4) Please select the image that most resembles the extent of your hair loss.'
        )
        # Question 5 
        Question.objects.get_or_create(
            form = instance,
            question_no = 5,
            question_value = '5) There are many potential triggers for increased hair shedding. These typically happen within the 3-6 months before shedding starts ?'
        )
        # Question 6
        Question.objects.get_or_create(
            form = instance,
            question_no = 6,
            question_value = '6) Are you allergic to Minoxidil ?'
        )
        # Question 7 
        Question.objects.get_or_create(
            form = instance,
            question_no = 7,
            question_value = '7) Do you have any of the following on your scalp ?'
        )
        # Question 8 
        Question.objects.get_or_create(
            form = instance,
            question_no = 8,
            question_value = '8) How much does your hair loss affect you ?'
        )
        # Question 9
        Question.objects.get_or_create(
            form = instance,
            question_no = 9,
            question_value = '9) How does the hair loss make you feel ?'
        )
        
        
        