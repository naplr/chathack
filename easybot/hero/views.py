from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed
import requests
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
from django.views.generic.edit import CreateView
from .models import *
import csv
import io
from django.core import serializers
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from libs.chatai.chatai import ChatAi
from libs.fbclient.client import FbClient

BOTNAME = '1584bot'
chatai = ChatAi('mock', BOTNAME)
# TODO: Add access token
fbclient = FbClient()


def bot_list(request):
    return render(request, 'hero/bot_list.html', {'bot_list': Bot.objects.all()})


def bot_add(request):
    if request.method == 'POST':
        form = request.POST
        bot = Bot.objects.create(name=form['name'], api_key=form['apikey'])
        return HttpResponseRedirect('/admin/main')
    return render(request, 'hero/bot_add.html')


def setup(request, bot_pk):
    if request.method == 'POST':
        # file = request.FILES['file']
        file = io.StringIO(request.FILES['file'].read().decode('utf-8'))
        print(file)
        question_csv_reader = csv.DictReader(file)

        for row in question_csv_reader:

            response = Response.objects.create(text=row['response'], type=row['responsetype'])
            intent = Intent.objects.create(text=row['intent'], response=response, bot=Bot.objects.get(pk=bot_pk))

            for num in range(1, 4):
                entity_text = row['e' + str(num)]
                entity_response_text = row['e' + str(num) + 'r']
                entity_response_type = row['e' + str(num) + 't']
                if '' not in [entity_text, entity_response_text, entity_response_type]:
                    entity_response = Response.objects.create(text=entity_response_text, type=entity_response_type)
                    entity_obj = Entity.objects.create(text=entity_text, response=entity_response)
                    intent.entity.add(entity_obj)
                    intent.save()

    intent = Intent.objects.filter(bot__pk=bot_pk).prefetch_related('entity').prefetch_related('response')
    return render(request, 'hero/setup.html', {'intent_list': intent, 'bot': Bot.objects.get(pk=bot_pk)})


def setup_edit_intent(request, bot_pk, pk):
    # TODO
    intent = Intent.objects.filter(pk=pk).prefetch_related('entity').prefetch_related('response')
    intent = intent[0]
    entity_list = intent.entity.all()

    if request.method == 'POST':
        form = request.POST

        response = Response.objects.create(text=form['response'], type=form['response_type'])
        intent = Intent.objects.create(text=form['intent'], response=response)

        for num in range(1, 6):
            entity_text = form['e' + str(num)]
            entity_response_text = form['e' + str(num) + 'r']
            entity_response_type = form['e' + str(num) + 't']
            print(entity_response_type)
            if '' not in [entity_text, entity_response_text, entity_response_type]:
                entity_response = Response.objects.create(text=entity_response_text, type=entity_response_type)
                entity_obj = Entity.objects.create(text=entity_text, response=entity_response)
                intent.entity.add(entity_obj)
                intent.save()

        return HttpResponseRedirect('/admin/setup')
    else:
        return render(request, 'hero/intent_add.html', {'intent': intent, 'entity_list': entity_list})


def setup_add_intent(request, bot_pk):
    if request.method == 'POST':
        form = request.POST

        response = Response.objects.create(text=form['response'], type=form['response_type'])
        intent = Intent.objects.create(text=form['intent'], response=response, bot=Bot.objects.get(pk=bot_pk))

        for num in range(1, 4):
            entity_text = form['e' + str(num)]
            entity_response_text = form['e' + str(num) + 'r']
            entity_response_type = form['e' + str(num) + 't']
            print(entity_response_type)
            if '' not in [entity_text, entity_response_text, entity_response_type]:
                entity_response = Response.objects.create(text=entity_response_text, type=entity_response_type)
                entity_obj = Entity.objects.create(text=entity_text, response=entity_response)
                intent.entity.add(entity_obj)
                intent.save()

        return HttpResponseRedirect('/admin/bot/{}/'.format(bot_pk))
    else:
        return render(request, 'hero/intent_add.html', {'bot': Bot.objects.get(pk=bot_pk)})


@csrf_exempt
def accept_intent(request):
    # IN: intent name, bot ID
    # OUT: intent's entity

    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        print(data) 
        intent_name = data['intent_name']
        msg = data['msg']

        intent = Intent.objects.get(text=intent_name)
        entities = list(Entity.objects.filter(intent=intent).values('text'))
        print(entities)
        resp = {}
        for e in entities:
            x = chatai.get_entity(msg, e['text'])
            text = x[0] if x  else ''
            resp[e['text']] = text

        return JsonResponse(resp, safe=False)

    else:  # test. Dont' use it!
        print("Shouldn't be here")


@csrf_exempt
def reject_intent(request):
    '''
    IN: intent name, bot ID
    {
        msg: <msg>,
        intentName: <intent_name>,
        threadId: <thread_id>
    }
    # OUT: all intent belonging to BOT
    {
        intents: [
            <intent_name>,
            <intent_name>,
        ]
    }
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        print(data)
        msg = data['msg']
        intent_name = data['intent_name']
        threadid = data['threadId']
        bot_name = BOTNAME
        bot = Bot.objects.get(name=bot_name)

        intents = Intent.objects.filter(bot=bot).all()
        intents_resp = {}
        for i in intents:
            intents_resp[i.text] = i.text
        resp = { 
            'msg': msg,
            'intents': intents_resp 
        }
        
        return JsonResponse(resp, safe=False)


@csrf_exempt
def continue_response(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        threadid = data['threadId']
        msg = data['msg']

        thread = Thread.objects.get(id=threadid)
        rid = thread.customer_rid

        fbclient.send_message(rid, msg)

        data = {
            'threadId': threadid,
            'response': msg,
        }
        return JsonResponse(data)
    else:  
        return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def finish_conversation(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        threadid = data['threadId']

        try:
            thread = Thread.objects.get(id=threadid)
            thread.delete()
        except Thread.DoesNotExist:
            print("Thread {} was already deleted!".format(threadid))

        return HttpResponse(status=200)
    else:  
        return HttpResponseNotAllowed(['POST'])


@csrf_exempt
### NOT DONE ###
def add_new_intent(request):
    '''
    We currently cannot add new intent that requires entities.
    IN: {
        threadId: 'threadid',
        msg: "hello people",
        intentName: "ask_for_opening_hours",
        response: "we open from 8 hours"
    }
    OUT: {
        threadId: 'threadId',
        response: "we open from 8 hours"
    } 
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        threadid = data['threadId']
        msg = data['msg']
        new_intent_name = data['intentName']
        response = data['response']
            
        thread = Thread.objects.get(id=threadid)
        thread_entities = json.load(thread.entities)

        # Create intent.
        Intent.objects.create(
            text=new_intent_name, 
            bot=BOTNAME, 
            response=response)
        chatai.create_intent(new_intent_name, [msg])

        data = {
            'threadId': threadid,
            'response': response,
        }
        
        return JsonResponse(data)
    else:  
        return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def accept_entities(request):
    '''
    IN: {
        threadId: 'threadid',
        msg: "hello people",
        entities: {
            location: "siamsquare",
            time: "",
        }
    }
    OUT: {
        threadId: 'threadId',
        response: "Please tell us your location!"
        entity_name: "location"
    } 

    or if we have all entities
    {
        threadId: 'threadId',
        response: 'Thanks for reporting. We will contact you back soon'
    }
    '''
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        print(data)
        threadid = data['threadId']
        msg = data['msg']
        entities = data['entities']
            
        thread = Thread.objects.get(id=threadid)
        if len(entities) == 1:
            # There will be no empty value here
            thread_entities = json.load(thread.entities)
            entity_name = entities.keys()[0]
            thread_entities[entity_name] = entities[entity_name]
        else:
            # We assume that there will be all entities here
            # This should be only the case after accept intent only
            # Update thread with all entities (not found entities will be blank)
            thread_entities = entities
        
        thread.entities = json.dumps(thread_entities)
        thread.save()

        print(thread_entities)

        missing_entities = [k for k in thread_entities if not thread_entities[k]]
        # Create response to ask for an entity
        if len(missing_entities) > 0:
            entity = Entity.objects.get(text=missing_entities[0])
            response = entity.response
            data = {
                'threadId': threadid,
                'response': response.text,
                'entity': entity.text
            }
        else:
            # We have all required entities
            # Do action!
            response = thread.intent.response.text
            data = {
                'threadId': threadid,
                'response': response
            }

            thread.delete()
        
        return JsonResponse(data)
    else:  
        return HttpResponseNotAllowed(['POST'])


def chat_test(request):
    return render(request, 'hero/chat_test.html')


def training(request, bot_pk):
    bot = Bot.objects.get(pk=bot_pk)

    return render(request, 'hero/training.html', {'bot': bot})
