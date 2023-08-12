import random
import re

from mainapp.processing.db.extract_json import get_db_sentences
from mainapp.processing.db.images import Image
from mainapp.processing.handle_sessionfile import get_qa_session_sentence
from mainapp.processing.handlers.proc_response_obj import generate_var_string, generate_var_buttons, \
    tts_prompt_sound, remove_tts_symbols
from mainapp.processing.handlers.service_replies import bye_replies

yes_answer = [r"^да$", r"\bда$", "давай", "хорошо", "я не против", "начн.м", "продолж", "начать", r"\bok$", r"^окей$",
              r"начинаем$", r"поехали$", "продолжим", "продолжай", "дальше", "yes", "ага", "попробуем$", "^попробуем", "угу"]
no_answer = ["нет", "не хочу", "потом", "выйти", "выход", "хватит", "давай, не будем", "не будем", "не начинаем", "no$"]


def yes_no_cont_replies(command, session_state, session_id, intents):
    """
    Функция формирует ответ на команду от пользователя, где подразумевается ответ на закрытый вопрос -
    положительный или отрицательный. Зависит от:
        - во время игры (вопрос уже был задан ранее):
            - положительный ответ;
                Возвращается с дополнительными фразами.
            - отрицательный ответ;
                Производится выход
            - не распознан;
                Нейтральная фраза и призыв продолжить в форме закрытого вопроса

        - в начале игры (пользователь ещё не слышал вопроса);
            - положительный ответ;
                Создается новый вопрос
            - отрицательный ответ;
                Производится выход
            - не распознан;
                Нейтральная фраза и призыв начать в форме закрытого вопроса
    """
    sentences = get_db_sentences()
    postsentence = random.choice(sentences["POSTsentence"])
    analytics = {}

    # Если ответ положительный и точно неотрицательный и не проходящий по интентам, то
    if (re.search("|".join(yes_answer), command) or intents.get('YANDEX.CONFIRM', {})) and \
            not intents.get('YANDEX.REJECT', {}) and \
            not re.search("|".join(no_answer), command):
        # Если в прошлом ответе есть вопрос, значит его возвращаем
        if session_state.get('question_dict', {}).get('answers'):
            question_dict = session_state['question_dict']
            question_body = question_dict['sentence']
            question_variants = question_dict['variants'][:3]
            variants = generate_var_string(question_variants)
            attempt = session_state['attempt']
        else:
            # Берем новый вопрос для сессии
            question_dict = get_qa_session_sentence(session_id)
            question_body = question_dict["sentence"]
            question_variants = question_dict["variants"][:3]
            variants = generate_var_string(question_variants)
            attempt = 1

        response: dict = {
            'text': remove_tts_symbols(f'Прекрасно! Мой вопрос.\n\n✨{question_body}\n{postsentence}:\n{variants}'),
            'tts': f'Прекрасно! sil <[100]> Мой вопрос. {tts_prompt_sound(question_body)}. {postsentence}: sil <[50]>{variants}',
            'card': {
                'type': 'BigImage',
                'image_id': Image.NEW_QUEST.id,
                'title': '',
                'description': remove_tts_symbols(f'Прекрасно! Мой вопрос.\n\n✨{question_body}\n{postsentence}:\n{variants}')
            },
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
        }

        analytics = {
            "events": [
                {
                    "name": "Новый вопрос",
                    "value": {
                        "Вопрос": question_body.replace(" - ", "").replace("+", ""),
                    }
                },
            ]
        }

        sessionstate = {
            "question_dict": question_dict,
            "attempt": attempt
        }

    # Если ответ отрицательный, то прощаемся
    elif re.search("|".join(no_answer), command):
        response = bye_replies(session_state, session_id)["response"]
        sessionstate = session_state

    # Если ответ не распознан, то формируем нейтральную фразу
    else:
        # До этого не было задано вопросов
        if not session_state.get("question_dict"):
            norecognize_for_yesno = random.choice(
                [
                    "Как-то нелогично. sil <[100]>А я просто хочу поиграть.sil <[100]> Поехали?",
                    "Я очень рада за сказанное тобой. sil <[100]>Но давай уже начнём?",
                    "Не вижу в этом логики. sil <[100]>Давай уже стартуем?",
                    "Отсутствие смысла иногда полезно, но не сейчас.sil <[100]> Может, просто поиграем?",
                    "Всё возможно.sil <[100]> Может, просто поиграем?"
                ]
            )

            analytics = {
                "events": [
                    {
                        "name": "Вне сценария без вопроса",
                        "value": {
                            "Ответ": command
                        }
                    },
                ]
            }

        # До этого был задан вопрос (прерывание на сервисное сообщение)
        else:
            norecognize_for_yesno = random.choice(
                ["Как-то нелогично. sil <[100]>А я просто хочу поиграть.sil <[100]> Давай дальше?",
                 "Я очень рада за сказанное тобой. sil <[100]>Но давай уже продолжим?",
                 "Не вижу в этом логики. sil <[100]>Давай уже продолжим?",
                 "Отсутствие смысла иногда полезно, но не сейчас.sil <[100]> Может, просто поиграем?",
                 "Всё возможно.sil <[100]> Может, просто поиграем?",
                 "Кажется, ты знаешь много всего, но как-то не очень связно говоришь. sil <[100]>Хочешь дальше поиграть?",
                 ]
            )

            analytics = {
                "events": [
                    {
                        "name": "Вне сценария с вопросом",
                        "value": {
                            "Вопрос": session_state['question_dict']['sentence'],
                            "Ответ": command
                        }
                    },
                ]
            }

        response: dict = {
            'text': remove_tts_symbols(f'{norecognize_for_yesno}'),
            'tts': f'{norecognize_for_yesno}',
            'card': {
                'type': 'BigImage',
                'image_id': Image.OFF_SCRIPT.id,
                'title': 'Хммм...',
                'description': remove_tts_symbols(f'{norecognize_for_yesno}')
            },
            'buttons': [
                {'title': 'Да', 'hide': 'true'},
                {'title': 'Нет', 'hide': 'true'}
            ],
            'end_session': 'False'
        }

        # Передаём прозрачно
        sessionstate = session_state

    # Возвращаем сформированный вопрос, а также отдаем в session_state для дальнейшего учёта
    return {
        "response": response,
        "analytics": analytics,
        "session_state": sessionstate
    }
