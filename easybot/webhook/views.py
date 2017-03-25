from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
import json
import traceback


def callSendAPI(messageData):
    response = requests.post('https://graph.facebook.com/v2.6/me/messages',
                             params={
                                 'access_token': 'EAAD8zs76JyMBAMbMsKZCFum0z6gqGWnz8wmoqcfA2PFP47DvmRqKbtLUqBdhfLapGpvLF3EmDMTlsZBTBNAUxZAHwlh7Gyr7ZAsc9TG0k2laFHc0uY0sneookV59sZAJpKv0NL1RRPZAUqrD05Vy2xjseisrAk81F3mGSZBZCu9BwgZDZD'},
                             json=messageData
                             )
    print('callSendAPI response: ' + str(response.content))


def sendTextMessage(recipientId, messageText):
    messageData = {
        'recipient': {
            'id': recipientId
        },
        'message': {
            'text': messageText
        }
    }
    callSendAPI(messageData)


def receivedMessage(event):
    senderID = event['sender']['id']
    recipientID = event['recipient']['id']
    timeOfMessage = event['timestamp']
    message = event['message']

    messageId = message['mid']

    if ('text' in message):
        print("Received message for user {} and page {} at {} with message: {}".format(
            senderID, recipientID, timeOfMessage, message['text']))
        sendTextMessage(senderID, message['text'])

    else:
        print(str(message))
        sendTextMessage(senderID, "Message with attachment received")


def manifest(request):
    return JsonResponse({"gcm_sender_id": "103953800507"})


def fms(request):
    resp = render(request, 'hero/fms.js')
    resp['Content-Type'] = 'application/javascript'
    return resp



@csrf_exempt
def webhook(request):
    try:
        print(request)
        if request.method == "GET":
            # print(request.GET)
            if (request.GET.get('hub.mode') == 'subscribe' and request.GET.get('hub.verify_token') == '7771717'):
                return HttpResponse(request.GET.get('hub.challenge'))
            return HttpResponseForbidden()

        elif request.method == 'POST':
            data = json.loads(request.body.decode('UTF-8'))
            print('data: ' + str(data))
            if data['object'] == 'page':
                for entry in data['entry']:
                    pageID = entry['id']
                    timeOfEvent = entry['time']
                    for event in entry['messaging']:
                        if 'message' in event:
                            receivedMessage(event)
                        else:
                            print("Webhook received unknown event: " + event)

            return HttpResponse()
    except:
        traceback.print_exc()
        return HttpResponse()
