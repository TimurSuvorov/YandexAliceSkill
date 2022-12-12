from .generate_question import generate_question
from .generate_variants_objects import generate_var_buttons
from .next_question import next_question


def dontknow(session_state):
    # Если пустой по каким-либо причинам, Алиса прикинится валенком
    if not session_state.get("question_dict"):
        response: dict = {
            'text': f'Ой, а я уже забыла. ¯\_(ツ)_/¯ . Давай я лучше загадаюю тебе слово?',
            'tts': f'Ой, а я уже забыла. Давай начнём сначала',
            'buttons': [{'title': 'Дальше', 'hide': 'true'}],
            'end_session': 'False'
        }
        sessionstate = {}
    # Если сообщение было сервисным, то генерируем новый вопрос
    elif session_state.get("service"):
        question_dict = generate_question()
        response_dict = next_question(question_dict)
        response = response_dict["response"]
        sessionstate = response_dict["session_state"]
    else:
        # Получаем первый из списка правильный ответ
        answer = session_state["question_dict"]["answers"][0]
        # Генерируем сразу новый вопрос и восстанавливаем количество попыток к нему
        question_dict = generate_question()
        # Из вопроса-словаря берем сам вопрос для подстановки в ответ
        question_body = question_dict["sentence"]
        # Генерируем кнопки для нового вопроса
        question_variants = question_dict["variants"]
        response: dict = {
            'text': f'Правильный ответ: {answer.capitalize()}. \nСледующий вопрос: {question_body}',
            'tts': f'Правильный ответ: {answer}. Следующий вопрос: {question_body}',
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
        }

        sessionstate = {
            "question_dict": question_dict,
            "attempt": 1
        }

    return {
        "response": response,
        "session_state": sessionstate
    }