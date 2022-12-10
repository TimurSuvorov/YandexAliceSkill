import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from mainapp.processing.handlers.hi_replies import hi_replies
from mainapp.processing.handlers.bye_replies import bye_replies
from mainapp.processing.handlers.main_checkanswer import checkanswer


@csrf_exempt
def anchorhandler(event):
    event: dict = json.load(event)
    if event['session']['new']:
        response_dict = {"response": hi_replies(),
                         "sessionstate": {}
                         }
    elif event['session']['message_id'] == 1 \
            and event['request']['command'] in ["нет", "не хочу", "закончим", "не начнём", "хватит"]:
        response_dict = {"response": bye_replies(),
                         "sessionstate": {}
                         }
    else:
        command = event['request']['command']
        session_state = event['state']['session']
        response_dict = checkanswer(command, session_state)

    resp_data = {
        'version': event['version'],
        'session': event['session'],
        'response': response_dict["response"],
        'session_state': response_dict["sessionstate"]
    }
    return JsonResponse(resp_data)


