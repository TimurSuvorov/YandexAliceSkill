import random

from .generate_question import tts_prompt_sound
from ..extract_json import get_db_sentences, get_db_sounds
from .generate_variants_objects import generate_var_buttons, generate_var_string


def correctanswer(question_dict, command, session_state):
    # Выбираем случайным образом предложение похвалы и "вариантов"
    sentences = get_db_sentences()
    nicesentence = random.choice(sentences["NICEsentence"])
    postsentence = random.choice(sentences["POSTsentence"])

    # Проверяем на схожесть слова
    rightanswer = session_state["question_dict"]["answers"][0].replace("+", "")
    if rightanswer != command:  # FIXIT check by regex
        nicesentence = random.choice(["Пишется по-другому, но я поняла. Верно!",
                                      "Нечетко говоришь, но, похоже, ты прав!",
                                      "Было непросто понять твои слова, но ты прав!"
                                      ]
                                     )

    # Выбираем звуки
    sounds = get_db_sounds()
    correctsound = random.choice(sounds["CORRECT"])

    # Из вопроса-словаря берем сам вопрос и варианты ответов
    question_body = question_dict["sentence"]
    question_variants = question_dict["variants"]
    variants = generate_var_string(question_variants)
    response: dict = {
            'text': f'{nicesentence}\n✨{question_body.replace(" - ", "").replace("+", "")} \n{postsentence}:\n{variants.replace("+", "")}',
            'tts': f'{correctsound}sil <[50]>{nicesentence}sil <[100]>{tts_prompt_sound(question_body)}sil <[50]>.{postsentence}:sil <[50]>{variants}',
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
    }
    print("From correctanswer")
    # Возвращаем сформированный вопрос, а также отдаем в session_state для дальнейшего учёта
    return {
        "response": response,
        "analytics": {
            "events": [
                {
                    "name": "Верный ответ",
                    "value": {
                        "Вопрос": session_state["question_dict"]["sentence"],
                        "Ответ": command
                        }
                },
                {
                    "name": "Новый вопрос",
                    "value": {
                        "Вопрос": question_body,
                    }
                },
            ]
        },
        "session_state": {
            "question_dict": question_dict,
            "attempt": 1
        }
    }
