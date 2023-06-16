import random

from mainapp.processing.declension_numbers import decl_scores, decl_places
from mainapp.processing.handle_common_rating import get_user_common_rating_info
from mainapp.processing.handle_userprofile import get_scores_rating
from mainapp.processing.handlers.proc_response_obj import remove_tts_symbols


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
    user_place_score, rating_table_print = get_user_common_rating_info(user_id)
    cur_scores = get_scores_rating(user_id, session_id)
    allscores = cur_scores["allscores"]
    sessionscore = cur_scores["sessionscore"]
    user_place = user_place_score[0]

    rating_head = f'🏅🏅🏅Ваш рейтинг🏅🏅🏅\n\nОбщий счёт: {allscores}. За эту игру: {sessionscore}\n\n' \
                  f'{rating_table_print}'

    rating_tts_only, rating_message = get_place_phrase(user_place, allscores)

    if not rating_tts_only:
        rating_tts_only = random.choice(
            [
                f'Сейчас за игру {decl_scores(sessionscore)} sil <[100]>и {decl_scores(allscores)} за всё время.sil <[100]>\n',
                f'Сейчас у тебя {decl_scores(sessionscore)} за игру sil <[100]>и {decl_scores(allscores)} в целом.sil <[100]>\n',
                f'У тебя за игру {decl_scores(sessionscore)} sil <[100]>и всего {decl_scores(allscores)}.sil <[100]>\n',
                f'За игру у тебя {decl_scores(sessionscore)}, sil <[100]>а всего {decl_scores(allscores)}.sil <[100]>\n',
                f'Всего {decl_scores(allscores)}, sil <[100]>а за эту игру {decl_scores(sessionscore)}.sil <[100]>\n'
                ])

    response: dict = {
        'text': remove_tts_symbols(f'{rating_head} \n{rating_message}'),
        'buttons': [
            {'title': 'Да', 'hide': 'true'},
            {'title': 'Нет', 'hide': 'true'}
        ],
        'tts': f'{rating_tts_only}{rating_message}',
        'end_session': 'false'
    }

    # Состояние с предыдущим ответом передаем прозрачно, но добавляем флаг Да/Нет
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


def get_place_phrase(user_place: int, user_scores: int):
    rating_tts_only = ''
    rating_message = ''
    if user_place == 1:
        rating_message += random.choice(
            ["Ты на первом месте! sil <[70]>Молодч+ина! Прод+олжим бить рекорды?",
             "Ты п+ервый в общем рейтинге! Только вперед! sil <[70]>Прод+олжим?",
             "Не поним+аю, как тебе это удалось, sil <[70]>но ты на первом месте! Прод+олжим идти вперёд?",
             "Ты лучший! sil <[70]> Так держать. Соперники не дремлют. sil <[70]>Прод+олжим?"
             ])

    elif user_place == 2:
        rating_message += random.choice(
            ["Ты в призовой тройке, sil <[70]>но не время расслабляться. sil <[70]>Прод+олжим?",
             "Ты втор+ой! Только вперед! sil <[100]>Продолжим?",
             "Ты втор+ой и наступаешь чемпиону на пятки! sil <[100]>Прод+олжим идти вперёд?",
             "Ты втор+ой!sil <[70]> Так держать. sil <[100]>Соперники не дремлют. Прод+олжим?",
             "Ты на втором месте! Я хочу, чтобы ты был лучшим! sil <[100]>Погнали дальше?"
             ])

    elif user_place == 3:
        rating_message += random.choice(
            ["Ты в призовой тройке, sil <[70]>но не время расслабляться. sil <[70]>Прод+олжим?",
             "Ты тр+етий! sil <[70]>Только вперед! sil <[70]>Прод+олжим?",
             "Ты тр+етий и наступаешь чемпиону на пятки! sil <[70]>Продолжим идти вперёд?",
             "Ты тр+етий!sil <[70]> Так держать. sil <[70]>Соперники не дремлют. Прод+олжим?",
             "Ты на тр+етьем месте! sil <[70]>Но я хочу, чтобы ты был лучшим! sil <[70]>Погнали дальше?"
             ])

    elif int(user_scores) != 0:
        rating_tts_only += random.choice(
            [f"Ты на {decl_places(user_place)} месте.sil <[70]>",
             f"Теперь ты на {decl_places(user_place)} месте.sil <[70]>",
             f"И вот ты на {decl_places(user_place)} месте. sil <[70]>",
             f"Сейчас ты на {decl_places(user_place)} месте. sil <[70]>"
             ]
        )

        rating_message += random.choice(
            ['Это весьма хорошо. Продолжим идти вперёд?',
             'Очень неплохо! Предлагаю не останавливаться на достигнутом. Прод+олжим игру?',
             'Уверена, что ты можешь больше. Прод+олжим?',
             'Весьма недурно! sil <[70]>Прод+олжим покорять вершины?',
             'Неплохой темп, но всё ещё впереди. Прод+олжим? ',
             'Уверенный темп! sil <[70]>Поехали дальше?',
             'Я вижу, sil <[70]> ты очень устремленный человек.sil <[70]>Поехали дальше?'
             ]
        )

    else:
        rating_tts_only += random.choice(["У тебя по нулям.",
                                         "У тебя ноль баллов."
                                         ])
        rating_message += random.choice(
            ['Не густо. sil <[70]>Начнём покорять вершины?',
             'Маловато будет. sil <[70]>Прод+олжим игру, чтоб это исправить?',
             'Уверена, что ты можешь на б+ольшее. sil <[70]>Прод+олжим игру, чтоб это исправить?',
             ]
        )

    return rating_tts_only, rating_message
