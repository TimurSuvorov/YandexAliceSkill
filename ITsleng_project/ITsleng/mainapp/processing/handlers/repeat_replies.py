import random

from .generate_question import tts_prompt_sound
from .generate_variants_objects import generate_var_buttons, generate_var_string
from mainapp.processing.extract_json import get_db_sentences


def repeat_replies(session_state: dict) -> dict:
    sentences = get_db_sentences()
    postsentence = random.choice(sentences["POSTsentence"])

    # Если пустой по каким-либо причинам, Алиса прикинится валенком
    if not session_state.get("question_dict"):
        response: dict = {
            'text': f'Мы ещё не начали, а ты уже просишь повторить. Давай уже начнём? Но если тебе нужна помощь, скажи "Правила" или "Помоги"',
            'tts': f'Мы ещё не начали, а ты уже просишь повторить. Давай уже начнём? Но если тебе нужна помощь, скажи "Правила" или "Помоги"',
            'buttons': [{'title': 'Начнём', 'hide': 'true'},
                        {'title': 'Правила', 'hide': 'true'},
                        {'title': 'Что ты умеешь?', 'hide': 'true'}],
            'end_session': 'False'
        }
        session_state = {}
    else:
        question_dict = session_state["question_dict"]
        question_body = question_dict["sentence"]
        question_variants: list = question_dict["variants"]
        variants = generate_var_string(question_variants)
        # Проверяем признак того, что перед нами вопрос с вариантами ответов, а не сервисное
        if len(question_variants) > 0:
            response: dict = {
                'text': f'✨{question_body.replace(" - ", "").replace("+", "")}\n{postsentence}:\n {variants.replace("+", "")}',
                'tts': f'Конечно!sil <[100]> {tts_prompt_sound(question_body)}sil <[50]> {postsentence}sil <[50]>{variants}',
                'buttons': generate_var_buttons(question_variants),
                'end_session': 'False'
            }
        else:
            response: dict = {
                'text': f'✨{question_body.replace(" - ", "").replace("+", "")}',
                'tts': f'Конечно!sil <[100]>{tts_prompt_sound(question_body)}',
                'buttons': [{'title': 'Дальше', 'hide': 'true'}],
                'end_session': 'False'
            }

    analytics = {
        "events": [
            {
                "name": "Повторить",
                "value": {
                    "Объект повторения": response['text'],
                }
            },
        ]
    }

    return {
            "response": response,
            "analytics": analytics,
            "session_state": session_state
        }