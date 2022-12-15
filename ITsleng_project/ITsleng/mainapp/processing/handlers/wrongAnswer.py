import random

from mainapp.processing.extract_json import get_db_sentences, get_db_sounds
from .generate_question import generate_question, tts_prompt_sound
from .generate_variants_objects import generate_var_buttons, generate_var_string


def incorrectanswer(command, session_state: dict):
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
        question_variants = question_dict["variants"]

        # Удаляем из вариантов, если был назван оттуда. Подставляем другу фразу
        if command in question_variants:
            question_variants.remove(command)
            postsentence = random.choice(["Остались варианты", "Вот что осталось"])

        variants = generate_var_string(question_variants)

        response: dict = {
                'text': f'{mistakesentence} \n{postsentence}:\n{variants.replace("+", "")}',
                'tts': f'{wrongsound}{mistakesentence}.sil <[50]>{postsentence}:sil <[50]> {variants}',
                'buttons': generate_var_buttons(question_variants),
                'end_session': 'False'
        }

    else:
        # Если попыток угадать больше нет. Выбираем случайным образом предложение поругать
        badsentence = random.choice(sentences["BADsentence"])
        postsentence = random.choice(sentences["POSTsentence"])
        # Получаем первый из списка правильный ответ и объяснение
        answer = session_state["question_dict"]["answers"][0]
        question_explanation = session_state["question_dict"]["explanation"]
        # Генерируем сразу новый вопрос и восстанавливаем количество попыток к нему
        question_dict = generate_question()
        attempt = 1
        # Из вопроса-словаря берем сам вопрос для подстановки в ответ
        question_body = question_dict["sentence"]
        # Генерируем кнопки для нового вопроса
        question_variants = question_dict["variants"]
        variants = generate_var_string(question_variants)

        response: dict = {
                'text': f'{badsentence}: {answer.capitalize().replace("+", "")}.\n{question_explanation.replace(" - ", "").replace("+", "")} \nДальше: {question_body} \n{postsentence}:\n{variants.replace("+", "")}',
                'tts': f'{wrongsound}{badsentence}: sil <[50]> {answer}.sil <[70]>{question_explanation} sil <[70]> Дальше: sil <[50]> {tts_prompt_sound(question_body)}. {postsentence}: sil <[50]>{variants}',
                'buttons': generate_var_buttons(question_variants),
                'end_session': 'False'
        }

    return {
        "response": response,
        "session_state": {
            "question_dict": question_dict,
            "attempt": attempt
        }
    }
