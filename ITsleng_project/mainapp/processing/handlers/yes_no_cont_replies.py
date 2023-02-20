import random
import re

from mainapp.processing.db.extract_json import get_db_sentences
from mainapp.processing.handle_sessionfile import get_qa_session_sentence
from mainapp.processing.handlers.generate_question import tts_prompt_sound
from mainapp.processing.handlers.generate_variants_objects import generate_var_string, generate_var_buttons
from mainapp.processing.handlers.service_replies import bye_replies

yes_answer = [r"^да$", r"\bда$", "давай", "хорошо", "я не против", "начн.м", "продолж", "начать", r"\bok$", r"^окей$",
              r"начинаем$", r"поехали$", "продолжим", "продолжай", "дальше", "yes"]
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
                Призыв продолжить в форме закрытого вопроса

        - в начале игры (пользователь ещё не слышал вопроса);
            - положительный ответ;
                Создается новый вопрос
            - отрицательный ответ;
                Производится выход
            - не распознан;
                Призыв начать в форме закрытого вопроса
    """
    sentences = get_db_sentences()
    postsentence = random.choice(sentences["POSTsentence"])
    analytics = {}

    # Если ответ положительный и точно неотрицательный, то
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
            'text': f'Прекрасно! Мой вопрос.\n✨{question_body}\n{postsentence}:\n{variants}'.replace(" - ", "").replace("+", ""),
            'tts': f'Прекрасно! sil <[100]> Мой вопрос. {tts_prompt_sound(question_body)}. {postsentence}: sil <[50]>{variants}',
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

    # Если ответ не из списка Да/Нет, то прикинуться валенком
    else:
        # До этого не было задано вопросов
        if not session_state.get("question_dict"):
            yesno_tupik_replies = random.choice(
                ["Как-то нелогично. А я просто хочу поиграть. -  Поехали?",
                 "Я очень рада за сказанное тобой. Но давай уже начнём?",
                 "Не вижу в этом логики. -  Давай уже стартуем?",
                 "Отсутствие смысла иногда полезно, но не сейчас. Может, просто поиграем?",
                 "Всё возможно. Может, просто поиграем?"
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

        # До был задан вопрос, был перерыв на сервисное сообщение
        else:
            yesno_tupik_replies = random.choice(
                ["Я очень рада за тебя. Продолжим?",
                 "До этого я тебя лучше понимала. Давай просто продолжим?",
                 "Тут сложно что-то прокомментировать. Может просто продолжим?",
                 "Всё возможно. Поехали дальше?"
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
            'text': f'{yesno_tupik_replies}'.replace(" - ", "").replace("+", ""),
            'tts': f'{yesno_tupik_replies}',
            'buttons': [
                {'title': 'Да', 'hide': 'true'},
                {'title': 'Нет', 'hide': 'true'}
            ],
            'end_session': 'False'
        }

        # Передаём прозрачно
        sessionstate = session_state

    # Возвращаем сформированный вопрос, а также отдаем в session_state для дальнейшего учёта
    print("From yesno")
    return {
        "response": response,
        "analytics": analytics,
        "session_state": sessionstate
    }

