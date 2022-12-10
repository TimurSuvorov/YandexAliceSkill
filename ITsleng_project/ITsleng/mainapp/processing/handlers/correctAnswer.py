import random
from ..extract_json import get_db_sentences
from .generate_var_buttons import generate_var_buttons


def correctanswer(question_dict):
    # Выбираем случайным образом предложение похвалы
    sentences = get_db_sentences()
    nicesentence = random.choice(sentences["NICEsentence"])

    # Из вопроса-словаря берем сам вопрос и варианты ответов
    question_body = question_dict["sentence"]
    question_variants = question_dict["variants"]

    response: dict = {
            'text': f'{nicesentence} \n{question_body}',
            'tts': f'{nicesentence} Следующий вопрос: {question_body}',
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
