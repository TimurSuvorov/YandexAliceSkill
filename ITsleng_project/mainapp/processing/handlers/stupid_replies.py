import random

from mainapp.processing.db.extract_json import get_db_sentences
from mainapp.processing.handlers.generate_question import tts_prompt_sound
from mainapp.processing.handlers.generate_variants_objects import generate_var_string, generate_var_buttons


def stupid_replies(command, session_state):
    sentences = get_db_sentences()
    postsentence = random.choice(sentences["POSTsentence"])

    question_dict = session_state["question_dict"]
    question_body = question_dict["sentence"]
    question_variants = question_dict["variants"][:3]
    variants = generate_var_string(question_variants)

    stupid_phrases = ["Вр+оде, умный, а говоришь не впоп+ад. Дав+ай ещё раз и поразборчивей. Повторю вопросик.",
                      "Неож+иданный ответ. Попробуй сказать поразб+орчивей. Напомню вопрос и варианты.",
                      "Тут даже нет таких вариантов или мне показалось. Давай еще раз.",
                      "Интересный вариант ответа. Наверное, ты перепутал с другим вопросом. А мой был следующий.",
                      "Ты ув+ерен, что это ответ на м+ой вопрос? Давай попробуй ещё раз."
                      ]
    stupid_phrase = random.choice(stupid_phrases)
    response: dict = {
        'text': f'{stupid_phrase}\n✨{question_body}\n{postsentence}:\n {variants}'.replace(" - ", "").replace("+", ""),
        'tts': f'{stupid_phrase}sil <[100]> {tts_prompt_sound(question_body)}sil <[50]> {postsentence}sil <[50]>{variants}',
        'buttons': generate_var_buttons(question_variants),
        'end_session': 'False'
    }

    analytics = {
        "events": [
            {
                "name": "Ответа нет в перечне",
                "value": {
                    "Вопрос": session_state['question_dict']['sentence'],
                    "Варианты": question_variants,
                    "Ответ": command
                }
            },
        ]
    }

    return {
        "response": response,
        "analytics": analytics,
        "session_state": session_state
    }
