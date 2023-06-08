import os
import random
import re
from collections import defaultdict

import rapidjson

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tellmeapp.post_processing.c_collect_allwords import allwords

cur_dir = os.path.dirname(__file__)


def remove_tts_symbols(instance: str) -> str:
    """
    Функция удаляет все tts символы для последующего отображения в text ответа
    """
    if "+" in instance or " - " in instance:
        instance: str = instance.replace(" - ", "").replace("+", "")
    if "sil" in instance:
        instance: str = re.sub(r"(sil <\[\d{1,3}\]>)", "", instance)
    return instance


@csrf_exempt
def anchortellme(event):
    event_dict: dict = rapidjson.loads(event.body)  # Сериализация POST-запроса (от пользователя)
    command: str = event_dict['request']['command']  # Преобразованная сообщение-команда (от пользователя)
    user_id = event_dict['session']['user']['user_id']  # Идентификатор пользователя (уникальный для уч.записи)
    session_state = event_dict['state']['session']  # Блок параметров "состояния"

    if event_dict['session']['new']:
        word = random.choice(allwords)
        response: dict = {
            'text': f'Привет! Потренируй меня! Я говорю слово, а ты повторяй \nПоехали: {remove_tts_symbols(word)}',
            'buttons': [
            ],
            'tts': f'Я говорю слово, а ты повторяй \nПоехали: {word}',
            'end_session': 'false'
        }

        resp_data = {
            'version': event_dict['version'],
            'session': event_dict['session'],
            'response': response,
            'session_state': {"word": word},
        }
    else:
        source_word = session_state["word"]

        with open(os.path.join(cur_dir, 'post_processing/db_results.json'), 'r') as fp:
            data_dict = rapidjson.load(fp)
        data_default_dict = defaultdict(list, data_dict)
        data_default_dict[source_word].append(command)
        data_default_dict[source_word] = list(set(data_default_dict[source_word]))
        data_res_dict = dict(data_default_dict)

        with open(os.path.join(cur_dir, 'post_processing/db_results.json'), 'w', encoding='utf-8') as fp:
            fp.write(rapidjson.dumps(data_res_dict, indent=4, ensure_ascii=False))

        # Новое слово
        word = random.choice(allwords)
        response: dict = {
            'text': remove_tts_symbols(word),
            'buttons': [
            ],
            'tts': word,
            'end_session': 'false'
        }

        resp_data = {
            'version': event_dict['version'],
            'session': event_dict['session'],
            'response': response,
            'session_state': {"word": word},
        }

    return JsonResponse(resp_data)

