from .dowellconnection import dowellconnection
import datetime
import requests
import json
def dowellclock():
        oldt=1609459200
        import time
        t1=time.time()
        dowell=t1-oldt
        return dowell
dd=datetime.datetime.now()
time=dd.strftime("%d/%m/%Y %H:%M:%S")
def timefun():
    dd=datetime.datetime.now()
    time=dd.strftime("%d:%m:%Y,%H:%M:%S")
    return time
d = datetime.datetime.strptime("2017-10-13T10:53:53.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
def event_creation(pfm_id,city_id,day_id,db_id,process_id,object_id,instance_id,context,rule,login_id,document_id,status_id,IP,session_id,location,regtime,datatype):
    pfm_code = pfm_id
    pfm={"platformcode":pfm_code}
    pfm_response=dowellconnection("mstr","bangalore","pfm","platform_master","pfm_master","97654321","ABCDE","fetch",pfm,"nil")
    if not pfm_code in pfm_response or pfm_response=="false":
        return "Platform code not matching"
    # return pfm_response
    else:
    #city_ID=re.findall('\d+',response)[0]
        pfm_id=pfm_code
    city_code = city_id
    city={"citycode":city_code}
    city_response=dowellconnection("mstr","bangalore","pfm","city_master","city_master","67654321","ABCDE","fetch",city,"nil")
    if not city_code in city_response or city_response=="false":
        return "City code not matching"
    else:
        city_id=city_code
    day_code = day_id
    day={"daycode":day_code}
    day_response=dowellconnection("mstr","bangalore","pfm","day_master","day_master","77654321","ABCDE","fetch",day,"nil")
    if not day_code in day_response or day_response=="false":
        return "day code not matching"
    else:
        day_id=day_code
    db_code =db_id
    db={"dbcode":db_code}
    db_response=dowellconnection("mstr","bangalore","pfm","db_master","db_master","37654321","ABCDE","find",db,"nil")
    if not db_code in db_response or db_response=="false":
        return "database code not matching"
    else:
        db_id=db_code
    process_code = process_id
    process={"processcode":process_code}
    process_response=dowellconnection("mstr","bangalore","pfm","process_master","process_master","57654321","ABCDE","fetch",process,"nil")
    if not process_code in process_response or process_response=="false":
        return "process code not matching"
    else:
        process_id=process_code
    object_code = object_id
    object={"objectcode":object_code}
    object_response=dowellconnection("mstr","bangalore","pfm","object_master","object_master","47654321","ABCDE","fetch",object,"nil")
    if not object_code in object_response or object_response=="false":
        return "object code not matching"
    else:
        object_id=object_code
    instance=instance_id
    if not instance:
        return "Instance is blank fill again"
    else:
        instance_id=instance
    Context=context
    if not rule:
        return "rules is blank fill again"
    else:
        rules=rule
    if not Context:
        return "Context is blank"
    else:
        timer=timefun
        context_is={"context":context,"rules":rules,"object_id":object_id,"login":login_id,"time":timer}
    document=document_id
    if not document:
        return "Document is blank"
    else:
        if len(document)>24:
            return "Invalid document id"
        elif len(document)<24:
            import time as t
            document=str(t.time())
            document.replace
            document=document.replace(".","5").zfill(24) # To fill prefix with zero to make length to 24
            document_id=document
    event_id=pfm_id+city_id+day_id+document_id
    status=status_id
    if not status:
        return "status is blank fill again"
    else:
        status_field=status
    if len(event_id) !=30:
        return "Error while creating Event ID"
    else:
        #newdate=datetime.datetime.strptime(request_data["dowell_time"], '%d/%m/%Y %H:%M:%S')
        #ls=[pfm_id,city_code,day_id,db_id,request_data["IP_Address"],request_data["login"],request_data["session"],process_id,
        #request_data["regional_time"],request_data["dowell_time"],request_data["location"],object_id,instance_id,context,document_id]
        field = {"eventId":event_id,
        "DatabaseId":db_id,"IP":IP,
        "login":login_id,"session":session_id,
        "process":process_id,"regional_time":regtime,
        "dowell_time":round(dowellclock()),"location":location,
        "object":object_id,"instane_id":instance_id,"context":context,"status":status_field,"data_type":datatype}
        NewObjectID=dowellconnection("FB","bangalore","blr","events","events","87654321","ABCDE","insert",field,"nil")
        #return f"NewObjectID : {NewObjectID} \n event_id :{event_id}"
        return event_id

def create_event():

    url="https://uxlivinglab.pythonanywhere.com/create_event"

    data={
        "platformcode":"FB" ,
        "citycode":"101",
        "daycode":"0",
        "dbcode":"pfm" ,
        "ip_address":"192.168.0.41", # get from dowell track my ip function
        "login_id":"lav", #get from login function
        "session_id":"new", #get from login function
        "processcode":"1",
        "location":"22446576", # get from dowell track my ip function
        "objectcode":"1",
        "instancecode":"100051",
        "context":"afdafa ",
        "document_id":"3004",
        "rules":"some rules",
        "status":"work",
        "data_type": "learn",
        "purpose_of_usage": "add",
        "colour":"color value",
        "hashtags":"hash tag alue",
        "mentions":"mentions value",
        "emojis":"emojis",
        "bookmarks": "a book marks"
    }

    r=requests.post(url,json=data)
    if r.status_code == 201:
        return json.loads(r.text)
    else:
        return json.loads(r.text)['error']