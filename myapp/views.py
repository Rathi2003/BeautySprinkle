from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from .models import *
from django.shortcuts import render,HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .services.razorpay_service import create_order, verify_payment 
from django.conf import settings
from .models import Payment  # Assuming Payment model is created




def index(request):
    detail=Detail.objects.all()
    return render(request,'index.html')

def lipstick(request):
    return render(request,'lipstick.html')
def serum(request):
    return render(request,'serum.html')
def eye(request):
    return render(request,'eye.html')
def mascara(request):
    return render(request,'mascara.html')
def mois(request):
    return render(request,'mois.html')

   




def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'login.html') 
    else:
        return render(request, 'login.html')  



def signup(request):
    if request.method=='POST':
        user_name=request.POST['uname']
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        email=request.POST['email']
        password1=request.POST['password']
        password2=request.POST['cpassword']
        user=User.objects.create_user(username=user_name,first_name=first_name,last_name=last_name,email=email,password=password1)
        user.save()
        send_mail(
            'Beauty Sprinkle',#subject
            'welcome to Beauty Sprinkle',#message
            'brathi303@gmail.com',#from mail
            [email],#to mail
            fail_silently=False,
        )

        print("user Created")
        return redirect('/')
    else:
        return render(request,'signup.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


def initiate_payment(request):
    if request.method == "POST":
        a=request.POST['name']
        b=request.POST['email']
        e=request.POST['address']
        f=request.POST['contact']
        detail=Detail(name=a,email=b,address=e,contact=f)
        detail.save()   
        send_mail(
            'Beauty Sprinkle ',#subject
            'Your Order is Placed ',#message 
            'brathi303@gmail.com',#from mail
            [b],#to mail
            fail_silently=False,
            )
        amount_str = request.POST.get('amount', '').strip()  # Get amount and remove any whitespace
        if not amount_str or not amount_str.isdigit():  # Check if amount is missing or not a valid number
            return render(request, 'payments/pay.html', {
                'error': 'Please enter a valid amount.'
            })
        
        amount = int(amount_str)  # Convert to int only after validation

        order = create_order(amount)  # Create Razorpay order
        context = {
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'order_id': order['id'],
            'amount': amount * 100,  # Convert to paise for Razorpay
            'currency': order['currency'],
        }
        return render(request, 'payments/checkout.html', context)

    return render(request, 'buynow.html')


@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')
        amount_in_paise = request.POST.get('amount')  # Amount is in paise

        if verify_payment(payment_id, order_id, signature):
            amount_in_rupees = int(amount_in_paise) / 100  # Convert paise to rupees before saving
            Payment.objects.create(
                payment_id=payment_id,
                order_id=order_id,
                amount=amount_in_rupees,  # Save the amount in rupees
                status='Success'
            )
            return render(request, 'payments/success.html')
        else:
            amount_in_rupees = int(amount_in_paise) / 100  # Convert paise to rupees
            Payment.objects.create(
                payment_id=payment_id,
                order_id=order_id,
                amount=amount_in_rupees,  # Save the amount in rupees
                status='Failed'
            )
            return render(request, 'payments/failure.html')
    return redirect('initiate_payment')





