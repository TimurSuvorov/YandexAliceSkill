import random

from .generate_question import tts_prompt_sound
from .generate_variants_objects import generate_var_buttons, generate_var_string
from mainapp.processing.db.extract_json import get_db_sentences, get_db_sounds
from ..handle_sessionfile import get_qa_session_sentence


def next_question(session_id) -> dict:
    # Берем новый вопрос для сессии
    question_dict = get_qa_session_sentence(session_id)
    # Из вопроса-словаря берем сам вопрос
    question_body = question_dict["sentence"]
    question_variants = question_dict["variants"][:3]

    # Выбираем фразу про варианты
    sentences = get_db_sentences()
    postsentence = random.choice(sentences["POSTsentence"])

    # Выбираем звуки
    sounds = get_db_sounds()
    nextquestsound = random.choice(sounds["NEXTQUEST"])
    variants = generate_var_string(question_variants)

    response: dict = {
            'text': f'✨{question_body.replace(" - ", "").replace("+", "")}\n{postsentence}:\n{variants.replace("+", "")}',
            'tts': f'{nextquestsound}sil <[5]>{tts_prompt_sound(question_body)}sil <[50]>{postsentence}sil <[70]>{variants}',
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
    }

    analytics = {
        "events": [
            {
                "name": "Новый вопрос",
                "value": {
                    "Вопрос": question_body.replace(" - ", "").replace("+", ""),
                }
            }
        ]
    }

    # Возвращаем сформированный вопрос, а также отдаем в session_state для дальнейшего учёта
    return {
        "response": response,
        "analytics": analytics,
        "session_state": {
            "question_dict": question_dict,
            "attempt": 1
            }
    }
