import hmac
import json

import requests
import time
import hashlib

data = json.dumps({'adsf': 'adsf'})
# path_and_query = "/api/v1/create?TIMESTAMP="+str(int(time.time()))+"&ACCOUNT_ID=admin&foo=bar"
host = "http://127.0.0.1:5000"
path_and_query = "/api/v1/new?TIMESTAMP="+str(int(time.time()))+"&ACCOUNT_ID=admin&foo=bar"
msg = path_and_query+data
sig = hmac.new(";hi^897t7utf", digestmod=hashlib.sha1, msg=msg).hexdigest()
# req = requests.get(host+path_and_query, headers={'X-Auth-Signature': sig})


req2 = requests.post(host+path_and_query, data=data,
                   headers={'X-Auth-Signature': sig})

pass

# MAC = message authentication code. collision resistant - against two different inputs for same output