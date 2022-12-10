from .generate_var_buttons import generate_var_buttons

def next_question(question_dict: dict) -> dict:

    # Из вопроса-словаря берем сам вопрос
    question_body = question_dict["sentence"]
    question_variants = question_dict["variants"]

    response: dict = {
            'text': question_body,
            'tts': question_body,
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
    }

    # Возвращаем сформированный вопрос, а также отдаем в session_state для дальнейшего учёта
    return {
        "response": response,
        "sessionstate": {
            "question_dict": question_dict,
            "attempt": 1
            }
    }
