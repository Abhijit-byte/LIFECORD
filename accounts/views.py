from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import random
import re
import json
import requests

otp_storage = {}

def send_otp_page(request):
    return render(request, 'accounts/send_otp.html')

def verify_otp_page(request):
    return render(request, 'accounts/verify_otp.html')

def dashboard(request):
    if 'phone' not in request.session:
        return redirect('/')
    return render(request, 'accounts/dashboard.html', {
        'phone': request.session.get('phone')
    })

@require_http_methods(["POST"])
@csrf_exempt




@require_http_methods(["POST"])
@csrf_exempt
def send_otp(request):
    # 🔍 DEBUG: Print credentials status
    instance_id = getattr(settings, 'ULTRAMSG_INSTANCE_ID', None)
    token = getattr(settings, 'ULTRAMSG_TOKEN', None)
    
    print(f"\n🔍 DEBUG INFO:")
    print(f"Instance ID present: {bool(instance_id)}")
    print(f"Token present: {bool(token)}")
    if instance_id:
        print(f"Instance ID: {instance_id}")
    print(f"{'='*50}\n")
    
    # ... rest of your code


    try:
        data = json.loads(request.body)
        phone = data.get("phone", "").strip()
        
        if not phone or not re.match(r"^\d{10}$", phone):
            return JsonResponse({
                "status": "error", 
                "message": "Invalid phone number"
            })
        
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        otp_storage[phone] = otp
        
        # Print OTP for testing
        print(f"\n{'='*50}")
        print(f"📱 OTP for {phone}: {otp}")
        print(f"{'='*50}\n")
        
        # Try to send via Ultramsg
        instance_id = getattr(settings, 'ULTRAMSG_INSTANCE_ID', None)
        token = getattr(settings, 'ULTRAMSG_TOKEN', None)
        
        if instance_id and token:
            try:
                url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
                payload = {
                    "token": token,
                    "to": f"91{phone}",  # Add country code
                    "body": f"🔐 Your LifeCord OTP is: *{otp}*\n\nThis code is valid for 5 minutes.\n\nDo not share this code with anyone.\n\n- LifeCord Team"
                }
                
                response = requests.post(url, data=payload, timeout=10)
                result = response.json()
                
                if response.status_code == 200 and result.get('sent') == 'true':
                    print(f"✅ OTP sent via WhatsApp to {phone}")
                else:
                    print(f"⚠️ Ultramsg API response: {result}")
                    print(f"⚠️ WhatsApp send failed, but OTP generated (check terminal)")
            except Exception as e:
                print(f"⚠️ Ultramsg error: {str(e)}")
                print(f"⚠️ OTP still available in terminal")
        else:
            print("❌ Ultramsg credentials not configured!")
        
        # Always return success (OTP works even without WhatsApp in TEST MODE)
        return JsonResponse({
            "status": "success", 
            "message": "OTP sent successfully"
        })
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return JsonResponse({
            "status": "error", 
            "message": str(e)
        })

@require_http_methods(["POST"])
@csrf_exempt
def verify_otp(request):
    try:
        data = json.loads(request.body)
        phone = data.get("phone", "").strip()
        otp = data.get("otp", "").strip()
        
        if phone in otp_storage and otp_storage[phone] == otp:
            del otp_storage[phone]
            request.session["phone"] = phone
            print(f"✅ OTP verified for {phone}")
            return JsonResponse({
                "status": "success", 
                "message": "OTP verified"
            })
        else:
            return JsonResponse({
                "status": "error", 
                "message": "Invalid or expired OTP"
            })
    
    except Exception as e:
        return JsonResponse({
            "status": "error", 
            "message": str(e)
        })
