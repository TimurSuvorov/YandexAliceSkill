import json
import random
import os

from mainapp.processing.extract_json import get_db_sentences, get_db_sounds


def hi_replies() -> dict:
    # Случайный выбор фразы приветствия
    sentences = get_db_sentences()
    hi_text = sentences["HIsentence"]

    # Выбираем звуки
    sounds = get_db_sounds()
    startsound = random.choice(sounds["START"])

    response: dict = {
            'text': hi_text,
            'buttons': [
                {'title': 'Правила', 'hide': 'true'},
                {'title': 'Что ты умеешь?', 'hide': 'true'}
            ],
            'tts': f'{startsound}{hi_text}',
            'end_session': 'false'
    }
    sessionstate = {'service': 11}
    return {
        "response": response,
        "session_state": sessionstate
    }


def bye_replies(session_state):
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
        "session_state": session_state
    }


def rules_replies(session_state) -> dict:

    sentences = get_db_sentences()
    rules_text = sentences["RULES"]["text"]
    rules_tts = sentences["RULES"]["tts"]

    response: dict = {
            'text': rules_text,
            'buttons': [
                {'title': 'Что ты умеешь?', 'hide': 'true'}
            ],
            'tts': rules_tts,
            'end_session': 'false'
    }

    sessionstate = {
        "question_dict": {
            'sentence': rules_text,
            'answers': [],
            'variants': [],
            'category': []
        },
        "yesno_type": 10,
        "service": 11
    }

    return {
        "response": response,
        "session_state": sessionstate
    }


def about_replies(session_state) -> dict:
    sentences = get_db_sentences()
    about_text = sentences["ABOUT"]

    response: dict = {
            'text': about_text,
            'buttons': [
                {'title': 'Правила', 'hide': 'true'}
            ],
            'tts': about_text,
            'end_session': 'false'
    }

    sessionstate = {
        "question_dict": {
            'sentence': about_text,
            'answers': [],
            'variants': [],
            'category': []
        },
        "yesno_type": 10,
        "service": 11
    }

    return {
        "response": response,
        "session_state": sessionstate
    }