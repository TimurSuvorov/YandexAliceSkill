import random
import re

from mainapp.processing.db.extract_json import get_db_sentences, get_db_sounds
from .proc_response_obj import generate_var_buttons, generate_var_string, tts_prompt_sound, remove_tts_symbols
from ..db.images import Image
from ..handle_sessionfile import get_qa_session_sentence
from ..handle_userprofile import update_scores


def incorrectanswer(command, session_state, user_id, session_id):

    sentences = get_db_sentences()

    # Выбираем звуки
    sounds = get_db_sounds()
    wrongsound = random.choice(sounds["WRONG"])

    # Если неправильно, но попытка угадать ответ еще есть
    if session_state["attempt"] > 0:
        # Выбираем случайным образом предложение повторить
        mistakesentence = random.choice(sentences["MISTAKEsentence"])
        postsentence = random.choice(sentences["POSTsentence"])
        # Снижаем кол-во попыток
        attempt = session_state["attempt"] - 1
        # Сам вопрос оставляем в session_state
        question_dict = session_state["question_dict"]
        # Генерируем кнопки
        question_variants = question_dict["variants"][:3]

        # Удаляем из вариантов, если был назван оттуда. Подставляем другу фразу
        for variant in question_variants:
            if re.search(variant.replace("+", ""), command):
                question_variants.remove(variant)
                postsentence = random.choice(
                    [
                        "Остались варианты",
                        "Вот что осталось",
                        "Осталось два варианта",
                        "Но уже вариантов поменьше",
                     ]
                )

        variants = generate_var_string(question_variants)

        response: dict = {
                'text': remove_tts_symbols(f'{mistakesentence}\n{postsentence}:\n{variants}'),
                'tts': f'{wrongsound}{mistakesentence}.sil <[50]>{postsentence}:sil <[50]> {variants}',
                'card': {
                    'type': 'BigImage',
                    'image_id': Image.WRONG_ANSWER_1.id,
                    'title': remove_tts_symbols(random.choice(sentences["WRONGsentence"])),
                    'description': remove_tts_symbols(f'{postsentence}:\n{variants}')
                },
                'buttons': generate_var_buttons(question_variants),
                'end_session': 'False'
        }

        analytics = {
            "events": [
                {
                    "name": "Неверный ответ 1",
                    "value": {
                        "Вопрос": session_state["question_dict"]["sentence"],
                        "Ответ": command
                    }
                }
            ]
        }

    else:
        # Если попыток угадать больше нет. Выбираем случайным образом предложение поругать
        badsentence = random.choice(sentences["BADsentence"])
        postsentence = random.choice(sentences["POSTsentence"])
        letsnext = random.choice(sentences["LETSNEXTsentence"])
        questionsound = random.choice(sounds["QUESTION"])
        # Получаем первый из списка правильный ответ и объяснение
        answer = session_state["question_dict"]["answers"][0]
        question_explanation = session_state["question_dict"]["explanation"]
        # Берем новый вопрос для сессии и восстанавливаем количество попыток к нему
        question_dict = get_qa_session_sentence(session_id)
        attempt = 1
        # Из вопроса-словаря берем сам вопрос для подстановки в ответ
        question_body = question_dict["sentence"]
        # Генерируем кнопки для нового вопроса
        question_variants = question_dict["variants"][:3]
        variants = generate_var_string(question_variants)

        # Подсчёт рейтинга и его отображение
        score = 0
        cur_scores = update_scores(user_id, session_id, score)
        allscores = cur_scores["allscores"]
        sessionscore = cur_scores["sessionscore"]
        cur_rating = f'\n\n🏅Ваш рейтинг:\nОбщий: {allscores}\nВ этой игре: {sessionscore}'

        response: dict = {
                'text': remove_tts_symbols(f'{badsentence}: {answer}.\n{question_explanation} \n{letsnext}.\n✨{question_body} \n{postsentence}:\n{variants}{cur_rating}'),
                'tts': f'{wrongsound}{badsentence}: sil <[50]> {answer}.sil <[70]>{question_explanation} sil <[100]> {letsnext}: sil <[100]> {questionsound}{tts_prompt_sound(question_body)}. {postsentence}: sil <[50]>{variants}',
                'card': {
                    'type': 'BigImage',
                    'image_id': Image.WRONG_ANSWER_2.id,
                    'title': remove_tts_symbols(random.choice(sentences["WRONGsentence"])),
                    'description': remove_tts_symbols(f'Ответ: {answer}.\n{question_explanation}\n\n {letsnext}.\n✨{question_body} \n{postsentence}:\n{variants}{cur_rating}')
                },
                'buttons': generate_var_buttons(question_variants),
                'end_session': 'False'
        }
        analytics = {
            "events": [
                {
                    "name": "Неверный ответ 2",
                    "value": {
                        "Вопрос": session_state["question_dict"]["sentence"],
                        "Ответ": command
                    }
                },
                {
                    "name": "Новый вопрос",
                    "value": {
                        "Вопрос": remove_tts_symbols(question_body),
                    }
                }
            ]
        }

    return {
        "response": response,
        "analytics": analytics,
        "session_state": {
            "question_dict": question_dict,
            "attempt": attempt
        }
    }
