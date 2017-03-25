class FbClient:
    def __init__(self, access_token):
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


    def send_message(self, recipientid, msg_text):
        msg_data = {
            'recipient': { 'id': recipientid },
            'message': { 'text': msg_text }
        }

        self._send_api_request(msg_data)


    def extract_message_and_recipientid(self, event):
        senderid = event['sender']['id']
        recipientid = event['recipient']['id']
        time_of_message = event['timestamp']
        message = event['message']

        messageid = message['mid']

        return (recipientid, message['text'])
