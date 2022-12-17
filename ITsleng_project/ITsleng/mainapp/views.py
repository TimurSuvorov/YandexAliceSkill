from pprint import pprint

import rapidjson
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from mainapp.processing.handlers.fucking_replies import fucking_replies
from mainapp.processing.handlers.many_words import many_words
from mainapp.processing.handlers.question_on_question_replies import question_on_question_replies
from mainapp.processing.handlers.service_replies import hi_replies, bye_replies, rules_replies, about_replies
from mainapp.processing.handlers.help_dontknow_replies import dontknow
from mainapp.processing.handlers.main_checkanswer import checkanswer
from mainapp.processing.handlers.repeat_replies import repeat_replies
from mainapp.processing.handlers.yes_no_cont_replies import yes_no_cont_replies

exit_light = ["нет", "не хочу", "закончим", "не начнём", "хватит", "выйди", "выход", "стоп", "все пока", "всё пока", "я ухожу"]
exit_hard = ["закончим", "закончить", "хватит", "выйди", "выход$", "стоп$", "не хочу", "выйти", "я ухожу", "мне надоело", "все пока", "всё пока"]
rules = ["правила", "помощь"]
about = ["что ты умеешь", "что умеешь", "умеешь", "знаешь$", "что ты можешь"]
dont_know = ["не знаю", "дальше", "сдаюсь", "ответ", "новый вопрос", "откуда мне знать", "следующий вопрос"]
repeat = ["повтор", "не понял", "ещё раз", "не расслышал"]



@csrf_exempt
def anchorhandler(event):
    event: dict = rapidjson.load(event)
    command: str = event['request']['command']
    original_utterance: str = event['request']['original_utterance']
    sessionuser_id = event['session']['user']['user_id']
    session_state = event['state']['session']
    nlu_tokens = event['request']["nlu"]["tokens"]
    print(original_utterance)
    # pprint(event)

    # Обработка нового входа
    if event['session']['new']:
        print('1#')
        response_dict = hi_replies()
    elif not session_state.get("question_dict") and re.search("|".join(exit_light), command):
        print('2#')
        response_dict = bye_replies(session_state)
    # Обработка сервисных ответов "Правила", "Что умеешь?"
    elif re.search("|".join(rules), command):
        print('3#')
        response_dict = rules_replies(session_state)
    elif re.search("|".join(about), command):
        print('4#')
        response_dict = about_replies(session_state)
    elif "*" in nlu_tokens:
        print('6#')
        response_dict = fucking_replies(command, session_state)
    # Обработка сообщений "вопрос на вопрос"
    elif re.search('\?$', original_utterance):
        print('7#')
        response_dict = question_on_question_replies(command, session_state)
    # Обработка сообщений из списка dont_know и если сообщений до не было!
    elif not session_state.get("question_dict") and re.search("|".join(dont_know), command):
         print('8#')
         response_dict = dontknow(command, session_state)
    # Обработка незнания из списка dont_know и если сообщение до этого не было сервисным
    elif re.search("|".join(dont_know), command) and not session_state.get("yesno_type"):
        print('9#')
        response_dict = dontknow(command, session_state)
    # Обработка запроса повторения
    elif re.search("|".join(repeat), command):
        print('10#')
        response_dict = repeat_replies(session_state)
    # Обработка запрос с мнимыми ответами Да/Нет
    elif len(original_utterance.split()) >= 4:
        print('11#')
        response_dict = many_words(command, session_state)
    elif session_state.get("yesno_type"):
        print('12#')
        response_dict = yes_no_cont_replies(command, session_state)
    # Обработка требования выхода
    elif re.search("|".join(exit_hard), command):
        print('13#')
        response_dict = bye_replies(session_state)
    else:
        # Здесь должен остаться только вариант с вопросом внутри - его обрабатываем дальше
        print('14#')
        response_dict = checkanswer(command, session_state)


    resp_data = {
        'version': event['version'],
        'session': event['session'],
        'response': response_dict["response"],
        'session_state': response_dict["session_state"],
        'analytics': response_dict.get("analytics", {})
    }
    return JsonResponse(resp_data)


