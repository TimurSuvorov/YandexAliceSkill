import random

from mainapp.processing.declension_scores import decl_scores
from mainapp.processing.handle_userprofile import get_scores_rating


def my_rating(session_state: dict, user_id: str, session_id: str) -> dict:
    """
    Функция формирует ответ с рейтингом пользователя общий и для текущей сессии в зависимости от:
        -нулевой рейтинг;
        -ненулевой рейтинг;
    Для отображения и озвучки контекст разный.
    В качестве аргумента функция принимает предыдущее состояние и отдает его прозрачно в ответ (пользователь
    продолжает с места во время запроса рейтинга), но уже с флагом закрытого вопроса.
    Добавление в ответ флага AppMetrics: "Запрос 'Рейтинг'"
    """
    cur_scores = get_scores_rating(user_id, session_id)
    allscores = cur_scores["allscores"]
    sessionscore = cur_scores["sessionscore"]
    rating_head = f'🏅🏅🏅Ваш рейтинг🏅🏅🏅\n\nОбщий: {allscores}\nВ этой игре: {sessionscore}\n'

    if int(allscores) != 0:
        rating_message = random.choice(
            ['Это весьма хорошо. Продолжим идти вперёд?',
             'Очень неплохо! Предлагаю не останавливаться на достигнутом. Продолжим игру?',
             'Уверена, что ты можешь больше. Продолжим?',
             'Весьма недурно! -  Продолжим покорять вершины?',
             'Неплохой темп, но всё ещё впереди. Продолжим? '
             ]
        )
        rating_tts_only = random.choice(
            [f'Ты набрал {decl_scores(sessionscore)} за игру и {decl_scores(allscores)} за всё время.\n',
             f'Сейчас у тебя {decl_scores(sessionscore)} за игру и {decl_scores(allscores)} в целом.\n',
             f'У тебя за игру {decl_scores(sessionscore)} и всего {decl_scores(allscores)}.\n',
             f'Ты набрал {decl_scores(sessionscore)} за игру, а всего {decl_scores(allscores)}\n.'
             ])

    else:
        rating_tts_only = random.choice(["У тебя по нулям.",
                                         "У тебя ноль баллов."
                                         ])
        rating_message = random.choice(
            ['Не густо. Начнём покорять вершины?',
             'Маловато будет. Продолжим игру, чтоб это исправить?',
             'Уверена, что ты можешь на б+ольшее. Продолжим игру, чтоб это исправить?',
             ]
        )

    response: dict = {
        'text': f'{rating_head} \n{rating_message}'.replace(" - ", "").replace("+", ""),
        'buttons': [
            {'title': 'Да', 'hide': 'true'},
            {'title': 'Нет', 'hide': 'true'}
        ],
        'tts': f'{rating_tts_only}{rating_message}',
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