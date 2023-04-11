import random

from mainapp.processing.declension_numbers import decl_scores
from mainapp.processing.db.extract_json import get_db_sentences, get_db_sounds
from mainapp.processing.handle_sessionfile import create_session_file
from mainapp.processing.handle_userprofile import check_old_user, get_scores_rating


def hi_replies(user_id: str, session_id: str) -> dict:
    """
    Функция формирует приветственное сообщение в зависимости от:
        - новый пользователь;
        - старый пользователь:
            -- нулевой рейтинг;
            -- ненулевой рейтинг;
    Добавление в ответ флага AppMetrics: "Запуск навыка"
    """
    # Создание файла с вопросами для сессии, возвращает содержимое файла db_sentences.json
    sentences = create_session_file(session_id)
    rating_message = ''
    # Формирование фразы приветствия для нового/старого пользователя
    if check_old_user(user_id):
        hi_text = sentences["HIsentence_olduser"]["text"]
        hi_tts = sentences["HIsentence_olduser"]["tts"]
        rating_message += random.choice(['🏅 Пару слов про твой рейтинг 🏅\n',
                                         '🏅 Посмотрим на твой рейтинг 🏅\n',
                                         '🏅 Пару слов про твой рейтинг 🏅\n'])
        # Получение рейтинга из профайла пользователя общий и за сессию
        cur_scores = get_scores_rating(user_id, session_id)
        allscores = cur_scores["allscores"]

        # Если рейтинг ненулевой, то значит сообщаем ему о текущей ситуации.
        # Функция decl_scores() изменяет склонение в зависимости от числа.
        if int(allscores) != 0:
            rating_message += random.choice(
                [f'Ты набрал {decl_scores(allscores)} за всё время.\n',
                 f'Сейчас у тебя {decl_scores(allscores)}.\n',
                 f'У тебя всего {decl_scores(allscores)}.\n',
                 f'Ты набрал всего {decl_scores(allscores)}.\n'
                 ]
            )

            rating_message += random.choice(
                ['Это весьма хорошо. Начинаем?',
                 'Очень неплохо! Предлагаю не останавливаться на достигнутом. Продолжим игру? ',
                 'Уверена, что ты можешь больше. Поехали?',
                 'Весьма недурно! -  Продолжим покорять вершины? ',
                 'Неплохой темп, но всё ещё впереди. Продолжим? ',
                 'Но ты не останавливайся. Продолжим? '
                 ]
                                            )
        # Если у пользователя ноль баллов
        else:
            rating_message += random.choice(
                ['У тебя по нулям. ',
                 'У тебя ноль баллов. ',
                 'Не могу понять почему, но у тебя ноль баллов. '
                 ]
            )
            rating_message += random.choice(
                ['Не густо. Начнём покорять вершины? ',
                 'Маловато будет. Продолжим игру, чтоб это исправить? ',
                 'Уверена, что ты можешь на б+ольшее. Продолжим игру, чтоб это исправить? ',
                ]
            )
    # Если пользователь зашёл в первый раз
    else:
        hi_text = sentences["HIsentence_newuser"]["text"]
        hi_tts = sentences["HIsentence_newuser"]["tts"]

    # Выбираем звуки
    sounds = get_db_sounds()
    startsound = random.choice(sounds["START"])

    response: dict = {
            'text': f'{hi_text} {rating_message}'.replace(" - ", "").replace("+", ""),
            'buttons': [
                {'title': 'Правила', 'hide': 'true'},
                {'title': 'Что ты умеешь?', 'hide': 'true'}
            ],
            'tts': f'{startsound}{hi_tts} {rating_message}',
            'end_session': 'false'
    }
    sessionstate = {'service': 11, 'yesno_type': 10}  # флаги сервисного ответа и закрытого вопроса
    analytics = {
            "events": [
                {
                    "name": "Запуск навыка",
                },
            ]
        }

    return {
        "response": response,
        "analytics": analytics,
        "session_state": sessionstate,
    }


def bye_replies(session_state: dict, session_id: str):
    """
    Функция формирует ответ прощания при явном выходе из навыка.
    Добавление в ответ флага AppMetrics: "Выход из навыка"
    """
    sentences = get_db_sentences()
    bye_text = random.choice(sentences["BYEsentence"])

    # Выбираем звуки
    sounds = get_db_sounds()
    byesound = random.choice(sounds["BYE"])

    response: dict = {
            'text': bye_text,
            'tts': f'{bye_text} {byesound}',
            'end_session': 'True'
    }

    return {
        "response": response,
        "analytics": {
            "events": [
                {
                    "name": "Выход из навыка",
                },
            ]
        },
        "session_state": session_state
    }


def rules_replies(session_state: dict) -> dict:
    """
    Функция формирует ответ с правилами и предлагает продолжить в разных формах в зависимост от:
        - запрос в начале игры;
        - запрос во время игры;
    В качестве аргумента функция принимает предыдущее состояние и отдает его прозрачно в ответ (пользователь
    продолжает с места во время запроса правил), но уже с флагами
    сервисного ответа и закрытого вопроса.
    Добавление в ответ флага AppMetrics: "Запрос 'Правила'"
    """
    sentences = get_db_sentences()
    rules_text = sentences["RULES"]["text"]
    rules_tts = sentences["RULES"]["tts"]
    # Если функция вызвана во время вопроса, когда присутствует session_state["question_dict"]["answers"]
    if session_state.get('question_dict', {}).get('answers'):
        rules_text += 'Продолжим?'
        rules_tts += 'Прод+олжим?'
    else:
        rules_text += 'Ну что, начинаем?'
        rules_tts += 'Ну чт+о, начин+аем?'

    response: dict = {
            'text': rules_text,
            'buttons': [
                {'title': 'Что ты умеешь?', 'hide': 'true'}
            ],
            'tts': rules_tts,
            'end_session': 'false'
    }

    # Состояние с предыдущем ответом передаем прозрачно, но добавляем сервисный флаг
    sessionstate = session_state
    sessionstate["yesno_type"] = 10
    sessionstate["service"] = 11

    analytics = {
            "events": [
                {
                    "name": "Запрос 'Правила'",
                },
            ]
        }

    return {
        "response": response,
        "analytics": analytics,
        "session_state": sessionstate
    }


def about_replies(session_state: dict) -> dict:
    """
    Функция формирует ответ с содержанием, что умеет навык, и предлагает продолжить в разных формах в зависимост от:
        - запрос в начале игры;
        - запрос во время игры;
    В качестве аргумента функция принимает предыдущее состояние и отдает его прозрачно в ответ (пользователь
    продолжает с места во время запроса), но уже с флагами
    сервисного ответа и закрытого вопроса.
    Добавление в ответ флага AppMetrics: "Запрос 'Что умеешь?'"
    """
    sentences = get_db_sentences()
    about_text = sentences["ABOUT"]

    # Если функция вызвана во время вопроса, когда присутствует session_state["question_dict"]["answers"]
    if session_state.get('question_dict', {}).get('answers'):
        about_text += 'Прод+олжим?'
    else:
        about_text += 'Начин+аем?'

    response: dict = {
            'text': about_text.replace(" - ", "").replace("+", ""),
            'buttons': [
                {'title': 'Правила', 'hide': 'true'}
            ],
            'tts': about_text,
            'end_session': 'false'
    }

    # Состояние с предыдущем ответом передаем прозрачно, но добавляем сервисный флаг
    sessionstate = session_state
    sessionstate["yesno_type"] = 10
    sessionstate["service"] = 11

    analytics = {
            "events": [
                {
                    "name": "Запрос 'Что умеешь?'",
                },
            ]
        }

    return {
        "response": response,
        "analytics": analytics,
        "session_state": sessionstate
    }