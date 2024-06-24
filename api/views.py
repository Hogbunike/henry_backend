from django.shortcuts import render
import json
import datetime
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import json
from .utils.dowell_hash import *
from .utils.event_function import create_event
from .utils.datacube import *
from .utils.dowellconnection import *
import datacube
from .models import RandomSession

username = "henry"
country = "nig"

def get_collection_name(username, country):
    collection_name = f"{country}_{username[0].lower()}"
    return collection_name


data = {
    "api_key": "82a7d2ed-c24d-4b55-9a3a-83d6273809d9",
    "db_name": "login_test",
    "coll_name": get_collection_name(username, country),
    "operation": "fetch",
}

print(data)

res = requests.post(
    "https://datacube.uxlivinglab.online/db_api/get_data/", json=data)

users = json.loads(res.text)
print(users)


# Create your views here.

def register_legal_policy(user):
    policy_url = "https://100087.pythonanywhere.com/api/legalpolicies/ayaquq6jdyqvaq9h6dlm9ysu3wkykfggyx0/iagreestatus/"
    RandomSession.objects.create(
        sessionID=user, status="Accepted", username=user)
    time = datetime.datetime.now()
    data = {
        "data": [
            {
                "event_id": "FB1010000000167475042357408025",
                "session_id": user,
                "i_agree": "true",
                "log_datetime": time,
                "i_agreed_datetime": time,
                "legal_policy_type": "app-privacy-policy"
            }
        ],
        "isSuccess": "true"
    }
    requests.post(policy_url, data=data)
    return "success"

def get_or_create_collection(collection_name):

    url = "https://datacube.uxlivinglab.online/db_api/collections/"
    payload = {
        "api_key": "82a7d2ed-c24d-4b55-9a3a-83d6273809d9",
        "db_name": "login_test",
        "payment": False
    }
    response = requests.get(url, params=payload)
    collections=response.json()

    if collection_name in collections["data"][0]:
    # if collection_name in json.loads(collections)["data"][0]:
        return collection_name

    url="https://datacube.uxlivinglab.online/db_api/add_collection/"
    del payload["payment"]
    payload["coll_names"] = collection_name
    payload["num_collections"] = 1
    collection = requests.post(url, json=payload)
    return collection_name

@api_view(["POST"])
def register(request):
    start=datetime.datetime.now()
    user = request.data["Username"]
    otp_input = request.data.get("otp")
    sms_input=request.data.get("sms")
    image = request.data.get("Profile_Image")
    password = request.data.get("Password")
    first = request.data.get("Firstname")
    last = request.data.get("Lastname")
    email = request.data.get("Email")
    phonecode = request.data.get("phonecode")
    phone = request.data.get("Phone")
    user_type = request.data.get('user_type')
    user_country = request.data.get('user_country')
    policy_status = request.data.get('policy_status')
    other_policy = request.data.get('other_policy')
    newsletter = request.data.get('newsletter')

    #Email and SMS verification

    email_data = {
        "api_key": "82a7d2ed-c24d-4b55-9a3a-83d6273809d9",
        "db_name": "login_test",
        "collection_name": "email_otp",
        "filters": {                   
            "email": email,"otp":otp_input
        },
        "payment":False
    }
    check_otp = datacube.datacube_data_retrieval(**email_data)
    check_otp1 = json.loads(check_otp)
    if len(check_otp1["data"]) <= 0:
        return Response({'msg':'error','info':'Wrong Email OTP'},status=status.HTTP_400_BAD_REQUEST)

    if sms_input is not None:
        sms_data = {
            "api_key": "82a7d2ed-c24d-4b55-9a3a-83d6273809d9",
            "db_name": "login_test",
            "collection_name": "mobile_sms",
            "filters": {                   
                "phone": "+"+str(phonecode) + str(phone),"sms":sms_input
            },
            "payment":False
        }
        check_sms = datacube.datacube_data_retrieval(**sms_data)
        check_sms1 = json.loads(check_sms)
        if len(check_sms1["data"]) <= 0 and phone:
            return Response({'msg':'error','info':'Wrong Mobile SMS'},status=status.HTTP_400_BAD_REQUEST)

    url = "https://datacube.uxlivinglab.online/db_api/get_data/"
    #Main data attributes for signup database
    data = {
        "api_key": "82a7d2ed-c24d-4b55-9a3a-83d6273809d9",
        "operation": "fetch",
        "db_name": "login_test",
        "coll_name": "username_list",
        "filters": {
            "Username": user
        },
        "payment": False
    }

    # Check for username
    user_query = requests.post(url,json=data) 
    user_list = json.loads(user_query.text)
    if (len(user_list["data"]) > 0):
        return Response({'msg':'error','info': 'Username already taken'},status=status.HTTP_400_BAD_REQUEST)

    #Add username in policy model
    register_legal_policy(user)

    # Setup collection
    url="https://datacube.uxlivinglab.online/db_api/crud/"
    data["operation"]="insert"
    data["data"]={"Username":user,"Email":email,"Country":user_country}
    requests.post(url,json=data)

    #Even ID of user
    event_id = None
    try:
        res = create_event()
        event_id = res['event_id']
    except:
        pass

    serverclock = datetime.datetime.now().strftime('%d %b %Y %H:%M:%S')

    #Info of user to be inserted
    field={"Profile_Image":image,"Username":user,"Password": dowell_hash.dowell_hash(password),"Firstname":first,"Lastname":last,"Email":email,"phonecode":phonecode,"Phone":phone,"Policy_status":policy_status,"User_type":user_type,"eventId":event_id,"payment_status":"unpaid","safety_security_policy":other_policy,"user_country":user_country,"newsletter_subscription":newsletter,"joined_serverclock":serverclock}

    #Change collection value of main data attribute to user's collection
    collection_name=f'{user_country}_{user[0].lower()}'
    data["coll_name"] = get_or_create_collection(collection_name)

    #Putting main data values in database attribute 
    data["data"]=field

    #Inserting data to signup database as per their collection name
    user_json=requests.post(url,json=data)
    user_json1 = json.loads(user_json.text)
    inserted_id = user_json1["data"]['inserted_id']

    #Signup COnfirmation Mail
    url = "https://100085.pythonanywhere.com/api/signup-feedback/"
    if not sms_input:
        verified_phone="unverified"
    else:
        verified_phone="verified"
    payload = json.dumps({
        "topic" : "Signupfeedback",
        "toEmail" : email,
        "toName" : first +" "+ last,
        "firstname" : first,
        "lastname" : last,
        "username" : user,
        "phoneCode" : "+" + str(phonecode),
        "phoneNumber" : phone,
        "usertype" : user_type,
        "country" : user_country,
        "verified_phone":verified_phone,
        "verified_email": "verified"
            })
    headers = {
        'Content-Type': 'application/json'
    }
    response1 = requests.request("POST", url, headers=headers, data=payload)

    return Response({
        'message':f"{user}, registration success",
        'inserted_id':f"{inserted_id}"
        })

