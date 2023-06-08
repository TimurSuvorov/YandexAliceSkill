import random

from mainapp.processing.db.extract_json import get_db_sentences
from mainapp.processing.handlers.proc_response_obj import generate_var_string, generate_var_buttons, \
    tts_prompt_sound, remove_tts_symbols


def many_words(command: str, session_state: dict) -> dict:
    """
    Функция формирует ответ на длинную команду от пользователя в зависимости от:
        - во время игры (вопрос уже был задан ранее);
        - в начале игры (пользователь ещё не слышал вопроса);
    Если был вопрос до этого, то мы берём все его компоненты и формируем соответствующий ответ с дополнительными
    фразами.
    В качестве аргумента функция принимает предыдущее состояние и передает его прозрачно.
    Добавление в ответ флага AppMetrics: "Много слов без вопроса" или "Много слов с вопросом" и параметры.
    """
    sentences = get_db_sentences()
    manywords_sentence = random.choice(sentences["MANYWORDSsentence"])
    postsentence = random.choice(sentences["POSTsentence"])
    letstart_sentence = random.choice(sentences["LETSSTARTsentence"])
    letscontinue_sentence = random.choice(sentences["LETSCONTINUEsentence"])

    # до этого не было задано вопросов
    if not session_state.get("question_dict"):
        response: dict = {
            'text': remove_tts_symbols(f'{manywords_sentence} {letstart_sentence}'),
            'tts': f'{manywords_sentence} sil <[70]> {letstart_sentence}',
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
                    "name": "Много слов без вопроса",
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
        question_variants = question_dict['variants'][:3]
        variants = generate_var_string(question_variants)

        response: dict = {
            'text': remove_tts_symbols(f'{manywords_sentence} {letscontinue_sentence}\n\n✨{question_body}\n{postsentence}:\n{variants}'),
            'tts': f'{manywords_sentence} sil <[70]> {letscontinue_sentence} sil <[100]>{tts_prompt_sound(question_body)}. {postsentence}: sil <[50]>{variants}',
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
        }

        sessionstate = session_state

        analytics = {
            "events": [
                {
                    "name": "Много слов с вопросом",
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
