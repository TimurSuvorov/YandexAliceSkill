from .generate_question import generate_question
from .next_question import next_question
from .iscorrectAnswer import iscorrectanswer
from .correctAnswer import correctanswer
from .wrongAnswer import incorrectanswer

'''
{'question_dict': {'answers': ['таска'],
                   'category': [],
                   'sentence': 'Заведенная или планируемая задача',
                   'variants': ['окиара', 'таска', 'фича']},
 'attempt': 0
}
'''

def checkanswer(command, session_state: dict):
    # Если нет предыдущего вопроса (session_state={"question_dict": {}})
    # или сообщение было сервисное (session_state={"service": 11})
    if not session_state.get("question_dict") or \
            session_state.get("service"):
        # Генерируем новый случайный вопрос-словарь из db_sentences.json
        question_dict = generate_question()
        # Передаем его для создания ответа в формате
        response_dict = next_question(question_dict)
        return response_dict

    if iscorrectanswer(command, session_state):
        # Генерируем новый случайный вопрос-словарь из db_sentences.json
        question_dict = generate_question()
        # Передаем его для создания ответа в формате для случая "успеха пользователя"
        response_dict = correctanswer(question_dict)
        return response_dict
    else:
        # В случае неверного ответа нам нужен заданный вопрос из session_state
        response_dict = incorrectanswer(command, session_state)
        return response_dict



