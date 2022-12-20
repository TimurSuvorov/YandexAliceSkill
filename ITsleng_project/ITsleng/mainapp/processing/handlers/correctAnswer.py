import random

from .generate_question import tts_prompt_sound
from ..declension_scores import decl_scores
from ..extract_json import get_db_sentences, get_db_sounds
from .generate_variants_objects import generate_var_buttons, generate_var_string
from ..handle_sessionfile import get_qa_session_sentence
from ..handle_userprofile import update_scores, get_scores_rating


def correctanswer(command, session_state, user_id, session_id, message_id):
    # Берем новый вопрос для сессии
    question_dict = get_qa_session_sentence(session_id)
    # Выбираем случайным образом предложение похвалы и "вариантов"
    sentences = get_db_sentences()
    nicesentence = random.choice(sentences["NICEsentence"])
    postsentence = random.choice(sentences["POSTsentence"])
    sayrating = ''
    letsnext = random.choice(sentences["LETSNEXTsentence"])

    # Проверяем на схожесть слова
    rightanswer = session_state["question_dict"]["answers"][0].replace("+", "")
    if rightanswer != command:  # FIXIT check by regex
        nicesentence = random.choice(["Пишется по-другому, но я поняла. Верно!",
                                      "Нечетко говоришь, но, похоже, ты прав!",
                                      "Было непросто понять твои слова, но ты прав!",
                                      "Я тебя поняла! Верно!"
                                      ]
                                     )

    # Выбираем звуки
    sounds = get_db_sounds()
    correctsound = random.choice(sounds["CORRECT"])

    # Из вопроса-словаря берем сам вопрос и варианты ответов
    question_body = question_dict["sentence"]
    question_variants = question_dict["variants"]
    variants = generate_var_string(question_variants)

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
        nicesentence = f'Поздравляю с первым верным ответом! Отличное начало. У тебя {decl_scores(sessionscore)}.'
        question_explanation = ''
    # Если баллов больше 5 и сообщение каждое 4-е или 5-е
    elif sessionscore > 5 and message_id % random.choice([4, 5]) == 0:
        cur_rating = ''
        sayrating = random.choice(
            [f'Движешься уверенно вперёд. Ты набрал {decl_scores(sessionscore)} за игру и {decl_scores(allscores)} за всё время.',
             f'Сейчас у тебя {decl_scores(sessionscore)} за игру и {decl_scores(allscores)} в целом. Очень неплохо!',
             f'Поражаюсь твоей целеустремленности. У тебя за игру {decl_scores(sessionscore)} и всего {decl_scores(allscores)}',
             f'Я верила в тебя не зря! Ты набрал {decl_scores(sessionscore)} за игру, а всего {decl_scores(allscores)}.'
             ]
        )


    response: dict = {
            'text': f'👍{nicesentence}\n{question_explanation}\n{sayrating}\n{letsnext}.\n✨{question_body} \n{postsentence}:\n{variants}{cur_rating}'.replace(" - ", "").replace("+", ""),
            'tts': f'{correctsound}sil <[50]>{nicesentence}{question_explanation} sil <[100]> {sayrating} sil <[100]>{letsnext}sil <[100]>{tts_prompt_sound(question_body)}sil <[50]>.{postsentence}:sil <[50]>{variants}',
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
    }
    print("From correctanswer")
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
