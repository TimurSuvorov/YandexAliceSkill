import copy
import random
from pprint import pprint

from ..db.images import Image
from ..declension_numbers import decl_scores
from mainapp.processing.db.extract_json import get_db_sentences, get_db_sounds
from ..handle_sessionfile import get_qa_session_sentence
from ..handle_userprofile import update_scores
from .proc_response_obj import (
    generate_var_buttons,
    generate_var_string,
    tts_prompt_sound,
    remove_tts_symbols,
)


def correctanswer(command: str, session_state: dict, user_id: str, session_id: str, message_id: int):

    # Выбираем предложение похвалы и случайным образом "вариантов"
    sentences = get_db_sentences()
    nicesentences = copy.deepcopy(sentences["NICEsentence"])
    nicesentence = random.choice(nicesentences)
    postsentence = random.choice(sentences["POSTsentence"])
    sayrating = ''
    letsnext = random.choice(sentences["LETSNEXTsentence"])

    # Проверяем на схожесть слова. Если не один-в-один, то добавляем варианты реакции на это
    rightanswer = session_state["question_dict"]["answers"][0].replace("+", "").replace(" - ", "")
    if rightanswer != command:  # FIXIT check by regex
        nicesentences += [
            "Пишется по-другому, но я поняла. Верно!",
            "Нечетко говоришь, но, похоже, ты прав!",
            "Было непросто понять твои слова,sil <[100]> но ты прав!",
            "Я тебя поняла! Верно!",
            "Не уверена в совпадении на 100 процентов. Н+о, хорош+о.sil <[100]> Засчит+аем!",
            "Поздравляю с верным ответом!sil <[100]> Отл+ично.sil <[90]>",
            "Мои н+ейро+уши распознали похожее слово, sil <[100]>хорошо есть н+ейромозг+и. Верно!"
        ]
        # Выбираем из всех реакций похвалы случайно
        nicesentence = random.choice(nicesentences)

    # Показывать или нет объяснение при верном ответе
    question_explanation = ""
    answer = session_state["question_dict"]["answers"][0]
    if random.choice([True, False]):
        question_explanation = session_state["question_dict"]["explanation"]
        question_explanation = f'Ответ: {answer}.sil <[100]>\n{question_explanation}\n\n'

    # Подсчёт рейтинга и его отображение
    score = session_state["attempt"] + 1
    cur_scores = update_scores(user_id, session_id, score)
    allscores = cur_scores["allscores"]
    sessionscore = cur_scores["sessionscore"]
    cur_rating = f'\n\n🏅Ваш рейтинг:\nОбщий: {allscores}\nВ этой игре: {sessionscore}'

    # Если первый верный ответ, то поздравим с этим
    if 1 <= cur_scores["allscores"] <= 2:
        nicesentence = f'Поздравляю с первым верным ответом!sil <[100]> Отличное начало.sil <[90]> У тебя плюс {decl_scores(sessionscore)}.'
        question_explanation = ''
    # Если баллов больше 5 и сообщение каждое 2-е или 3-е
    elif sessionscore > 4 and message_id % random.choice([3, 2]) == 0:
        cur_rating = ''
        sayrating = random.choice(
            [
                f'Движешься уверенно вперёд. sil <[100]>Ты набрал {decl_scores(sessionscore)} за игру и {decl_scores(allscores)} за всё время.\n\n',
                f'Сейчас у тебя {decl_scores(sessionscore)} за игру и {decl_scores(allscores)} в целом. sil <[100]>Очень неплохо!\n\n',
                f'Поражаюсь твоей целеустремл+ённости. sil <[100]>За игру {decl_scores(sessionscore)} sil <[70]>и всего {decl_scores(allscores)}.sil <[100]> Так держ+ать!\n\n',
                f'Я верила в тебя не зря! sil <[100]>Ты набрал {decl_scores(sessionscore)} за игру, sil <[70]>а всего {decl_scores(allscores)}.\n\n'
            ]
        )

    # Выбираем звуки
    sounds = get_db_sounds()
    correctsound = random.choice(sounds["CORRECT"])
    questionsound = random.choice(sounds["QUESTION"])
    # Берем новый вопрос для сессии
    question_dict = get_qa_session_sentence(session_id)
    # Из вопроса-словаря берем сам вопрос и варианты ответов
    question_body = question_dict["sentence"]
    question_variants = question_dict["variants"][:3]
    variants = generate_var_string(question_variants)

    response: dict = {
            'text': remove_tts_symbols(f'👍{nicesentence}\n{question_explanation}\n{sayrating}{letsnext}.\n✨{question_body} \n{postsentence}:\n{variants}{cur_rating}'),
            'tts': f'{correctsound}sil <[50]>{nicesentence}sil <[100]>{question_explanation} sil <[100]> {sayrating} sil <[100]>{letsnext}sil <[100]>{questionsound}{tts_prompt_sound(question_body)}sil <[50]>.{postsentence}:sil <[50]>{variants}',
            'card': {
                'type': 'BigImage',
                'image_id': Image.CORRECT_ANSWER.id,
                'title': remove_tts_symbols(random.choice(sentences["NICEsentence"])),
                'description': remove_tts_symbols(f'{question_explanation}{sayrating}{letsnext}.\n✨{question_body} \n{postsentence}:\n{variants}{cur_rating}'),
            },
            'buttons': generate_var_buttons(question_variants),
            'end_session': 'False'
    }
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
