import json
import random
import os

from mainapp.processing.extract_json import get_db_sentences, get_db_sounds
from mainapp.processing.handle_sessionfile import create_session_file, remove_session_file
from mainapp.processing.handle_userprofile import check_old_user


def hi_replies(user_id, session_id) -> dict:
    # Создание файла с вопросами для сессии
    create_session_file(session_id)
    # Фраза приветствия
    sentences = get_db_sentences()
    if check_old_user(user_id, session_id):
        hi_text = sentences["HIsentence_olduser"]["text"]
        hi_tts = sentences["HIsentence_olduser"]["tts"]
    else:
        hi_text = sentences["HIsentence_newuser"]["text"]
        hi_tts = sentences["HIsentence_newuser"]["tts"]

    # Выбираем звуки
    sounds = get_db_sounds()
    startsound = random.choice(sounds["START"])

    response: dict = {
            'text': hi_text.replace(" - ", "").replace("+", ""),
            'buttons': [
                {'title': 'Правила', 'hide': 'true'},
                {'title': 'Что ты умеешь?', 'hide': 'true'}
            ],
            'tts': f'{startsound}{hi_tts}',
            'end_session': 'false'
    }
    sessionstate = {'service': 11, 'yesno_type': 10}
    return {
        "response": response,
        "analytics": {
            "events": [
                {
                    "name": "Запуск навыка",
                },
            ]
        },
        "session_state": sessionstate,
    }


def bye_replies(session_state, session_id):

    sentences = get_db_sentences()
    bye_text = random.choice(sentences["BYEsentence"])

    # Выбираем звуки
    sounds = get_db_sounds()
    byesound = random.choice(sounds["BYE"])

    response: dict = {
            'text': bye_text,
            'tts': f'{bye_text} {byesound}',
            'end_session': 'True'
    }

    return {
        "response": response,
        "analytics": {
            "events": [
                {
                    "name": "Выход из навыка",
                },
            ]
        },
        "session_state": session_state
    }


def rules_replies(session_state: dict) -> dict:
    sentences = get_db_sentences()
    rules_text = sentences["RULES"]["text"]
    rules_tts = sentences["RULES"]["tts"]
    # Если функция вызвана во время вопроса, когда присутствует session_state["question_dict"]["answers"]
    if session_state.get('question_dict', {}).get('answers'):
        rules_text += 'Продолжим?'
        rules_tts += 'Прод+олжим?'
    else:
        rules_text += 'Ну что, начинаем?'
        rules_tts += 'Ну чт+о, начин+аем?'

    response: dict = {
            'text': rules_text,
            'buttons': [
                {'title': 'Что ты умеешь?', 'hide': 'true'}
            ],
            'tts': rules_tts,
            'end_session': 'false'
    }

    # Состояние с предыдущем ответом передаем прозрачно, но добавляем сервисный флаг
    sessionstate = session_state
    sessionstate["yesno_type"] = 10
    sessionstate["service"] = 11

    return {
        "response": response,
        "analytics": {
            "events": [
                {
                    "name": "Запрос 'Правила'",
                },
            ]
        },
        "session_state": sessionstate
    }


def about_replies(session_state) -> dict:
    sentences = get_db_sentences()
    about_text = sentences["ABOUT"]

    # Если функция вызвана во время вопроса, когда присутствует session_state["question_dict"]["answers"]
    if session_state.get('question_dict', {}).get('answers'):
        about_text += 'Прод+олжим?'
    else:
        about_text += 'Начин+аем?'

    response: dict = {
            'text': about_text.replace(" - ", "").replace("+", ""),
            'buttons': [
                {'title': 'Правила', 'hide': 'true'}
            ],
            'tts': about_text,
            'end_session': 'false'
    }

    # Состояние с предыдущем ответом передаем прозрачно, но добавляем сервисный флаг
    sessionstate = session_state
    sessionstate["yesno_type"] = 10
    sessionstate["service"] = 11

    return {
        "response": response,
        "analytics": {
            "events": [
                {
                    "name": "Запрос 'Что умеешь?'",
                },
            ]
        },
        "session_state": sessionstate
    }