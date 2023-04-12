import re


def iscorrectanswer(command: str, session_state: dict) -> bool:
    """
    Функция проверяет ответ пользователя на соответствие правильному из списка вариантов
    """
    # Из вопроса-словаря, который мы отправили ранее берём ответы.
    # Ищем совпадения вариантов ответа в отправленной команде от пользователя
    answers_list: list = session_state["question_dict"]["answers"]
    matching = re.search("|".join(answers_list).replace("+", ""), command)
    if matching:
        return True
    return False
