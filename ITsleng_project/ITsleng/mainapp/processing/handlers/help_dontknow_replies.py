import random

from .generate_question import generate_question, tts_prompt_sound
from .generate_variants_objects import generate_var_buttons, generate_var_string
from .next_question import next_question
from ..extract_json import get_db_sentences, get_db_sounds


def dontknow(command, session_state):
    # Если "session_state" пустой по каким-либо причинам, Алиса прикинится валенком
    noquestionbefore = random.choice(['А ведь мы даже ещё не начали, а ты такое говоришь. Давай я уже спрошу тебя о чём-нибудь?',
                                      'Мы пока ещё в начале пути. Давай начнём?'
                                      ])
    if not session_state.get("question_dict"):
        response: dict = {
            'text': f'{noquestionbefore}',
            'tts': f'{noquestionbefore}',
            'buttons': [{'title': 'Давай', 'hide': 'true'}],
            'end_session': 'False'
        }
        sessionstate = session_state
        # Ответа валенка
        analytics = {
            "events": [
                {
                    "name": "Валенок без вопроса",
                    "value": {
                        "Ответ": command
                    }
                },
            ]
        }

    # Если сообщение было сервисным, то генерируем новый вопрос
    elif session_state.get("service"):
        print('Ненужный сценарий???')
        question_dict = generate_question()
        response_dict = next_question(question_dict)
        response = response_dict["response"]
        sessionstate = response_dict["session_state"]
        print("From dontknow")
        analytics = {
            "events": [
                {
                    "name": "Новый вопрос",
                    "value": {
                        "Вопрос": question_dict["sentence"].replace(" - ", "").replace("+", ""),
                    }
                }
            ]
        }

    else:
        sentences = get_db_sentences()
        postsentence = random.choice(sentences["POSTsentence"])
        # Получаем первый из списка правильный ответ и его объяснение
        answer = session_state["question_dict"]["answers"][0]
        question_explanation = session_state["question_dict"]["explanation"]
        # Генерируем сразу новый вопрос и восстанавливаем количество попыток к нему
        question_dict = generate_question()
        # Из вопроса-словаря берем сам вопрос для подстановки в ответ
        question_body = question_dict["sentence"]
        # Генерируем кнопки для нового вопроса
        question_variants = question_dict["variants"]

        sounds = get_db_sounds()
        wrongsound = random.choice(sounds["WRONG"])
        noworrysentence = random.choice(sentences["NOWORRYsentence"])
        letnext = random.choice(sentences["LETSNEXTsentence"])
        variants = generate_var_string(question_variants)

        response: dict = {
            'text': f'{noworrysentence}\nПравильный ответ: {answer.capitalize().replace("+", "")}.\n{question_explanation.replace(" - ", "").replace("+", "")} \n{letnext}. ✨{question_body.replace(" - ", "").replace("+", "")}\n{postsentence}:\n{variants.replace("+", "")}',
            'tts': f'{wrongsound}sil <[5]>{noworrysentence}sil <[50]> Правильный ответ: sil <[50]> {answer}.sil <[50]> {question_explanation} sil <[100]> {letnext}. sil <[100]> {tts_prompt_sound(question_body)}.sil <[50]> {postsentence}:sil <[50]> {variants}',
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
        }

        sessionstate = {
            "question_dict": question_dict,
            "attempt": 1,
        }
        print("From dontknow_")
        analytics = {
            "events": [
                {
                    "name": "Сдался",
                    "value": {
                        "Вопрос": session_state["question_dict"]["sentence"],
                    }
                },
                {
                    "name": "Новый вопрос",
                    "value": {
                        "Вопрос": question_dict["sentence"].replace(" - ", "").replace("+", ""),
                    }
                }
            ]
        }

    return {
        "response": response,
        "analytics": analytics,
        "session_state": sessionstate
    }