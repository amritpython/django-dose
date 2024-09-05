from django.urls import path

from . import apiviews
from . import views

urlpatterns = [
    # Web Routes
    path('male_pattern_hair_loss',views.male_pattern_hair_loss_view),
    path('female_pattern_hair_loss',views.female_pattern_hair_loss_view),
    path('beard',views.men_beard_step_form_view),
    path('lashes',views.lashes_step_form_view),
    path('brows',views.brows_step_form_view),
    path('post_chemotheraphy_hair_loss',views.chemo_therapy_step_form_view),
    path('traction_related_hair_loss',views.traction_rela_ted_step_form_view),
    path('hair_shedding',views.hair_shedding_step_form_view),
    path('my_account',views.my_account_view),
    path('my_account/',views.my_account_view),
    path('dose_directory',views.dose_directory_view),
    path('consulation_result/<str:ref>',views.consulation_result_view),
    path('email/subscribe',views.email_subscribe_view),
    path('logout',views.logout_view),
    path('medicheck/orders',views.medicheck_orders_view),
    path('roseway/orders',views.roseway_orders_view),
    path('logs',views.logs_view),
    path('retake',views.retake_view),
    
    # Api Routes
    path('cart',apiviews.cart_apiview),
    path('product_fit',apiviews.product_fit_apiview),
    path('api/database',apiviews.database_apiview),

    # Cron Routes
    path('cron/currency_rate_update',apiviews.currency_rate_update_apiview),
]

