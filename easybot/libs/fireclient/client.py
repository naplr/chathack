import pyrebase

config = {
    "apiKey": "AIzaSyBbLf8k4NKQVXfjMg--POKkiQjHi2yuTxc",
    "authDomain": "chathack-db0fb.firebaseapp.com",
    "databaseURL": "https://chathack-db0fb.firebaseio.com",
    "storageBucket": "chathack-db0fb.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def push_msg(botname, msg, intent_name, intent_precision):
    db.child(botname).update({
        'text': msg,
        'intent': {
            'text': intent_name,
            'precision': intent_precision
        }
    })

