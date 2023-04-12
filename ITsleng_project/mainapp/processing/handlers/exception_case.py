import random


from mainapp.processing.db.extract_json import get_db_sentences
from mainapp.processing.handle_sessionfile import get_qa_session_sentence
from mainapp.processing.handlers.generate_question import tts_prompt_sound
from mainapp.processing.handlers.generate_variants_objects import generate_var_string, generate_var_buttons
from mainapp.processing.utils.custom_response import RapidJSONResponse


def exception_replies(event_dict: dict, error: Exception):
    """
    Функция для отработки исключений. Отправляет сформулированный ответ извинения и новый вопрос.
    """
    session_id: str = event_dict['session']['session_id']

    # Берем новый вопрос для сессии
    question_dict: dict = get_qa_session_sentence(session_id)
    # Из вопроса-словаря берем сам вопрос и варианты ответов
    question_body: str = question_dict["sentence"]
    question_variants: list = question_dict["variants"][:3]
    variants: str = generate_var_string(question_variants)
    # Выбираем случайным образом предложение похвалы и "вариантов"
    sentences: dict = get_db_sentences()
    postsentence: str = random.choice(sentences["POSTsentence"])

    exception_sentence: str = \
        random.choice(['Извини, я отвлеклась и забыла, что спрашивала. Задам тебе новый вопрос.',
                       'Что-то случилось и я забыла, про что говорила. Вообщем, давай дальше.',
                       'Ой. Кажется у меня провал в памяти. Я задам тебе другой вопрос.',
                       'Ты удивишься, но я забыла ответ. Предлагаю понять и простить. Следующий вопрос.'
                       ])

    response: dict = {
            'text': f'😳{exception_sentence}\n ✨{question_body} \n{postsentence}:\n{variants}'.replace(" - ", "").replace("+", ""),
            'tts': f'{exception_sentence}sil <[100]>{tts_prompt_sound(question_body)}sil <[50]>.{postsentence}:sil <[50]>{variants}',
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
    }

    analytics: dict = {
        "events": [
            {
                "name": "Ошибка в системе",
                "value": {
                    "Ответ": str(error)
                }
            },
        ]
    }

    resp_data: dict = {
        'version': event_dict['version'],
        'session': event_dict['session'],
        'response': response,
        'analytics': analytics,
        'session_state': {
            "question_dict": question_dict,
            "attempt": 1
        }
    }
    return RapidJSONResponse(resp_data)
