import os

from django.http import JsonResponse
from django.shortcuts import render
import rapidjson
from django.views.decorators.csrf import csrf_exempt

cur_dir = os.path.dirname(__file__)


def tts_prompt_sound(question_body: str) -> str:
    """
    Функция заменяет пропущенное слово-загадку на звук для последующей передачи в tts ответа
    """
    if "<...>" in question_body:
        # question_body = question_body.replace("<...>", "<speaker audio='alice-sounds-human-cough-1.opus'>")
        question_body = question_body.replace("<...>", '<speaker audio="dialogs-upload/6e7b768c-62e7-4abd-81f2-b9c1ae10bd0c/fc4e12e6-33dc-463e-9444-d000bc71085d.opus">')
    return question_body

@csrf_exempt
def anchorlistenit(event):
    event_dict: dict = rapidjson.loads(event.body)
    command: str = event_dict['request']['command']

    sentences_list = []
    if event_dict['session']['new']:

        with open(os.path.join(cur_dir, 'post_processing/sentences_for_check.txt'), 'r', encoding='utf-8') as fp:
            for line in fp.readlines():
                sentences_list.append(line.strip())

        response: dict = {
            'text': f'Привет! Послушай, как я буду произносить фразы. Скажи "Хорошо", если всё хорошо. \n'
                    f'Поехали: \n '
                    f'{sentences_list[0]}',
            'buttons': [
                {'title': 'Дальше', 'hide': 'true'},
                {'title': 'хорошо', 'hide': 'true'}
            ],
            'tts': f'Привет! Послушай, как я буду произносить фразы. Скажи "Хорошо", если всё хорошо. \n'
                   f'Поехали: \n'
                   f'{tts_prompt_sound(sentences_list[0])}',
            'end_session': 'false'
        }

    else:
        with open(os.path.join(cur_dir, 'post_processing/sentences_for_check.txt'), 'r', encoding='utf-8') as fp:
            for line in fp.readlines():
                sentences_list.append(line.strip())
        if command == 'хорошо':
            good_sentence = sentences_list.pop(0)

            with open(os.path.join(cur_dir, 'post_processing/sentences_after_check.txt'), 'a', encoding='utf-8') as fp:
                fp.write(f"{good_sentence}\n")


            with open(os.path.join(cur_dir, 'post_processing/sentences_for_check.txt'), 'w', encoding='utf-8') as fp:
                for sentence in sentences_list:
                    fp.write(f"{sentence}\n")

        if sentences_list:
            response: dict = {
                'text': f'{sentences_list[0]}',
                'buttons': [
                    {'title': 'Дальше', 'hide': 'true'},
                    {'title': 'хорошо', 'hide': 'true'}
                ],
                'tts': f' Дальше: \n'
                       f'{tts_prompt_sound(sentences_list[0])}',
                'end_session': 'false'
            }
        else:
            response: dict = {
                'text': 'Больше предложений нет',
                'tts': 'Больше предложений нет',
                'end_session': 'true'
            }

    resp_data = {
        'version': event_dict['version'],
        'session': event_dict['session'],
        'response': response,
        'session_state': {},
    }
    sentences_list = None

    return JsonResponse(resp_data)
