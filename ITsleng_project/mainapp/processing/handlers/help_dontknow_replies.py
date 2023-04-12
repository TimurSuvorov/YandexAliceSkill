import random

from .proc_response_obj import generate_var_buttons, generate_var_string, tts_prompt_sound, remove_tts_symbols
from mainapp.processing.db.extract_json import get_db_sentences, get_db_sounds
from ..handle_sessionfile import get_qa_session_sentence
from ..handle_userprofile import update_scores, get_scores_rating


def dontknow(command, session_state, user_id, session_id):
    """
    Функция формирует ответ на команду не знания или сдачи пользователя в зависимости от:
        - во время игры (вопрос уже был задан ранее);
        - в начале игры (пользователь ещё не слышал вопроса);
    Если был вопрос до этого, то пользователь проиграл и формируется новый вопрос.
    Если вопроса не было в качестве аргумента функция принимает предыдущее состояние и передает его прозрачно.
    Добавление в ответ флага AppMetrics: "Вне сценария без вопроса", "Сдался" + "Новый вопрос" и параметры.
    """
    # Если "session_state" пустой по каким-либо причинам, Алиса прикинится валенком
    noquestionbefore = random.choice(
        ['А ведь мы даже ещё не начали, а ты такое говоришь. Давай я уже спрошу тебя о чём-нибудь?',
         'Мы пока ещё в начале пути. Давай уже стартуем?'
         ]
    )
    if not session_state.get("question_dict"):
        response: dict = {
            'text': f'{noquestionbefore}',
            'tts': f'{noquestionbefore}',
            'buttons': [{'title': 'Давай', 'hide': 'true'}],
            'end_session': 'False'
        }
        sessionstate = session_state

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
    else:
        sounds = get_db_sounds()
        wrongsound = random.choice(sounds["WRONG"])
        sentences = get_db_sentences()
        postsentence = random.choice(sentences["POSTsentence"])
        noworrysentence = random.choice(sentences["NOWORRYsentence"])
        letnext = random.choice(sentences["LETSNEXTsentence"])
        # Получаем первый из списка правильный ответ и его объяснение
        answer = session_state["question_dict"]["answers"][0]
        question_explanation = session_state["question_dict"]["explanation"]
        # Берем новый вопрос для сессии
        question_dict = get_qa_session_sentence(session_id)
        # Из вопроса-словаря берем сам вопрос для подстановки в ответ
        question_body = question_dict["sentence"]
        # Генерируем кнопки для нового вопроса
        question_variants = question_dict["variants"][:3]
        variants = generate_var_string(question_variants)

        # Получение рейтинга и его отображение
        cur_scores = get_scores_rating(user_id, session_id)
        allscores = cur_scores["allscores"]
        sessionscore = cur_scores["sessionscore"]
        cur_rating = f'\n\n🏅Ваш рейтинг:\nОбщий: {allscores}\nВ этой игре: {sessionscore}'

        response: dict = {
            'text': remove_tts_symbols(f'{noworrysentence}\nПравильный ответ: {answer}.\n{question_explanation} \n{letnext}.\n✨{question_body}\n{postsentence}:\n{variants}{cur_rating}'),
            'tts': f'{wrongsound}sil <[5]>{noworrysentence}sil <[70]> Правильный ответ: sil <[70]> {answer}.sil <[70]> {question_explanation} sil <[100]> {letnext}. sil <[100]> {tts_prompt_sound(question_body)}.sil <[50]> {postsentence}:sil <[50]> {variants}',
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
        }

        sessionstate = {
            "question_dict": question_dict,
            "attempt": 1,
        }
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
                        "Вопрос": remove_tts_symbols(question_dict["sentence"]),
                    }
                }
            ]
        }

    return {
        "response": response,
        "analytics": analytics,
        "session_state": sessionstate
    }
