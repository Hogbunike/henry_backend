import hashlib
import base64
import json
from .dowellconnection import dowellconnection
def dowell_hash(pwd):
    if len(pwd)>=8:
        strtobase=base64.b64encode(pwd.encode())
        strtohash="!4@5#19*^82$37"
        ls=[i for ii in zip(list(strtobase.decode()),list(strtohash)) for i in ii]
        lstostr=''.join(map(str, ls))
        strhash=hashlib.sha256(str.encode('utf-8')).hexdigest()
        st=strhash[int(len((strhash))/2):]
        return f'{lstostr}dowell={st}'
    else:
        return "password less than 8 charector"
def dowell_authenticate(username,password):
    field={"Username":username,"Password":dowell_hash(password)}
    response=dowellconnection("login","bangalore","login","dowell_users","dowell_users","1116","ABCDE","fetch",field,"nil")
    resp=json.loads(response)
    if len(resp["data"])<1:
        return "username or password wrong"
    else:
        return resp
        # request.session["session_id"]=resp["data"][0]["role"]
        # field1={"Username":username,"session_id"=resp["data"][0]["role"]}
        # session=dowellconnection("login","bangalore","login","dowell_session","dowell_session","1119","ABCDE","insert",field,"nil")
# r=dowell_authenticate("Roshan","dowell1234")
#print(dowell_hash("dowell1234"))
# print(r)