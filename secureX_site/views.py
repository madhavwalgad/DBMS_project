from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.http import HttpResponse
from secureX_site.forms import UserRegisterForm
from secureX_site.models import Service,RequestService,BranchLocation,JobApplication,Profile,Order,OrderItem,Course,OpenJob
from .forms import RequestForm,JobApplicationForm,CheckoutForm,AddressForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from secureX_site.extras import generate_order_id
import datetime

def index(request):

    #number of services provided 
    num_services = Service.objects.all().count()

    context = {
        'num_services': num_services
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'secureX_site/index.html', context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'secureX_site/register.html', {'form': form})   

def Career_page(request):
    openjob = OpenJob.objects.all()
    context = {
        'openjob': openjob
    }
    return render(request, 'secureX_site/career.html', context)

def Service_index(request):
    services = Service.objects.all()
    context = {
        'services': services
    }
    return render(request, 'secureX_site/service.html', context)    

def Service_request(request):
    if request.method == 'POST':
          form = RequestForm(request.POST)
          if form.is_valid():
            form.save()
            messages.success(request, f'Your request has been submitted')
            return redirect('services')
    else:    
      form=RequestForm()
    return render(request,'secureX_site/requestservice.html',{'form':form})

def Branch_index(request):
    branches = BranchLocation.objects.all()
    context = {
        'branches': branches
    }
    return render(request, 'secureX_site/branch.html', context)


@login_required
def Job_Request(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            jobapplication = form.save(commit=False)
            jobapplication.user = request.user
            jobapplication.save()
            messages.success(request, f'Your job application has been submitted, We will contact you for further enquiry')
            return redirect('career')
    else:
        form = JobApplicationForm()
    return render(request, 'secureX_site/jobapplication.html', {'form': form})
@login_required
def my_profile(request):
    my_user_profile = Profile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
    context = {
        'my_orders': my_orders
    }

    return render(request, "secureX_site/profile.html", context)

@login_required
def course_list(request):
    object_list = Course.objects.all()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_courses = []
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_courses = [course.course for course in user_order_items]

    context = {
        'object_list': object_list,
        'current_order_courses': current_order_courses
    }

    return render(request, "secureX_site/course_list.html", context)   

def get_user_pending_order(request):
    
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        return order[0]
    return 0     

@login_required
def add_to_cart(request,**kwargs):
    user_profile = get_object_or_404(Profile, user=request.user)
    course = Course.objects.filter(id=kwargs.get('item_id',"")).first()
    if course in  request.user.profile.course.all():
        messages.info(request,'You already bought this course')
        return redirect(reverse('course-list'))
    order_item, status = OrderItem.objects.get_or_create(course=course)
    user_order, status = Order.objects.get_or_create(owner=user_profile,is_ordered=False)
    user_order.items.add(order_item)
    if status:
        user_order.ref_code = generate_order_id()
        user_order.save()
    messages.info(request,'Course added to cart')
    return redirect(reverse('course-list'))

@login_required
def delete_from_cart(request,item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request,'Course has been removed')
    return redirect(reverse('order_summary'))

@login_required
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'secureX_site/order_summary.html',context)

@login_required
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            orderf = form.save(commit=False)
            orderf.owner = request.user.profile
            orderf.save()
    else:    
      form=CheckoutForm
      existing_order = get_user_pending_order(request)
      context = {
        'order': existing_order
      }
      context.update({"form":form})
      return render(request, 'secureX_site/checkout.html',context)




@login_required
def process_payment(request,order_id):
    return redirect(reverse('update_records',
                     kwargs={
                         'order_id': order_id,
                     })
                )         

@login_required
def update_transaction_records(request, order_id):
    order_to_purchase = Order.objects.filter(pk=order_id).first()
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()
    order_items = order_to_purchase.items.all()
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())
    user_profile = get_object_or_404(Profile,user=request.user)
    order_courses = [item.course for item in order_items]
    user_profile.course.add(*order_courses)
    user_profile.save()
    messages.info(request,'Thank You! Your Courses have been added to your Profile')
    return redirect(reverse('my_profile'))

def success(request,**kwargs):
    return render(request,'secureX_site/purchase_success.html',{})


@login_required
def formdelivery(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            deliveryadd = form.save(commit=False)
            deliveryadd.user = request.user
            deliveryadd.save()
            messages.success(request, f'Your address has been updated')
            return redirect('my_profile')
    else:
        form = AddressForm()
    return render(request, 'secureX_site/deliveryaddress.html', {'form': form})