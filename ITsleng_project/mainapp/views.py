import datetime
import logging
from pprint import pprint

import rapidjson
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .processing.handle_userprofile import check_and_create_profile, update_time_end, check_and_add_new_session
from .processing.handlers.fucking_replies import fucking_replies
from .processing.handlers.many_words import many_words
from .processing.handlers.my_rating_replies import my_rating
from .processing.handlers.question_on_question_replies import question_on_question_replies
from .processing.handlers.service_replies import hi_replies, bye_replies, rules_replies, about_replies
from .processing.handlers.help_dontknow_replies import dontknow
from .processing.handlers.main_checkanswer import checkanswer
from .processing.handlers.repeat_replies import repeat_replies
from .processing.handlers.yes_no_cont_replies import yes_no_cont_replies

exit_hard = ["не хочу играть", "все надоело", "закончим", "закончить", "хватит", "выйди", "выход$", "стоп$", "не хочу",
             "выйти", "я ухожу", "мне надоело", "все пока", "всё пока", "наигралась", "^пока$", "стоп", "выйду$",
             r"бай\b", "гудбай", "goodbye", "покинуть игру", "надоел", "пока пока"]
rules = ["правила", "помощь", "помоги", "help"]
about = ["что ты умеешь", "что умеешь", "умеешь", "знаешь$", "что ты можешь", "еще можешь"]
dont_know = ["не знаю", r"^дальше$", "сдаюсь", r"ответ$", "новый вопрос", "откуда мне знать", "следующий вопрос",
             "следующий$", r"пропус.*"]
repeat = ["повтор", "не понял", "ещё раз", "не расслышал", "еще раз", "повтори", "не услышал", "что что", "не понимаю"]


@csrf_exempt
def anchorhandler(event):
    event: dict = rapidjson.load(event)  # Сериализация POST-запроса (от пользователя)
    command: str = event['request']['command']  # Преобразованная сообщение-команда (от пользователя)
    original_utterance: str = event['request']['original_utterance']  # Исходное сообщение-команда (от пользователя)
    user_id = event['session']['user']['user_id']  # Идентификатор пользователя (уникальный для уч.записи)
    session_id = event['session']['session_id']  # Идентификатор сессии (сброс при выходе или по тайм-ауту 20 мин.)
    message_id = event['session']['message_id']  # Порядковый номер сообщения за сессию
    session_state = event['state']['session']  # Блок параметров "состояния"
    nlu_tokens = event['request']['nlu']['tokens']  # Массив слов из произнесенной фразы. * - в случае нецензурны
    intents = event['request']['nlu']['intents']  # Извлеченные интенты

    print(f'>>{session_state.get("question_dict", {}).get("sentence", {})}\n<<{original_utterance}')

    # Обработка нового входа
    if event['session']['new']:
        print('1# - новая сессия')
        check_and_create_profile(user_id, session_id)  # Существует ли профайл пользователя; создание, если нет
        check_and_add_new_session(user_id, session_id)  # Существует ли запись сессии в профайле; создание, если нет
        response_dict = hi_replies(user_id, session_id)
    # Обработка сервисных ответов "Правила"
    elif re.search("|".join(rules), command):
        print('3# - правила')
        response_dict = rules_replies(session_state)
    # Обработка сервисных ответов "Что ты умеешь?"
    elif re.search("|".join(about), command):
        print('4# - что ты умеешь')
        response_dict = about_replies(session_state)
    # Запрос рейтинга. Берем из интентов
    elif intents.get('rating_1', {}):
        print('5# - запрос рейтинга')
        response_dict = my_rating(session_state, user_id, session_id)
    # Нецензурная речь в ответе
    elif "*" in nlu_tokens:
        print('6# - нецензурная речь')
        response_dict = fucking_replies(command, session_state)
    # Обработка требования выхода
    elif re.search("|".join(exit_hard), command):
        print('12# - требование выхода')
        response_dict = bye_replies(session_state, session_id)
    # Обработка сообщений "вопрос на вопрос". Берем из интентов
    elif intents.get('question_1', {}):
        print('7# - вопрос на вопрос')
        response_dict = question_on_question_replies(command, session_state)
    # Обработка запроса повторения
    elif re.search("|".join(repeat), command) or intents.get('YANDEX.REPEAT', {}):
        print('8# - запрос повторения')
        response_dict = repeat_replies(session_state)
    # Обработка сообщений из списка dont_know и если сообщений до не было!
    elif re.search("|".join(dont_know), command) and not session_state.get("question_dict"):
        print('9# - не знает без вопроса')
        response_dict = dontknow(command, session_state, user_id, session_id)
    # Обработка сообщений из списка dont_know и если сообщение до этого не было закрытым
    elif re.search("|".join(dont_know), command) and not session_state.get("yesno_type"):
        print('10# - не знает или сдается')
        response_dict = dontknow(command, session_state, user_id, session_id)
    # Обработка запроса с длинными предложениями и вопросы не распознаны как согласия или реджекта(чтоб шли ниже)
    elif len(original_utterance.split()) > 4 and \
            not (intents.get('YANDEX.CONFIRM', {}) or intents.get('YANDEX.REJECT', {})):
        print('11# - слишком большая команда')
        response_dict = many_words(command, session_state)
    # Обработка ответа на закрытый вопрос
    elif session_state.get("yesno_type"):
        print('13# - закрытый вопрос')
        response_dict = yes_no_cont_replies(command, session_state, session_id, intents)
    else:
        # Здесь должен остаться только вариант с вопросом внутри - его обрабатываем дальше
        print('14#')
        response_dict = checkanswer(command, session_state, user_id, session_id, message_id)

    resp_data = {
        'version': event['version'],
        'session': event['session'],
        'response': response_dict["response"],
        'session_state': response_dict["session_state"],
        'analytics': response_dict.get("analytics", {})
    }

    update_time_end(user_id, session_id)  # Score develop

    return JsonResponse(resp_data)
