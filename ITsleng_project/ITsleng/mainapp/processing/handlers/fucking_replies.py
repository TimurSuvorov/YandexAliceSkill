import random

from mainapp.processing.extract_json import get_db_sentences
from mainapp.processing.handlers.generate_question import tts_prompt_sound
from mainapp.processing.handlers.generate_variants_objects import generate_var_string, generate_var_buttons


def fucking_replies(command, session_state):
    sentences = get_db_sentences()
    fucking_sentence = random.choice(sentences["FUCKINGsentence"])
    postsentence = random.choice(sentences["POSTsentence"])
    letstart_empty = random.choice(["Мы начнём уже?",
                                    "Ты собираешься поиграть со мной?",
                                    "Начнём уже?",
                                    "Начнём игру?"
                                    ])
    letstart_noempty = random.choice(["Давай повторю последний вопрос.",
                                      "Повторяю для тебя вопрос, если забыл.",
                                      "Ты остановился вот на каком вопросе.",
                                      "Вернемся к игре. Вот мой вопрос."
                                      ])


    # До этого не было задано вопросов
    if not session_state.get("question_dict"):
        response: dict = {
            'text': f'{fucking_sentence.replace(" - ", "").replace("+", "")} {letstart_empty.replace(" - ", "").replace("+", "")}',
            'tts': f'{fucking_sentence} sil <[70]> {letstart_empty}',
            'buttons': [
                {'title': 'Да', 'hide': 'true'},
                {'title': 'Нет', 'hide': 'true'}
            ],
            'end_session': 'False'
        }

        sessionstate = session_state
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

    # Если до этого был задан вопрос, то неважно какое сообщение - сервисное или игровое
    else:
        question_dict = session_state['question_dict']
        question_body = question_dict['sentence']
        attempt = session_state['attempt']
        question_variants = question_dict['variants'][:3]
        variants = generate_var_string(question_variants)

        response: dict = {
            'text': f'{fucking_sentence.replace(" - ", "").replace("+", "")} {letstart_noempty}\n✨{question_body.replace(" - ", "").replace("+", "")}\n{postsentence}:\n{variants.replace("+", "")}',
            'tts': f'{fucking_sentence} sil <[70]> {letstart_noempty} sil <[100]>{tts_prompt_sound(question_body)}. {postsentence}: sil <[50]>{variants}',
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
        }

        sessionstate = {
            "question_dict": question_dict,
            "attempt": attempt
        }

        analytics = {
            "events": [
                {
                    "name": "Валенок с вопросом",
                    "value": {
                        "Вопрос": session_state['question_dict']['sentence'],
                        "Ответ": command
                    }
                },
            ]
        }

        # Возвращаем сформированный вопрос, а также отдаем в session_state для дальнейшего учёта
    return {
        "response": response,
        "analytics": analytics,
        "session_state": sessionstate
    }