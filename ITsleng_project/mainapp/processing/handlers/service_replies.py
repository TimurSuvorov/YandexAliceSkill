import random

from mainapp.processing.declension_numbers import decl_scores, decl_places
from mainapp.processing.db.extract_json import get_db_sentences, get_db_sounds
from mainapp.processing.handle_common_rating import get_user_common_rating_info
from mainapp.processing.handle_sessionfile import create_session_file
from mainapp.processing.handle_userprofile import check_old_user
from mainapp.processing.handlers.proc_response_obj import remove_tts_symbols, tts_prompt_sound


def hi_replies(user_id: str, session_id: str) -> dict:
    """Функция формирует приветственное сообщение.

     Условия:
        - новый пользователь;
        - старый пользователь:
            -- нулевой рейтинг;
            -- ненулевой рейтинг и место;
    Добавление в ответ флага AppMetrics: "Запуск навыка"

    """
    # Создание файла с вопросами для сессии, возвращает содержимое файла db_sentences.json
    sentences = create_session_file(session_id)

    # Выбираем звуки
    sounds = get_db_sounds()
    startsound = random.choice(sounds["START"])

    # Формирование фразы приветствия для нового/старого пользователя
    rating_text = ''
    rating_tts = ''

    if check_old_user(user_id):
        # Получение рейтинга и места
        user_place_score = get_user_common_rating_info(user_id)[0]
        user_place = user_place_score[0]
        user_scores = user_place_score[1]

        hi_text = random.choice(sentences["HIsentence_olduser"])

        rating_phr1_text_tts = random.choice(
            [
                '\n\n🏅 Посм+отрим, сколько в твоей копилке 🏅 \n',
                '\n\n🏅 Посм+отрим на твой рейтинг 🏅 \n',
                '\n\n🏅 Пару слов про твой рейтинг 🏅 \n',
                '\n\n🏅 Интер+есно взглянуть на твой рейтинг 🏅 \n',
            ]
        )

        # Если рейтинг ненулевой, то значит сообщаем ему о текущей ситуации.
        if int(user_scores) != 0:
            rating_phr2_text = random.choice(
                [
                    f'Ты набрал {decl_scores(user_scores)} за всё время и находишься на {user_place} месте.\n',
                    f'Сейчас у тебя {decl_scores(user_scores)}. В общем зачёте ты на {user_place} месте.\n',
                    f'У тебя всего {decl_scores(user_scores)} и ты на {user_place} месте.\n',
                    f'Ты набрал всего {decl_scores(user_scores)} и находишься на {user_place} месте.\n',
                    f'В твоей коп+илке {decl_scores(user_scores)}, ты на {user_place} месте в общем зачёте.\n',
                ]
            )

            rating_phr2_tts = random.choice(
                [
                    f'Ты набрал {decl_scores(user_scores)} за всё время и находишься на {decl_places(user_place)} месте.\n',
                    f'Сейчас у тебя {decl_scores(user_scores)}. В общем зачёте ты на {decl_places(user_place)} месте.\n',
                    f'У тебя всего {decl_scores(user_scores)} и ты на {decl_places(user_place)} месте.\n',
                    f'Ты набрал всего {decl_scores(user_scores)} и находишься на {decl_places(user_place)} месте.\n',
                    f'В твоей коп+илке {decl_scores(user_scores)}, ты на {decl_places(user_place)} месте в общем зачёте.\n',
                ]
            )

            rating_phr3_text_tts = random.choice(
                [
                    'Это весьма хорошо.sil <[100]> \n',
                    'Очень неплохо! Предлагаю не останавливаться на достигнутом.sil <[100]> \n',
                    'Уверена, что ты можешь больше.sil <[100]> \n',
                    'Весьма недурно!sil <[100]> \n',
                    'Неплохой темп, но всё ещё впереди.sil <[100]> \n',
                    'Но ты н+е останавливайся.sil <[100]> \n',
                    'Уверена, что ты можешь на б+ольшее.sil <[100]> \n',
                 ]
            )

            rating_phr4_text_tts = random.choice(
                [
                    "Начинаем?",
                    "Прод+олжим игру?",
                    "Поехали?",
                    "Продолжим покорять вершины?",
                    "Продолжим?",
                ]
            )

            rating_text = rating_phr1_text_tts + rating_phr2_text + rating_phr3_text_tts + rating_phr4_text_tts
            rating_tts = rating_phr1_text_tts + rating_phr2_tts + rating_phr3_text_tts + rating_phr4_text_tts

        # Если у пользователя ноль баллов
        else:
            rating_phr1_text_tts = random.choice(
                [
                    'У тебя по нулям. ',
                    'У тебя ноль баллов. ',
                    'Не могу понять почему, но у тебя ноль баллов. '
                ]
            )
            rating_phr2_text_tts = random.choice(
                [
                    'Не густо. \n',
                    'Маловато будет. \n',
                    'Уверена, что ты можешь на б+ольшее. \n',
                ]
            )

            rating_phr3_text_tts = random.choice(
                [
                    "Начнём покорять вершины?",
                    "Прод+олжим игру, чтоб это исправить?",
                    "Прод+олжим игру, чтоб это исправить?",
                ]
            )

            rating_text = rating_phr1_text_tts + rating_phr2_text_tts + rating_phr3_text_tts
            rating_tts = rating_phr1_text_tts + rating_phr2_text_tts + rating_phr3_text_tts

    # Если пользователь зашёл в первый раз
    else:
        hi_text = sentences["HIsentence_newuser"]

    response: dict = {
            'text': remove_tts_symbols(f'{hi_text}{rating_text}'),
            'buttons': [
                {'title': 'Правила', 'hide': 'true'},
                {'title': 'Что ты умеешь?', 'hide': 'true'},
                {'title': 'Играть!', 'hide': 'true'},
                {'title': 'Выйти', 'hide': 'true'}
            ],
            'tts': f'{startsound}{hi_text}{rating_tts}',
            "card": {
                "type": "BigImage",
                "image_id": "997614/c45c09816466152b9aca",
                "title": "  «ITшник в офисе»",
                "description": remove_tts_symbols(f'{hi_text}{rating_text}'),
                "button": {
                    "text": "Играть"
                }
            },
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
    """Функция формирует ответ прощания при явном выходе из навыка.

    Добавление в ответ флага AppMetrics: "Выход из навыка"
    """
    sentences = get_db_sentences()
    bye_text = random.choice(sentences["BYEsentence"])

    # Выбираем звуки
    sounds = get_db_sounds()
    byesound = random.choice(sounds["BYE"])

    response: dict = {
            'text': remove_tts_symbols(bye_text),
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
    """Функция формирует ответ с правилами и предлагает продолжить в разных формах.

    Зависимость от:
        - запрос в начале игры;
        - запрос во время игры;

    В качестве аргумента функция принимает предыдущее состояние и отдает его прозрачно в ответ (пользователь
    продолжает с места во время запроса правил), но уже с флагами
    сервисного ответа и закрытого вопроса.
    Добавление в ответ флага AppMetrics: "Запрос 'Правила'."

    """
    sentences: dict = get_db_sentences()
    rules_text = sentences["RULES"]
    # Если функция вызвана во время вопроса, когда присутствует session_state["question_dict"]["answers"]
    if session_state.get('question_dict', {}).get('answers'):
        rules_text += 'Прод+олжим?'
    else:
        rules_text += 'Ну чт+о, начин+аем?'

    response: dict = {
            'text': remove_tts_symbols(rules_text).replace("<...>", '🎶'),
            'buttons': [
                {'title': 'Что ты умеешь?', 'hide': 'true'},
                {'title': 'Играть!', 'hide': 'true'},
                {'title': 'Выйти', 'hide': 'true'}
            ],
            'tts': tts_prompt_sound(rules_text),
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
    """Функция формирует ответ с содержанием, что умеет навык, и предлагает продолжить в разных формах в зависимост от:
        - запрос в начале игры;
        - запрос во время игры;

    В качестве аргумента функция принимает предыдущее состояние и отдает его прозрачно в ответ (пользователь
    продолжает с места во время запроса), но уже с флагами
    сервисного ответа и закрытого вопроса.
    Добавление в ответ флага AppMetrics: "Запрос 'Что умеешь?'."

    """
    sentences = get_db_sentences()
    about_text = sentences["ABOUT"]

    # Если функция вызвана во время вопроса, когда присутствует session_state["question_dict"]["answers"]
    if session_state.get('question_dict', {}).get('answers'):
        about_text += 'Прод+олжим?'
    else:
        about_text += 'Начин+аем?'

    response: dict = {
            'text': remove_tts_symbols(about_text),
            'buttons': [
                {'title': 'Правила', 'hide': 'true'},
                {'title': 'Играть!', 'hide': 'true'},
                {'title': 'Выйти', 'hide': 'true'}
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
