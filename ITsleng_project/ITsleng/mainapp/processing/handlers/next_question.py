import random

from .generate_question import tts_prompt_sound
from .generate_variants_objects import generate_var_buttons, generate_var_string
from mainapp.processing.extract_json import get_db_sentences, get_db_sounds


def next_question(question_dict: dict) -> dict:
    # Из вопроса-словаря берем сам вопрос
    question_body = question_dict["sentence"]
    question_variants = question_dict["variants"]

    # Выбираем фразу про варианты
    sentences = get_db_sentences()
    postsentence = random.choice(sentences["POSTsentence"])

    # Выбираем звуки
    sounds = get_db_sounds()
    nextquestsound = random.choice(sounds["NEXTQUEST"])

    response: dict = {
            'text': f'{question_body}.\n{postsentence}:\n{generate_var_string(question_variants)}',
            'tts': f'{nextquestsound}sil <[5]>{tts_prompt_sound(question_body)}sil <[50]>{postsentence}sil <[70]>{generate_var_string(question_variants)}',
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
