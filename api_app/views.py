from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import hashlib
import secrets
import json
from .forms import TransactionForm, CheckStatusForm
from .models import Transaction, ApiResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'api_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'api_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def generate_random_sha256():
    random_string = secrets.token_hex(32)
    sha256_hash = hashlib.sha256(random_string.encode()).hexdigest()
    return sha256_hash

@login_required
def dashboard(request):
    transactions = Transaction.objects.all()
    return render(request, 'api_app/dashboard.html', {'transactions': transactions})

@login_required
def transaction_request(request):
    response_data = None
    error_message = None

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.external_reference = generate_random_sha256()
            transaction.save()

            url = 'https://uat-businessapi.spenn.com/api/Partner/transaction/request'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer eyJhbG...NrEQ41w'  # Replace with your actual bearer token
            }
            callback_url = request.build_absolute_uri('/api/callback/')
            payload = {
                "phoneNumber": transaction.phone_number,
                "amount": transaction.amount,
                "message": transaction.message,
                "callbackUrl": callback_url,
                "externalReference": transaction.external_reference
            }

            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                response_data = response.json()
                transaction.request_id = response_data['requestId']
                transaction.status = response_data['status']
                transaction.save()
                ApiResponse.objects.create(
                    request_id=response_data['requestId'],
                    response_id=response_data['$id'],
                    status=response_data['status'],
                    external_reference=response_data['externalReference']
                )
            else:
                error_message = f"Request failed with status code {response.status_code}: {response.text}"
    else:
        form = TransactionForm()

    return render(request, 'api_app/transaction_form.html', {
        'form': form,
        'response_data': response_data,
        'error_message': error_message
    })

@login_required
def check_status(request):
    status_data = None
    error_message = None

    if request.method == 'POST':
        form = CheckStatusForm(request.POST)
        if form.is_valid():
            request_id = form.cleaned_data['request_id']

            url = f"https://uat-businessapi.spenn.com/api/Partner/transaction/request/{request_id}/status"
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer eyJhbG...NrEQ41w"
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                status_data = response.json()
            else:
                error_message = f"Error: {response.status_code} - {response.text}"
    else:
        form = CheckStatusForm()

    return render(request, 'api_app/check_status.html', {
        'form': form,
        'status_data': status_data,
        'error_message': error_message
    })

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            request_guid = data.get('RequestGuid')
            external_reference = data.get('ExternalReference')
            request_status = data.get('RequestStatus')
            response_id= data.get('$id')

            transaction = Transaction.objects.get(external_reference=external_reference)
            transaction.status = request_status
            transaction.save()

            ApiResponse.objects.create(
                request_id=request_guid,
                response_id=response_id,  # Add response ID if available
                status=request_status,
                external_reference=external_reference
            )

            return JsonResponse({'status': 'success'}, status=200)
        except Transaction.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Transaction not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
