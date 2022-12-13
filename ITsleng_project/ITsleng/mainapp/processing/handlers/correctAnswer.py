import random

from .generate_question import tts_prompt_sound
from ..extract_json import get_db_sentences, get_db_sounds
from .generate_variants_objects import generate_var_buttons, generate_var_string


def correctanswer(question_dict):
    # Выбираем случайным образом предложение похвалы и "вариантов"
    sentences = get_db_sentences()
    nicesentence = random.choice(sentences["NICEsentence"])
    postsentence = random.choice(sentences["POSTsentence"])

    # Выбираем звуки
    sounds = get_db_sounds()
    correctsound = random.choice(sounds["CORRECT"])
    nextquestsound = random.choice(sounds["NEXTQUEST"])

    # Из вопроса-словаря берем сам вопрос и варианты ответов
    question_body = question_dict["sentence"]
    question_variants = question_dict["variants"]

    response: dict = {
            'text': f'{nicesentence}\n{question_body}.\n{postsentence}:\n{generate_var_string(question_variants)}',
            'tts': f'{correctsound}sil <[5]>{nicesentence}sil <[50]>{tts_prompt_sound(question_body)}.{postsentence}:sil <[50]>{generate_var_string(question_variants)}',
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
    }

    # Возвращаем сформированный вопрос, а также отдаем в session_state для дальнейшего учёта
    return {
        "response": response,
        "session_state": {
            "question_dict": question_dict,
            "attempt": 1
        }
    }
