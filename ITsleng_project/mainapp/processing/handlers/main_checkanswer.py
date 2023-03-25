import re

from .iscorrectAnswer import iscorrectanswer
from .correctAnswer import correctanswer
from .stupid_replies import stupid_replies
from .wrongAnswer import incorrectanswer

stupid_answers = [r"^да+", "да уж", "ништяк", "^нет", "^ой", "блин", "ерунда", "^упс", "сама ответь"]


'''
{'question_dict': {'answers': ['таска'],
                   'category': [],
                   'sentence': 'Заведенная или планируемая задача',
                   'variants': ['окиара', 'таска', 'фича']},
 'attempt': 0
}
'''


def checkanswer(command, session_state, user_id, session_id, message_id):

    # Формирование списка вариантов+ответов для проверки вне вариантов
    all_variants = session_state["question_dict"]["answers"] + session_state["question_dict"]["variants"]
    if not re.search("|".join(all_variants).replace("+", ""), command):
        # Берем ранее озвученный вопрос и добавляем фразу
        response_dict = stupid_replies(command, session_state)
        return response_dict

    # Если слово прошло проверку по одному из вариантов
    if iscorrectanswer(command, session_state):
        # Генерируем новый вопрос для создания ответа в формате для случая "успеха пользователя"
        response_dict = correctanswer(command, session_state, user_id, session_id, message_id)
        return response_dict
    else:
        # В случае неверного ответа нам нужен заданный вопрос из session_state
        response_dict = incorrectanswer(command, session_state, user_id, session_id)
        return response_dict



