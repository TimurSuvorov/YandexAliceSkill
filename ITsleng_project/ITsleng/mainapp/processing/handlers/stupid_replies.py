import random

from mainapp.processing.extract_json import get_db_sentences
from mainapp.processing.handlers.generate_question import tts_prompt_sound
from mainapp.processing.handlers.generate_variants_objects import generate_var_string, generate_var_buttons


def stupid_replies(command, session_state):
    sentences = get_db_sentences()
    postsentence = random.choice(sentences["POSTsentence"])

    question_dict = session_state["question_dict"]
    question_body = question_dict["sentence"]
    question_variants = question_dict["variants"]
    variants = generate_var_string(question_variants)

    stupid_phrases = ["Вр+оде, умный, а говоришь не впоп+ад. Дав+ай ещё раз.",
                      "Неож+иданный ответ. Попробуй сказать поразборчивей."
                      ]
    stupid_phrase = random.choice(stupid_phrases)

    response: dict = {
        'text': f'{stupid_phrase.replace(" - ", "").replace("+", "")}\n✨{question_body.replace(" - ", "").replace("+", "")}.\n{postsentence}:\n {variants.replace("+", "")}',
        'tts': f'{stupid_phrase}sil <[100]> {tts_prompt_sound(question_body)}sil <[50]> {postsentence}sil <[50]>{variants}',
        'buttons': generate_var_buttons(question_variants),
        'end_session': 'False'
    }

    analytics = {
        "events": [
            {
                "name": "Валенок с вопросом",
                "value": {
                    "Вопрос": session_state['question_dict']['sentence'],
                    "Ответ": command
                }
            },
        ]
    }

    return {
        "response": response,
        "analytics": analytics,
        "session_state": session_state
    }