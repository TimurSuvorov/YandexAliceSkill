import rapidjson
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from mainapp.processing.handlers.service_replies import hi_replies, bye_replies, rules_replies, about_replies
from mainapp.processing.handlers.help_dontknow_replies import dontknow
from mainapp.processing.handlers.main_checkanswer import checkanswer
from mainapp.processing.handlers.repeat_replies import repeat_replies


exit_light = ["нет", "не хочу", "закончим", "не начнём", "хватит", "выйди", "выход", "стоп"]
exit_hard = ["закончим", "хватит", "выйди", "выход$", "стоп$", "не хочу", "выйти"]
rules = ["правила", "помощь"]
about = ["что ты умеешь", "что умеешь", "умеешь", "знаешь?"]
dont_know = ["не знаю", "дальше", "сдаюсь", "ответ"]
repeat = ["повтор", "не понял", "ещё раз", "не расслышал"]

yes_ = ["да$", "давай", "хорошо"]
no_ = ["нет", "не хочу"]



@csrf_exempt
def anchorhandler(event):
    event: dict = rapidjson.load(event)
    command = event['request']['command']
    session_state = event['state']['session']

    # Обработка нового входа
    if event['session']['new']:
        response_dict = hi_replies()
    elif not session_state.get("question_dict") and re.search("|".join(exit_light), command):
        response_dict = bye_replies(session_state)

    # Обработка запроса повторения
    elif re.search("|".join(repeat), command):
        response_dict = repeat_replies(session_state)
    # Обработка незнания
    elif re.search("|".join(dont_know), command):
        response_dict = dontknow(session_state)
    # Обработка сервисных ответов "Правила", "Что умеешь?"
    elif re.search("|".join(rules), command):
        response_dict = rules_replies(session_state)
    elif re.search("|".join(about), command):
        response_dict = about_replies(session_state)
    # Обработка требования выхода
    elif re.search("|".join(exit_hard), command):
        response_dict = bye_replies(session_state)
    else:
        response_dict = checkanswer(command, session_state)


    resp_data = {
        'version': event['version'],
        'session': event['session'],
        'response': response_dict["response"],
        'session_state': response_dict["session_state"]
    }
    return JsonResponse(resp_data)


