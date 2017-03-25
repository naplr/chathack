from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
from libs.fbclient.client import FbClient
from libs.chatai.chatai import ChatAi
from libs.fireclient import client as fireclient
from hero.models import *

ACCESS_TOKEN = 'EAAD8zs76JyMBAMbMsKZCFum0z6gqGWnz8wmoqcfA2PFP47DvmRqKbtLUqBdhfLapGpvLF3EmDMTlsZBTBNAUxZAHwlh7Gyr7ZAsc9TG0k2laFHc0uY0sneookV59sZAJpKv0NL1RRPZAUqrD05Vy2xjseisrAk81F3mGSZBZCu9BwgZDZD'
BOTNAME = '1584bot'

def _handle_message_from_fb(event):
    client = FbClient(ACCESS_TOKEN)
    chatai = ChatAi('mock', BOTNAME)
    rid,  msg = client.extract_message_and_recipientid(event)

    # first message
    new_thread = True
    if new_thread:
        intent_name, precision = chatai.get_intent(msg)

        intent = Intent.objects.get(text=intent_name)
        thread = Thread.objects.create(customer_rid=rid, intent=intent)
        fireclient.push_msg(BOTNAME, thread.id, msg, intent_name, precision)

    # subsequence msg
    else:
        pass



@csrf_exempt
def webhook(request):
    try:
        # 'GET' request is for setting up webhook with challenge.
        if request.method == 'GET':
            if (request.GET.get('hub.mode') == 'subscribe' and request.GET.get('hub.verify_token') == '7771717'):
                return HttpResponse(request.GET.get('hub.challenge'))
            return HttpResponseForbidden()

        elif request.method == 'POST':
            data = json.loads(request.body.decode('UTF-8'))
            print('data: ' + str(data))
            if data['object'] == 'page':
                for entry in data['entry']:
                    pageid = entry['id']
                    time_of_event = entry['time']
                    for event in entry['messaging']:
                        if 'message' in event:
                            _handle_message_from_fb(event)
                        else:
                            print("Webhook received unknown event: " + event)

            return HttpResponse()
    except:
        traceback.print_exc()
        return HttpResponse()
