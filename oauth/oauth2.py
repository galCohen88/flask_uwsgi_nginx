from flask import Flask
from oauth.flask_hmacauth import hmac_auth, DictAccountBroker, HmacManager

app = Flask(__name__)
accountmgr = DictAccountBroker(
    accounts={
        "admin": {"secret": ";hi^897t7utf", "rights": ["create", "edit", "delete", "view"]},
        "editor": {"secret": "afstr5afewr", "rights": ["create", "edit", "view"]},
        "guest": {"secret": "ASDFjoiu%i", "rights": ["view"]}
    })

hmacmgr = HmacManager(accountmgr, app)

@app.route('/api/v1/create')
@hmac_auth("create")
def create_thing():
    pass

@app.route('/api/v1/new', methods=["POST"])
@hmac_auth("edit")
def new_thing():
    pass

if __name__ == '__main__':
    app.run()
