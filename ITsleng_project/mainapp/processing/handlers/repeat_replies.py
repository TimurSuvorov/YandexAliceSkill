import random

from .proc_response_obj import generate_var_buttons, generate_var_string, tts_prompt_sound, remove_tts_symbols
from mainapp.processing.db.extract_json import get_db_sentences


def repeat_replies(session_state: dict) -> dict:
    """
    Функция формирует ответ на запрос повторения от пользователя в зависимости от:
        - во время игры (вопрос уже был задан ранее);
        - в начале игры (пользователь ещё не слышал вопроса);
    Если был вопрос до этого, то мы получаем все его компоненты и формируем соответствующий ответ с дополнительными
    фразами.
    В качестве аргумента функция принимает предыдущее состояние и передает его прозрачно.
    Добавление в ответ флага AppMetrics: "Повторить" и параметры.
    """

    # Если пустой по каким-либо причинам, Алиса прикинится валенком
    if not session_state.get("question_dict"):
        response: dict = {
            'text': f'Мы ещё не начали, а ты уже просишь повторить. Давай уже начнём? Но если тебе нужна помощь, скажи "Правила" или "Помоги"',
            'tts': f'Мы ещё не начали, а ты уже просишь повторить. Давай уже начнём? Но если тебе нужна помощь, скажи "Правила" или "Помоги"',
            'buttons': [{'title': 'Начнём', 'hide': 'true'},
                        {'title': 'Правила', 'hide': 'true'},
                        {'title': 'Что ты умеешь?', 'hide': 'true'}],
            'end_session': 'False'
        }
        session_state = {}
    else:
        sentences = get_db_sentences()
        postsentence = random.choice(sentences["POSTsentence"])
        question_dict = session_state["question_dict"]
        question_body = question_dict["sentence"]
        question_variants: list = question_dict["variants"][:3]
        variants = generate_var_string(question_variants)
        response: dict = {
            'text': remove_tts_symbols(f'✨{question_body}\n{postsentence}:\n {variants}'),
            'tts': f'Конечно!sil <[100]> {tts_prompt_sound(question_body)}sil <[50]> {postsentence}sil <[50]>{variants}',
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
        }

    analytics = {
        "events": [
            {
                "name": "Повторить",
                "value": {
                    "Объект повторения": response['text'],
                }
            },
        ]
    }

    return {
            "response": response,
            "analytics": analytics,
            "session_state": session_state
        }