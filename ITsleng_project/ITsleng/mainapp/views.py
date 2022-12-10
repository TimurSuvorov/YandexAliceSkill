import json
import random
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .handlers.hi_replies import hi_replies
from .handlers.bye_replies import bye_replies
from .handlers.next_question import next_question
from .handlers.correctAnswer import correctanswer
from .handlers.incorrectAnswer import incorrectanswer
from .handlers.generate_question import generate_question


question_tuple = None

@csrf_exempt
def anchorhandler(event):
    event = json.load(event)
    global question_tuple
    if event['session']['new']:
        response = hi_replies()
        question = None
    elif event['session']['message_id'] == 1 \
            and event['request']['command'] in ["нет", "не хочу", "закончим", "не начнём", "хватит"]:
        response = bye_replies()
    else:
        response, question_tuple = checkanswer(event['request']['command'], question_tuple)

    resp_data = {
        'version': event['version'],
        'session': event['session'],
        'response': response,
    }
    return JsonResponse(resp_data)


def checkanswer(command, question_attempt):
    if not question_attempt:
        question_attempt = generate_question()
        response = next_question(question_attempt)
        return response, question_attempt

    if iscorrectanswer(command, question_attempt):
        question_attempt = generate_question()
        response = correctanswer(question_attempt)
        return response, question_attempt
    else:
        response, question_attempt_minus = incorrectanswer(question_attempt)
        return response, question_attempt_minus


def iscorrectanswer(command, question_tuple):
    matching = re.search("|".join(question_tuple[0]['answers']), command)
    if matching:
        return True
    return False


