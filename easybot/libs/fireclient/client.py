import pyrebase
import sys
config = {
    "apiKey": "AIzaSyBbLf8k4NKQVXfjMg--POKkiQjHi2yuTxc",
    "authDomain": "chathack-db0fb.firebaseapp.com",
    "databaseURL": "https://chathack-db0fb.firebaseio.com",
    "storageBucket": "chathack-db0fb.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def push_msg_intent(botname, threadid, msg, intent_name, intent_precision):
    print("Send msg: {}, intent: {}".format(msg, intent_name))
    db.child(botname).update({
        'threadId': str(threadid),
        'text': msg,
        'entity': None,
        'intent': {
            'text': intent_name,
            'precision': intent_precision
        }
    })


def push_msg_entity(botname, threadid, msg, entity_name, entity_value, precision):
    print("Send msg: {}, entity: {} = {}".format(msg, entity_name, entity_value))
    db.child(botname).update({
        'threadId': str(threadid),
        'text': msg,
        'entity': {
            'name': entity_name,
            'value': entity_value,
            'precision': precision
        }
    })

if __name__ == '__main__':
    push_msg(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])