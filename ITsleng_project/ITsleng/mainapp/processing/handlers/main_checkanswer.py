from .generate_question import generate_question
from .next_question import next_question
from .iscorrectanswer import iscorrectanswer
from .correctAnswer import correctanswer
from .incorrectAnswer import incorrectanswer


def checkanswer(command, session_state: dict):
    # Если нет предыдущего вопроса (session_state={"question_dict": {}} )
    if not session_state.get("question_dict"):
        # Генерируем новый случайный вопрос-словарь из db_sentences.json
        question_dict = generate_question()
        # Передаем его для создания ответа в формате
        response_dict = next_question(question_dict)
        return response_dict

    if iscorrectanswer(command, session_state):
        # Генерируем новый случайный вопрос-словарь из db_sentences.json
        question_dict = generate_question()
        # Передаем его для создания ответа в формате ждя случая успеха пользователя
        response_dict = correctanswer(question_dict)
        return response_dict
    else:
        response_dict = incorrectanswer(session_state)
        return response_dict



