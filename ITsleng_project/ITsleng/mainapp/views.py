from pprint import pprint

import rapidjson
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from mainapp.processing.handle_userprofile import check_and_create_profile, update_time_end, check_and_add_new_session
from mainapp.processing.handlers.fucking_replies import fucking_replies
from mainapp.processing.handlers.many_words import many_words
from mainapp.processing.handlers.question_on_question_replies import question_on_question_replies
from mainapp.processing.handlers.service_replies import hi_replies, bye_replies, rules_replies, about_replies
from mainapp.processing.handlers.help_dontknow_replies import dontknow
from mainapp.processing.handlers.main_checkanswer import checkanswer
from mainapp.processing.handlers.repeat_replies import repeat_replies
from mainapp.processing.handlers.yes_no_cont_replies import yes_no_cont_replies

exit_light = ["нет", "не хочу", "закончим", "не начнём", "хватит", "выйди", "выход", "стоп", "все пока", "всё пока",
              "я ухожу"]
exit_hard = ["не хочу играть", "все надоело", "закончим", "закончить", "хватит", "выйди", "выход$", "стоп$", "не хочу",
             "выйти", "я ухожу", "мне надоело", "все пока", "всё пока", "наигралась", "^пока$", "стоп"]
rules = ["правила", "помощь", "помоги", "help"]
about = ["что ты умеешь", "что умеешь", "умеешь", "знаешь$", "что ты можешь", "еще можешь"]
dont_know = ["не знаю", "дальше", "сдаюсь", r"ответ$", "новый вопрос", "откуда мне знать", "следующий вопрос"]
repeat = ["повтор", "не понял", "ещё раз", "не расслышал", "еще раз", "повтори", "не услышал"]


@csrf_exempt
def anchorhandler(event):
    event: dict = rapidjson.load(event)
    command: str = event['request']['command']
    original_utterance: str = event['request']['original_utterance']
    user_id = event['session']['user']['user_id']
    session_id = event['session']['session_id']
    session_state = event['state']['session']
    nlu_tokens = event['request']["nlu"]['tokens']
    intents = event['request']['nlu']['intents']
    print(f'>>{session_state.get("question_dict", {}).get("sentence", {})}\n<<{original_utterance}')

    check_and_create_profile(user_id, session_id)  # Score develop
    check_and_add_new_session(user_id, session_id)  # Score develop

    # Обработка нового входа
    if event['session']['new']:
        print('1#')
        response_dict = hi_replies(session_id)
    elif not session_state.get("question_dict") and re.search("|".join(exit_hard), command):
        print('2#')
        response_dict = bye_replies(session_state, session_id)
    # Обработка сервисных ответов "Правила", "Что умеешь?"
    elif re.search("|".join(rules), command):
        print('3#')
        response_dict = rules_replies(session_state)
    elif re.search("|".join(about), command) or intents.get('YANDEX.HELP', {}):
        print('4#')
        response_dict = about_replies(session_state)
    elif "*" in nlu_tokens:
        print('6#')
        response_dict = fucking_replies(command, session_state)
    # Обработка сообщений "вопрос на вопрос"
    elif intents.get('question_1', {}):
        print('7#')
        response_dict = question_on_question_replies(command, session_state)
    # Обработка запроса повторения
    elif re.search("|".join(repeat), command) or intents.get('YANDEX.REPEAT', {}):
        print('8#')
        response_dict = repeat_replies(session_state)
    # Обработка сообщений из списка dont_know и если сообщений до не было!
    elif not session_state.get("question_dict") and re.search("|".join(dont_know), command):
        print('9#')
        response_dict = dontknow(command, session_state, user_id, session_id)
    # Обработка незнания из списка dont_know и если сообщение до этого не было сервисным
    elif re.search("|".join(dont_know), command) and not session_state.get("yesno_type"):
        print('10#')
        response_dict = dontknow(command, session_state, user_id, session_id)
    # Обработка запроса с длинными предложениями и вопросы не распознаны как согласия или реджекта(чтоб шли ниже)
    elif len(original_utterance.split()) > 4 and \
            not (intents.get('YANDEX.CONFIRM', {}) or intents.get('YANDEX.REJECT', {})):
        print('11#')
        response_dict = many_words(command, session_state)
    # Обработка требования выхода
    elif re.search("|".join(exit_hard), command):
        print('12#')
        response_dict = bye_replies(session_state, session_id)
    # Обработка запрос с мнимыми ответами Да/Нет
    elif session_state.get("yesno_type"):
        print('13#')
        response_dict = yes_no_cont_replies(command, session_state, session_id, intents)
    else:
        # Здесь должен остаться только вариант с вопросом внутри - его обрабатываем дальше
        print('14#')
        response_dict = checkanswer(command, session_state, user_id, session_id)

    resp_data = {
        'version': event['version'],
        'session': event['session'],
        'response': response_dict["response"],
        'session_state': response_dict["session_state"],
        'analytics': response_dict.get("analytics", {})
    }

    update_time_end(user_id, session_id) # Score develop

    return JsonResponse(resp_data)
