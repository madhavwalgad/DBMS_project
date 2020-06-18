from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('service/',views.Service_index,name='services'),
    path('requestservice/',views.Service_request,name='servicerequest'),
    path('branch/',views.Branch_index,name='branches'),
    path('jobapplication/',views.Job_Request,name='jobapplication'),
    path('add-to-cart/<int:item_id>/',views.add_to_cart,name='add_to_cart'),
    path('order-summary/',views.order_details,name='order_summary'),
    path('success/',views.success,name='purchase_success'),
    path('item/delete/<int:item_id>/',views.delete_from_cart,name='delete_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('payment/<int:order_id>/',views.process_payment,name='process-payment'),
    path('update-transaction/<int:order_id>/',views.update_transaction_records,name='update_records'),
    path('course/',views.course_list,name='course-list'),
    path('profile/',views.my_profile,name='my_profile'),
    path('deliveryadd/',views.formdelivery,name='deliveryadd'),
    path('career/',views.Career_page,name='career'),

]