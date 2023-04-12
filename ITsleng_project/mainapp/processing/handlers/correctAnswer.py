import random

from ..declension_numbers import decl_scores
from mainapp.processing.db.extract_json import get_db_sentences, get_db_sounds
from .proc_response_obj import generate_var_buttons, generate_var_string, tts_prompt_sound, remove_tts_symbols
from ..handle_sessionfile import get_qa_session_sentence
from ..handle_userprofile import update_scores


def correctanswer(command, session_state, user_id, session_id, message_id):

    # Выбираем случайным образом предложение похвалы и "вариантов"
    sentences = get_db_sentences()
    nicesentence = random.choice(sentences["NICEsentence"])
    postsentence = random.choice(sentences["POSTsentence"])
    sayrating = ''
    letsnext = random.choice(sentences["LETSNEXTsentence"])

    # Проверяем на схожесть слова
    rightanswer = session_state["question_dict"]["answers"][0].replace("+", "").replace(" - ", "")
    if rightanswer != command:  # FIXIT check by regex
        nicesentence = random.choice(["Пишется по-другому, но я поняла.sil <[100]> Верно!",
                                      "Нечетко говоришь, но, похоже, ты прав!",
                                      "Было непросто понять твои слова,sil <[100]> но ты прав!",
                                      "Я тебя поняла!sil <[100]> Верно!",
                                      "Не уверена в совпадении на 100 процентов.sil <[100]> Хорош+о,sil <[100]> засчит+аем!"
                                      ])

    # Показывать или нет объяснение при верном ответе
    question_explanation = ""
    answer = session_state["question_dict"]["answers"][0]
    if random.choice([True, False, False]):
        question_explanation = session_state["question_dict"]["explanation"]
        question_explanation = f'Ответ: {answer}. -  {question_explanation}'

    # Подсчёт рейтинга и его отображение
    score = session_state["attempt"] + 1
    cur_scores = update_scores(user_id, session_id, score)
    allscores = cur_scores["allscores"]
    sessionscore = cur_scores["sessionscore"]
    cur_rating = f'\n\n🏅Ваш рейтинг:\nОбщий: {allscores}\nВ этой игре: {sessionscore}'

    # Если первый верный ответ, то поздравим с этим
    if 1 <= cur_scores["allscores"] <= 2:
        nicesentence = f'Поздравляю с первым верным ответом!sil <[100]> Отличное начало.sil <[90]> У тебя плюс {decl_scores(sessionscore)}.'
        question_explanation = ''
    # Если баллов больше 5 и сообщение каждое 4-е или 5-е
    elif sessionscore > 4 and message_id % random.choice([3, 4]) == 0:
        cur_rating = ''
        sayrating = random.choice(
            [f'Движешься уверенно вперёд. Ты набрал {decl_scores(sessionscore)} за игру и {decl_scores(allscores)} за всё время.\n',
             f'Сейчас у тебя {decl_scores(sessionscore)} за игру и {decl_scores(allscores)} в целом. Очень неплохо!\n',
             f'Поражаюсь твоей целеустремленности. У тебя за игру {decl_scores(sessionscore)} и всего {decl_scores(allscores)}.\n',
             f'Я верила в тебя не зря! Ты набрал {decl_scores(sessionscore)} за игру, а всего {decl_scores(allscores)}.\n'
             ]
        )

    # Выбираем звуки
    sounds = get_db_sounds()
    correctsound = random.choice(sounds["CORRECT"])
    # Берем новый вопрос для сессии
    question_dict = get_qa_session_sentence(session_id)
    # Из вопроса-словаря берем сам вопрос и варианты ответов
    question_body = question_dict["sentence"]
    question_variants = question_dict["variants"][:3]
    variants = generate_var_string(question_variants)

    response: dict = {
            'text': remove_tts_symbols(f'👍{nicesentence}\n{question_explanation}\n{sayrating}{letsnext}.\n✨{question_body} \n{postsentence}:\n{variants}{cur_rating}'),
            'tts': f'{correctsound}sil <[50]>{nicesentence}sil <[100]>{question_explanation} sil <[100]> {sayrating} sil <[100]>{letsnext}sil <[100]>{tts_prompt_sound(question_body)}sil <[50]>.{postsentence}:sil <[50]>{variants}',
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
    }
    # Возвращаем сформированный вопрос, а также отдаем в session_state для дальнейшего учёта
    return {
        "response": response,
        "analytics": {
            "events": [
                {
                    "name": "Верный ответ",
                    "value": {
                        "Вопрос": session_state["question_dict"]["sentence"],
                        "Ответ": command
                        }
                },
                {
                    "name": "Новый вопрос",
                    "value": {
                        "Вопрос": question_body,
                    }
                },
            ]
        },
        "session_state": {
            "question_dict": question_dict,
            "attempt": 1
        }
    }
