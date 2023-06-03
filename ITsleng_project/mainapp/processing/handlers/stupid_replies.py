import random

from mainapp.processing.db.extract_json import get_db_sentences
from mainapp.processing.handlers.proc_response_obj import generate_var_string, generate_var_buttons, \
    tts_prompt_sound, remove_tts_symbols


def stupid_replies(command, session_state):
    """
    Формирование ответа на случай, если ответ от пользователя не коррелирует ни с одним из вариантов.
    Произносится нейтральная фраза и повторяется вопрос.
    """
    sentences = get_db_sentences()
    postsentence = random.choice(sentences["POSTsentence"])

    question_dict = session_state["question_dict"]
    question_body = question_dict["sentence"]
    question_variants = question_dict["variants"][:3]
    variants = generate_var_string(question_variants)

    stupid_phrases = \
        [
            "Вр+оде, умный, а говоришь не впоп+ад. sil <[100]>Дав+ай ещё раз и поразборчивей. Повторю вопросик.",
            "Неож+иданный ответ. sil <[100]>Попробуй сказать поразб+орчивей. Напомню вопрос и варианты.",
            "Плохо рассл+ышала тебя sil <[70]>или ты оп+ять говоришь со своим кот+ом. sil <[100]>Повтор+им.",
            "Вот тут я зависла. sil <[100]>Ты точно отвечаешь на этот вопрос?. sil <[100]>Напомню ещё разок.",
            "Тут даже нет таких вариантов или мне показалось.sil <[100]>Постарайся говорить чётко. sil <[100]>Давай еще раз.",
            "Или я совсем стара sil <[80]>и не расслышала слово, sil <[80]>л+ибо ты о другом. sil <[100]>Повторю тебе вопрос.",
            "Интересный вариант ответа.sil <[100]> Наверное, ты перепутал с другим вопросом. sil <[100]>А мой был следующий.",
            "Ты ув+ерен, что это ответ на м+ой вопрос? sil <[100]>Постарайся говорить чётко. sil <[100]>Давай попробуй ещё раз.",
            "Не вижу в этом логики. sil <[100]>Повторю вопросик.",
            "Иногда я слышу по-другому. Похоже, это произошло и сейчас. Но вопрос повторю всё же.",
            "Отсутствие смысла иногда полезно, но не сейчас.sil <[100]> Ответь мне чётко.",
            "Кажется, ты знаешь много всего, но как-то не очень связно говоришь. sil <[100]>Повторю тебе вопрос.",
            "Ты +явно компет+ентен в этой области, но м+ожет стоит немного подумать, прежде чем говорить. sil <[100]>Итак.",
            "Ты точно знаешь, о чем говоришь, но иногда твои мысли рассеиваются. sil <[100]>Попробуем ещё раз."
         ]
    stupid_phrase = random.choice(stupid_phrases)
    response: dict = {
        'text': remove_tts_symbols(f'{stupid_phrase}\n✨{question_body}\n{postsentence}:\n{variants}'),
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
