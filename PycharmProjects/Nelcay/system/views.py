import base64

from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import requests
from django.core.mail import send_mail
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient
from django.contrib import messages
from django.conf import settings
from google.rpc.http_pb2 import HttpResponse
from requests.auth import HTTPBasicAuth
from Nelcay import firebase_config
from Nelcay.firebase_config import db


from .models import OrderHere


from .forms import OrderHereForm, ContactForm, LoginForm, RegisterForm, OrderForm
import json
from django import forms

from .models import OrderHere, FLAVOUR_PRICES
from .models import FLAVOUR_CHOICES


# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                subject=f"New message from {name}",
                message=f"Sender: {email}\n\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
            )

            messages.success(request, "Thank you for reaching out! I’ll get back to you soon.")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def gallery(request):
    return render(request, 'gallery.html')

def profile(request):
    return render(request, 'profile.html')

def edit(request):
    return render(request, 'edit.html')




def pricing(request):
    return render(request, 'pricing.html')


# def order_view(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             # 1. Capture Data
#             flavour_name = form.cleaned_data['flavour']
#             weight = float(form.cleaned_data['weight'])
#
#             # User details from hidden fields
#             c_name = form.cleaned_data.get('customer_name') or "Guest"
#             c_email = form.cleaned_data.get('customer_email') or "No Email"
#
#             # 2. Calculate Costs Server-Side
#             price_per_kg = FLAVOUR_PRICES.get(flavour_name, 2000)
#             total_price = price_per_kg * weight
#             deposit_amount = total_price * 0.5  # 50% Deposit
#
#             # 3. Safely extract first and last name for the database
#             name_parts = c_name.split()
#             first_name = name_parts[0] if name_parts else "Guest"
#             last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
#
#             # 4. Create Order (EXACT mapping to OrderHere models.py)
#             order = OrderHere.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 email_address=c_email,
#                 flavour=flavour_name,
#                 quantity=weight,
#                 message=f"Date: {form.cleaned_data.get('date_needed')} | Msg: {form.cleaned_data.get('cake_message')} | Details: {form.cleaned_data.get('details')}",
#
#                 # Default required fields
#                 phone_number="Pending",
#                 whatsapp_number="Pending",
#                 residence="nairobi",
#                 pastry="cake",
#                 occasion="other",
#                 measurement="kgs"
#             )
#
#             # 5. Store Session variables for the Payment page & Webhook
#             request.session['order_id'] = order.id
#             request.session['order_data'] = {
#                 'customer_name': c_name,
#                 'customer_email': c_email,
#                 'flavour': flavour_name,
#                 'weight': weight,
#                 'total_price': total_price,
#                 'deposit_amount': deposit_amount,
#             }
#
#             return redirect('payment')
#     else:
#         form = OrderForm()
#
#     return render(request, 'order.html', {'form': form, 'flavour_prices': FLAVOUR_PRICES})



def order_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # 1. Capture Data (Exactly like your first view)
            flavour_name = form.cleaned_data['flavour']
            weight = float(form.cleaned_data['weight'])  # Using 'quantity' as weight

            c_name = form.cleaned_data.get('customer_name') or "Guest"
            c_email = form.cleaned_data.get('customer_email') or "No Email"

            # 2. Calculate Costs Server-Side
            price_per_kg = FLAVOUR_PRICES.get(flavour_name, 2000)
            total_price = price_per_kg * weight
            deposit_amount = total_price * 0.5  # 50% Deposit

            # 3. Format names
            name_parts = c_name.split()
            first_name = name_parts[0] if name_parts else "Guest"
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

            # 4. Prepare data for Firebase
            order_data = {
                'first_name': first_name,
                'last_name': last_name,
                'email_address': c_email,
                'flavour': flavour_name,
                'quantity': weight,
                'message': f"Date: {form.cleaned_data.get('date_needed')} | Msg: {form.cleaned_data.get('cake_message')} | Details: {form.cleaned_data.get('details')}",
                'total_price': total_price,
                'deposit_amount': deposit_amount,
                'status': 'pending',
                'created_at': datetime.now().isoformat()
            }

            # 5. Save to Firebase (Bypassing SQL Read-Only Error)
            try:
                print("DEBUG: About to write to Firebase")
                doc_ref = firebase_config.db.collection('orders').add(order_data)
                print("DEBUG: Firebase write success, ID =", doc_ref[1].id)
            except Exception as e:
                print(f"DEBUG: FIREBASE ERROR: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()

            # 6. Store Session variables
            request.session['order_id'] = doc_ref[1].id
            request.session['order_data'] = {
                'customer_name': c_name,
                'customer_email': c_email,
                'flavour': flavour_name,
                'weight': weight,
                'total_price': total_price,
                'deposit_amount': deposit_amount,
            }

            return redirect('payment')
    else:
        form = OrderForm()

    return render(request, 'order.html', {'form': form, 'flavour_prices': FLAVOUR_PRICES})



# def order_view(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             # SUCCESS PATH
#             print("DEBUG: FORM IS VALID. SAVING...")
#             # This line is likely where the crash happens
#             # By removing Firebase, we confirm if it's the DB or the cloud
#             return redirect('payment')
#         else:
#             # THIS IS THE KEY! If form is invalid, this will print why.
#             print(f"DEBUG: FORM IS INVALID: {form.errors}")
#             return HttpResponse(f"Form errors: {form.errors}")
#     else:
#         form = OrderForm()
#     return render(request, 'order.html', {'form': form, 'flavour_prices': FLAVOUR_PRICES})

def add(request):
    return render(request, 'add.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request)
                messages.success(request, f"Welcome back, {username}!")
                # Redirect to the 'next' page if it exists (e.g. attempting to order), else home
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('index') # Assuming you have a URL named 'index' for home
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after registration
            login(request, user)
            messages.success(request, "Registration successful! Welcome to the family.")
            return redirect('index')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# ==========================================
#  LOGOUT VIEW
# ==========================================
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


def payment(request):
    order_data = request.session.get('order_data')
    if not order_data:
        messages.error(request, "No active order found.")
        return redirect('order')
    return render(request, 'payment.html', {'order': order_data})


# ==========================================
#  M-PESA API LOGIC (Fixed for Till Number)
# ==========================================


def get_mpesa_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_url = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials' if settings.MPESA_ENVIRONMENT == 'production' else 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    # The firewall blocks generic Python requests.
    # We must explicitly set headers that mimic a browser.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Connection': 'keep-alive'
    }

    try:
        r = requests.get(
            api_url,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
            headers=headers,
            timeout=10 # Add a timeout so it doesn't hang forever
        )
        r.raise_for_status()
        return r.json()['access_token']
    except Exception as e:
        print(f"DEBUG: M-PESA TOKEN ERROR: {e}")
        # If Safaricom returns 403, it means your IP is blocked.
        # Check if you are on a VPN and turn it OFF.
        return None


def mpesaapi(request):
    print("\n--- MPESA API VIEW TRIGGERED ---")  # TRACKER 1
    if request.method == 'POST':
        order_data = request.session.get('order_data')
        if not order_data:
            messages.error(request, "Session expired.")
            return redirect('order')

        raw_phone = request.POST.get('phonenumber')
        try:
            amount = int(float(request.POST.get('amount')))
        except:
            amount = 1

        phone = raw_phone.replace('+', '').replace(' ', '').strip()
        if phone.startswith('07') or phone.startswith('01'):
            phone = '254' + phone[1:]

        access_token = get_mpesa_access_token()
        if not access_token:
            messages.error(request, "Failed to connect to M-Pesa.")
            return redirect('payment')

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        passkey = settings.MPESA_PASSKEY
        business_short_code = settings.MPESA_EXPRESS_SHORTCODE

        password_str = business_short_code + passkey + timestamp
        password = base64.b64encode(password_str.encode()).decode()

        payload = {
            "BusinessShortCode": business_short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",  # Dummy URL since we are polling instead
            "AccountReference": "Nelcay Treats",
            "TransactionDesc": "Cake Deposit"
        }

        api_url = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest' if settings.MPESA_ENVIRONMENT == 'production' else 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            response_data = response.json()

            if response_data.get('ResponseCode') == '0':
                # SAVE THE CHECKOUT ID TO THE SESSION
                request.session['checkout_request_id'] = response_data.get('CheckoutRequestID')

                # Redirect to the waiting page
                return redirect('payment_processing')
            else:
                err = response_data.get('errorMessage', 'Unknown error.')
                messages.error(request, f"M-Pesa Failed: {err}")

        except Exception as e:
            messages.error(request, f"Connection failed: {str(e)}")

        return redirect('payment')
    return redirect('payment')


def payment_processing(request):
    """Renders the loading page where the user waits for the M-Pesa prompt."""
    if not request.session.get('checkout_request_id'):
        return redirect('index')
    return render(request, 'payment_processing.html')


@csrf_exempt
def check_payment_status(request):
    access_token = get_mpesa_access_token()
    print(f"DEBUG: Token generated: {access_token}")  # Add this
    if not access_token:
        return JsonResponse({'status': 'pending', 'message': 'No Token'})
    """
    Checks the status of the M-Pesa STK push.
    Returns 'pending' to keep the loader active, 'success' to redirect,
    or 'failed' to alert the user.
    """
    checkout_request_id = request.session.get('checkout_request_id')
    order_id = request.session.get('order_id')

    if not checkout_request_id:
        return JsonResponse({'status': 'error', 'message': 'No transaction found.'})

    access_token = get_mpesa_access_token()
    if not access_token:
        return JsonResponse({'status': 'pending', 'message': 'Connecting...'})

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    passkey = settings.MPESA_PASSKEY
    business_short_code = settings.MPESA_EXPRESS_SHORTCODE
    password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()

    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "CheckoutRequestID": checkout_request_id
    }

    api_url = 'https://api.safaricom.co.ke/mpesa/stkpushquery/v1/query' if settings.MPESA_ENVIRONMENT == 'production' else 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        res_data = response.json()

        # DEBUG: Print this to your terminal so you can see if the code is 0
        print(f"DEBUG: M-PESA QUERY RESPONSE: {res_data}")

        result_code = str(res_data.get('ResultCode', ''))
        result_desc = str(res_data.get('ResultDesc', '')).lower()

        # Handle Processing or Initial State
        # Added check for result_code '1' (often used for initial 'not found' or 'processing')
        if not result_code or result_code in ['1037', '1'] or 'processing' in result_desc:
            return JsonResponse({'status': 'pending', 'message': 'Processing...'})

        # Handle Success
        if result_code == '0':
            if order_id:
                # Update Firebase (this seems to be working!)
                firebase_config.db.collection('orders').document(order_id).update({
                    'payment_status': 'Paid',
                    'status': 'confirmed'
                })
            # THIS IS WHAT THE JAVASCRIPT IS LOOKING FOR:
            return JsonResponse({'status': 'success', 'message': 'Payment successful!'})

        # Handle Cancellation
        if result_code == '1032':
            return JsonResponse({'status': 'cancelled', 'message': 'You cancelled the prompt.'})

        # Real Failure
        return JsonResponse({'status': 'failed', 'message': res_data.get('ResultDesc', 'Payment failed.')})

    except Exception as e:
        print(f"DEBUG: QUERY EXCEPTION: {e}")
        return JsonResponse({'status': 'pending', 'message': 'Connecting...'})

# @login_required
# @user_passes_test(is_baker)
def baker_portal(request):
    """
    Renders the Baker's Portal dashboard.
    Fetches orders from OrderHere model.
    """
    today = timezone.now().date()

    # Fetch all orders (Sorted by creation date)
    active_orders = OrderHere.objects.all().order_by('-created_at')

    pending_count = active_orders.count()
    delivery_today_count = 0

    # Check if delivery_date exists before filtering to avoid crashes
    if hasattr(OrderHere, 'delivery_date'):
        delivery_today_count = active_orders.filter(delivery_date=today).count()
    elif hasattr(OrderHere, 'date_needed'):
        delivery_today_count = active_orders.filter(date_needed=today).count()

    context = {
        'orders': active_orders,
        'pending_orders_count': pending_count,
        'delivery_today_count': delivery_today_count,
    }

    return render(request, 'baker_portal.html', context)


# @login_required
# @user_passes_test(is_baker)
def update_order(request, order_id):
    """
    Handles POST requests from the Baker Portal.
    Includes safety checks for model fields.
    """
    if request.method == 'POST':
        order = get_object_or_404(OrderHere, id=order_id)

        # 1. Update Decoration Cost
        decoration_cost = request.POST.get('decoration_cost')
        if decoration_cost and decoration_cost.strip():
            try:
                cost = float(decoration_cost)
                if cost > 0:
                    if hasattr(order, 'decoration_cost'):
                        order.decoration_cost = cost
                        # Update total if fields exist
                        if hasattr(order, 'total_price') and hasattr(order, 'base_price'):
                            order.total_price = order.base_price + cost
                        order.save()
                        messages.success(request, f"Added decoration cost: KES {cost}")
                    else:
                        messages.warning(request, "Model field 'decoration_cost' is missing.")
            except ValueError:
                messages.error(request, "Invalid amount entered.")

        # 2. Update Status
        new_status = request.POST.get('status')
        if new_status:
            if hasattr(order, 'status'):
                order.status = new_status
                order.save()
                messages.info(request, f"Order updated to: {new_status}")
            else:
                messages.warning(request, "Model field 'status' is missing.")

        # 3. Send Prompt Logic
        action = request.POST.get('action')
        if action == 'send_prompt':
            c_name = getattr(order, 'first_name', 'Client')
            messages.success(request, f"Payment prompt sent to {c_name}.")

        return redirect('baker_portal')

    return redirect('baker_portal')

@csrf_exempt
@csrf_exempt
def mpesa_callback(request):

    if request.method == "POST":

        try:
            data = json.loads(request.body)
            print("M-Pesa Callback:", data)

            callback = data.get("Body", {}).get("stkCallback", {})

            result_code = callback.get("ResultCode")

            # If payment successful
            if result_code == 0:

                items = callback.get("CallbackMetadata", {}).get("Item", [])

                mpesa_receipt = None
                amount = None
                phone = None

                for item in items:
                    if item.get("Name") == "MpesaReceiptNumber":
                        mpesa_receipt = item.get("Value")

                    if item.get("Name") == "Amount":
                        amount = item.get("Value")

                    if item.get("Name") == "PhoneNumber":
                        phone = item.get("Value")

                print("Receipt:", mpesa_receipt)
                print("Amount:", amount)
                print("Phone:", phone)

                # Get order from session
                order_id = request.session.get("order_id")

                if order_id:
                    order = OrderHere.objects.get(id=order_id)

                    order.payment_status = "Paid"
                    order.save()

                    print(f"Order {order_id} marked as PAID")

            else:
                print("Payment failed")

        except Exception as e:
            print("Callback error:", str(e))

        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})