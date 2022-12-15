import random
import re

from mainapp.processing.extract_json import get_db_sentences
from mainapp.processing.handlers.generate_question import generate_question, tts_prompt_sound
from mainapp.processing.handlers.generate_variants_objects import generate_var_string, generate_var_buttons
from mainapp.processing.handlers.service_replies import bye_replies

yes_answer = ["да$", "давай", "хорошо", "я не против", "начн.м", "продолж"]
no_answer = ["нет", "не хочу", "потом"]

def yes_no_cont_replies(command, session_state):
    sentences = get_db_sentences()
    postsentence = random.choice(sentences["POSTsentence"])

    # Если ответ положительный, то
    if re.search("|".join(yes_answer), command):
        # Вызвано ли сервисное сообщение во время вопроса - присутствует ли session_state["question_dict"]["answers"]
        # Если в прошлом ответе есть вопрос, значит его возвращаем
        if session_state.get('question_dict', {}).get('answers'):
            question_dict = session_state['question_dict']
            attempt = session_state['attempt']
            question_body = question_dict['sentence']
            question_variants = question_dict['variants']
            variants = generate_var_string(question_variants)
        else:
            # Генерируем сразу новый вопрос, вытаскиваем его тело и варианты для подстановки
            question_dict = generate_question()
            attempt = 1
            question_body = question_dict["sentence"]
            question_variants = question_dict["variants"]
            variants = generate_var_string(question_variants)

        response: dict = {
            'text': f'Прекрасно! {question_body}\n{postsentence}:\n{variants.replace("+", "")}',
            'tts': f'Прекрасно! sil <[60]> {tts_prompt_sound(question_body)}. {postsentence}: sil <[50]>{variants}',
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
        }

        sessionstate = {
            "question_dict": question_dict,
            "attempt": attempt
        }

    # Если ответ отрицательный, то прощаемся
    elif re.search("|".join(no_answer), command):

        response = bye_replies(session_state)["response"]
        sessionstate = session_state

    # Если ответ не из списка Да/Нет, то прикинуться валенком
    else:
        response: dict = {
            'text': f'Ой, я тебя не понимаю. Скажи "Да" или "Нет"',
            'tts': f'Ой sil <[50]>, я теб+я не понимаю.sil <[50]> Скажи "Да" или "Нет". Это я точно знаю',
            'buttons': [
                {'title': 'Да', 'hide': 'true'},
                {'title': 'Нет', 'hide': 'true'}
            ],
            'end_session': 'False'
        }
        # Передаём прозрачно
        sessionstate = session_state

    # Возвращаем сформированный вопрос, а также отдаем в session_state для дальнейшего учёта
    return {
        "response": response,
        "session_state": sessionstate
    }

