import random

from mainapp.processing.extract_json import get_db_sentences
from .generate_question import generate_question
from .generate_var_buttons import generate_var_buttons


def incorrectanswer(session_state: dict):
    sentences = get_db_sentences()

    # Если неправильно, но попытка угадать ответ еще есть
    if session_state["attempt"] > 0:
        # Выбираем случайным образом предложение повторить
        mistakesentence = random.choice(sentences["MISTAKEsentence"])
        # Снижаем кол-во попыток
        attempt = session_state["attempt"] - 1
        # Сам вопрос оставляем в session_state
        question_dict = session_state["question_dict"]
        # Генерируем кнопки
        question_variants = question_dict["variants"]

        response: dict = {
                'text': f'{mistakesentence}',
                'tts': f'{mistakesentence}',
                'buttons': generate_var_buttons(question_variants),
                'end_session': 'False'
        }

    else:
        # Если попыток угадать больше нет. Выбираем случайным образом предложение поругать
        badsentence = random.choice(sentences["BADsentence"])
        # Получаем первый из списка правильный ответ
        answer = session_state["question_dict"]["answers"][0]
        # Генерируем сразу новый вопрос и восстанавливаем количество попыток к нему
        question_dict = generate_question()
        attempt = 1
        # Из вопроса-словаря берем сам вопрос для подстановки в ответ
        question_body = question_dict["sentence"]
        # Генерируем кнопки для нового вопроса
        question_variants = question_dict["variants"]
        response: dict = {
                'text': f'{badsentence}: {answer}. Следующий вопрос: {question_body}',
                'tts': f'{badsentence}: {answer}. Следующий вопрос: {question_body}',
                'buttons': generate_var_buttons(question_variants),
                'end_session': 'False'
        }

    return {
        "response": response,
        "sessionstate": {
            "question_dict": question_dict,
            "attempt": attempt
        }
    }
