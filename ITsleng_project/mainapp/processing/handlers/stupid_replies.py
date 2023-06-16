import random

from mainapp.processing.db.extract_json import get_db_sentences, get_db_sounds
from mainapp.processing.handle_sessionfile import get_qa_session_sentence
from mainapp.processing.handle_userprofile import update_scores
from mainapp.processing.handlers.proc_response_obj import (
    generate_var_string,
    generate_var_buttons,
    tts_prompt_sound,
    remove_tts_symbols,
)


def stupid_replies(command: str, session_state: dict, user_id: str, session_id: str):
    """
    Формирование ответа на случай, если ответ от пользователя не коррелирует ни с одним из вариантов.
    Произносится нейтральная фраза и повторяется вопрос.
    """
    sentences = get_db_sentences()
    postsentence = random.choice(sentences["POSTsentence"])

    sounds = get_db_sounds()
    hmmmsound = random.choice(sounds["HMMM"])


    question_dict = session_state["question_dict"]
    question_body = question_dict["sentence"]
    question_variants = question_dict["variants"][:3]
    variants = generate_var_string(question_variants)

    unrecognized_attempt = session_state.setdefault("unrecognized_attempt", 0)
    # if not session_state.get("unrecognized_attempt"):
    #     session_state["unrecognized_attempt"] = 0
    # unrecognized_attempt = session_state.get("unrecognized_attempt")
    if unrecognized_attempt < 2:

        unrecognized_phrases = [
            "Вр+оде, умный, а говоришь не впоп+ад. sil <[100]>Дав+ай ещё раз и поразборчивей. Повторю вопросик.",
            "Неож+иданный ответ. sil <[100]>Попробуй сказать поразб+орчивей. Напомню вопрос и варианты.",
            "Плохо рассл+ышала тебя sil <[70]>или ты оп+ять говоришь со своим кот+ом. sil <[100]>Повтор+им.",
            "Вот тут я зависла. sil <[100]>Ты точно отвечаешь на этот вопрос? sil <[100]>Напомню ещё разок.",
            "Тут даже нет таких вариантов или мне показалось.sil <[100]> Постарайся говорить чётко. sil <[100]>Давай еще раз.",
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
        unrecognized_phrase = random.choice(unrecognized_phrases)
        response: dict = {
            'text': remove_tts_symbols(f'{unrecognized_phrase}\n\n✨{question_body}\n{postsentence}:\n{variants}'),
            'tts': f'{hmmmsound}sil <[10]>{unrecognized_phrase}sil <[100]> {tts_prompt_sound(question_body)}sil <[50]> {postsentence}sil <[50]>{variants}',
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
        }

        session_state["unrecognized_attempt"] += 1

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

    else:
        workaround_phrases = [
            "Иногда сложно выговорить то, что непонятно. Давай пропустим вопрос...",
            "Иногда я слышу по-другому. Похоже, это произошло и сейчас. Забудем это и пойдём дальше...",
            "Это уже слишком. Я не могу понять, о чём ты говоришь. Задам тебе новый вопрос...",
            "Я безнадёжно тебя н+е понимаю. Может, у нас получится что-нибудь со следующим вопросом...",
            "Моя твоя н+е понимать. Такое бывает иногда. Давай пропустим вопрос...",
            "Я снова не расслышала, хотя уши чищу каждый день. Я прощаю этот вопрос и задам другой..."
        ]
        workaround_phrase = random.choice(workaround_phrases)
        questionsound = random.choice(sounds["QUESTION"])
        # Берем новый вопрос для сессии и восстанавливаем количество попыток к нему
        question_dict = get_qa_session_sentence(session_id)
        attempt = 1
        # Из вопроса-словаря берем сам вопрос для подстановки в ответ
        question_body = question_dict["sentence"]
        # Генерируем кнопки для нового вопроса
        question_variants = question_dict["variants"][:3]
        variants = generate_var_string(question_variants)

        # Подсчёт рейтинга и его отображение
        score = 0
        cur_scores = update_scores(user_id, session_id, score)
        allscores = cur_scores["allscores"]
        sessionscore = cur_scores["sessionscore"]
        cur_rating = f'\n\n🏅Ваш рейтинг:\nОбщий: {allscores}\nВ этой игре: {sessionscore}'

        response: dict = {
            'text': remove_tts_symbols(f'{workaround_phrase}\n\n✨{question_body} \n{postsentence}:\n{variants}{cur_rating}'),
            'tts': f'{hmmmsound}sil <[10]>{workaround_phrase} sil <[110]>{questionsound}{tts_prompt_sound(question_body)} {postsentence}sil <[90]> {variants}',
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
        }

        session_state = {
            "question_dict": question_dict,
            "attempt": attempt
        }

        analytics = {
            "events": [
                {
                    "name": "Ответа нет в перечне, нет попыток",
                    "value": {
                        "Вопрос": session_state["question_dict"]["sentence"],
                        "Ответ": command
                    }
                },
                {
                    "name": "Новый вопрос",
                    "value": {
                        "Вопрос": remove_tts_symbols(question_body),
                    }
                }
            ]
        }

    return {
        "response": response,
        "analytics": analytics,
        "session_state": session_state
    }
