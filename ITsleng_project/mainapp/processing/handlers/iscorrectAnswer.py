import re


def iscorrectanswer(command, session_state):
    # Из вопроса-словаря, который мы отправили ранее берём ответы.
    # Ищем совпадения вариантов ответа в отправленной команде от пользователя
    answers_list = session_state["question_dict"]["answers"]
    matching = re.search("|".join(answers_list).replace("+", ""), command)
    if matching:
        return True
    return False
