import random

from .generate_question import tts_prompt_sound
from ..extract_json import get_db_sentences, get_db_sounds
from .generate_variants_objects import generate_var_buttons, generate_var_string
from ..handle_sessionfile import get_qa_session_sentence
from ..handle_userprofile import update_scores


def correctanswer(command, session_state, user_id, session_id):
    # Берем новый вопрос для сессии
    question_dict = get_qa_session_sentence(session_id)
    # Выбираем случайным образом предложение похвалы и "вариантов"
    sentences = get_db_sentences()
    nicesentence = random.choice(sentences["NICEsentence"])
    postsentence = random.choice(sentences["POSTsentence"])
    letsnext = random.choice(sentences["LETSNEXTsentence"])

    # Проверяем на схожесть слова
    rightanswer = session_state["question_dict"]["answers"][0].replace("+", "")
    if rightanswer != command:  # FIXIT check by regex
        nicesentence = random.choice(["Пишется по-другому, но я поняла. Верно!",
                                      "Нечетко говоришь, но, похоже, ты прав!",
                                      "Было непросто понять твои слова, но ты прав!",
                                      "Я тебя поняла! Верно!"
                                      ]
                                     )

    # Выбираем звуки
    sounds = get_db_sounds()
    correctsound = random.choice(sounds["CORRECT"])

    # Из вопроса-словаря берем сам вопрос и варианты ответов
    question_body = question_dict["sentence"]
    question_variants = question_dict["variants"]
    variants = generate_var_string(question_variants)

    # Показывать или нет объяснение при верном ответе
    question_explanation = ""
    if random.choice([True, False, False]):
        question_explanation = session_state["question_dict"]["explanation"]
        question_explanation = f'Ответ: {rightanswer}. -  {question_explanation}'

    # Подсчёт рейтинга и его отображение
    score = session_state["attempt"] + 1
    cur_scores = update_scores(user_id, session_id, score)
    cur_rating = f'\n\n🏅Ваш рейтинг:\nОбщий: {cur_scores[0]}\nТекущий: {cur_scores[1]}'

    response: dict = {
            'text': f'{nicesentence} {question_explanation.replace(" - ", "").replace("+", "")} {letsnext}.\n✨{question_body.replace(" - ", "").replace("+", "")} \n{postsentence}:\n{variants.replace("+", "")}{cur_rating}',
            'tts': f'{correctsound}sil <[50]>{nicesentence}{question_explanation} sil <[100]> {letsnext}sil <[100]>{tts_prompt_sound(question_body)}sil <[50]>.{postsentence}:sil <[50]>{variants}',
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
