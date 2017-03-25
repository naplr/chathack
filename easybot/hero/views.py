from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
from django.views.generic.edit import CreateView
from .models import *
import csv
import io
from django.core import serializers


def bot_list(request):
    return render(request, 'hero/bot_list.html', {'bot_list': Bot.objects.all()})


def bot_add(request):
    if request.method == 'POST':
        form = request.POST
        bot = Bot.objects.create(name=form['name'], api_key=form['apikey'])
        return HttpResponseRedirect('/admin/')
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

            for num in range(1, 6):
                entity_text = row['e' + str(num)]
                entity_response_text = row['e' + str(num) + 'r']
                entity_response_type = row['e' + str(num) + 't']
                print(entity_response_type)
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

        return HttpResponseRedirect('/admin/bot/{}/'.format(bot_pk))
    else:
        return render(request, 'hero/intent_add.html', {'bot': Bot.objects.get(pk=bot_pk)})


@csrf_exempt
def accept_intent(request):
    # IN: intentID
    # OUT: intent's entity

    if request.method == 'POST':
        intentID = uuid.UUID(json.loads(request.body.decode("utf-8"))['intentID'])
        intent = Intent.objects.get(pk=intentID)
        entities = Entity.objects.filter(intent=intent)
        qs_json = serializers.serialize('json', entities)
        return JsonResponse(qs_json, safe=False)


@csrf_exempt
def reject_intent(request):
    # IN: intentID
    # OUT: all intent belonging to BOT

    if request.method == 'POST':
        intentID = uuid.UUID(json.loads(request.body.decode("utf-8"))['intentID'])
        bot = Bot.objects.get(intent__pk=intentID)

        intents = Intent.objects.filter(bot=bot)
        qs_json = serializers.serialize('json', intents)
        return JsonResponse(qs_json, safe=False)


def chat(request, bot_pk):
    return HttpResponse()
