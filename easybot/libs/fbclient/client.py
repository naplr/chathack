import requests

ACCESS_TOKEN = 'EAAD8zs76JyMBAMbMsKZCFum0z6gqGWnz8wmoqcfA2PFP47DvmRqKbtLUqBdhfLapGpvLF3EmDMTlsZBTBNAUxZAHwlh7Gyr7ZAsc9TG0k2laFHc0uY0sneookV59sZAJpKv0NL1RRPZAUqrD05Vy2xjseisrAk81F3mGSZBZCu9BwgZDZD'

class FbClient:
    def __init__(self, access_token=ACCESS_TOKEN):
        self.token = access_token

    def _send_api_request(self, message_data):
        response = requests.post(
            'https://graph.facebook.com/v2.6/me/messages',
            params={
                'access_token': self.token
            },
            json=message_data
        )

        print('callSendAPI response: ' + str(response.content))


    def send_message(self, rid, msg_text):
        msg_data = {
            'recipient': { 'id': rid },
            'message': { 'text': msg_text }
        }

        print("sending to rid: {}".format(rid))

        self._send_api_request(msg_data)


    def extract_message_and_recipientid(self, event):
        senderid = event['sender']['id']
        rid = event['recipient']['id']
        time_of_message = event['timestamp']
        message = event['message']

        messageid = message['mid']

        return (senderid, message['text'])
