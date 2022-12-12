import json
import random
import os

from mainapp.processing.extract_json import get_db_sentences


def hi_replies() -> dict:
    sentences = get_db_sentences()
    # Случайный выбор фразы приветствия
    hi_text = sentences["HIsentence"]

    response: dict = {
            'text': hi_text,
            'buttons': [
                {'title': 'Правила', 'hide': 'true'},
                {'title': 'Что ты умеешь?', 'hide': 'true'}
            ],
            'tts': hi_text,
            'end_session': 'false'
    }
    sessionstate = {'service': 1}
    return {
        "response": response,
        "session_state": sessionstate
    }


def bye_replies(session_state):
    sentences = get_db_sentences()
    bye_text = random.choice(sentences["BYEsentence"])

    response: dict = {
            'text': bye_text,
            'tts': bye_text,
            'end_session': 'True'
    }


    return {
        "response": response,
        "session_state": session_state
    }


def rules_replies(session_state) -> dict:

    sentences = get_db_sentences()
    rules_text = sentences["RULES"]

    response: dict = {
            'text': rules_text,
            'buttons': [
                {'title': 'Что ты умеешь?', 'hide': 'true'}
            ],
            'tts': rules_text,
            'end_session': 'false'
    }

    sessionstate = {
        "question_dict": {
            'sentence': rules_text,
            'answers': [],
            'variants': [],
            'category': []
        },
        "yesno_answertype": 1,
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
        "yesno_answertype": 1,
        "service": 11
    }

    return {
        "response": response,
        "session_state": sessionstate
    }