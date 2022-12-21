import random

from mainapp.processing.declension_scores import decl_scores
from mainapp.processing.handle_userprofile import get_scores_rating


def my_rating(session_state, user_id, session_id):
    # Вызов рейтинга
    cur_scores = get_scores_rating(user_id, session_id)
    allscores = cur_scores["allscores"]
    sessionscore = cur_scores["sessionscore"]
    rating_head = f'🏅🏅🏅Ваш рейтинг🏅🏅🏅\n\nОбщий: {allscores}\nВ этой игре: {sessionscore}\n'


    print(allscores)
    print(type(allscores))
    if int(allscores) != 0:
        rating_tts_only = random.choice(
            [f'Ты набрал {decl_scores(sessionscore)} за игру и {decl_scores(allscores)} за всё время.\n',
             f'Сейчас у тебя {decl_scores(sessionscore)} за игру и {decl_scores(allscores)} в целом.\n',
             f'У тебя за игру {decl_scores(sessionscore)} и всего {decl_scores(allscores)}.\n',
             f'Ты набрал {decl_scores(sessionscore)} за игру, а всего {decl_scores(allscores)}\n.'
             ])

        rating_text = random.choice(['Это весьма хорошо. Продолжим идти вперёд?',
                                     'Очень неплохо! Предлагаю не останавливаться на достигнутом. Продолжим игру?',
                                     'Уверена, что ты можешь больше. Продолжаем?',
                                     'Весьма недурно! -  Продолжим покорять вершины?',
                                     'Неплохой темп, но всё ещё впереди. Продолжаем? '
                                      ])
    else:
        rating_tts_only = random.choice(["У тебя по нулям.",
                                         "У тебя ноль баллов."
                                         ])
        rating_text = random.choice(['Не густо. Начнём покорять вершины?',
                                     'Маловато будет. Продолжим игру, чтоб это исправить?',
                                     'Уверена, что ты можешь на б+ольше. Продолжим игру, чтоб это исправить?',
                                     ])


    response: dict = {
        'text': f'{rating_head}\n{rating_text}'.replace(" - ", "").replace("+", ""),
        'buttons': [
            {'title': 'Да', 'hide': 'true'},
            {'title': 'Нет', 'hide': 'true'}
        ],
        'tts': f'{rating_tts_only}{rating_text}',
        'end_session': 'false'
    }

    # Состояние с предыдущем ответом передаем прозрачно, но добавляем флаг Да/Нет
    sessionstate = session_state
    sessionstate["yesno_type"] = 10

    analytics = {
            "events": [
                {
                    "name": "Запрос 'Рейтинг'",
                },
            ]
        }

    return {
        "response": response,
        "analytics": analytics,
        "session_state": sessionstate
    }