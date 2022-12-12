from .generate_variants_objects import generate_var_buttons, generate_var_string
from mainapp.processing.extract_json import get_db_sentences


def repeat_replies(session_state: dict) -> dict:
    # Если пустой по каким-либо причинам, Алиса прикинится валенком
    if not session_state.get("question_dict"):
        response: dict = {
            'text': f'Ой, а я уже забыла. ¯\_(ツ)_/¯ . Давай я лучше загадаюю тебе слово?',
            'tts': f'Ой, а я уже забыла. Давай начнём сначала',
            'buttons': [{'title': 'Дальше', 'hide': 'true'}],
            'end_session': 'False'
        }
        session_state = {}
    else:
        question_dict = session_state["question_dict"]
        question_body = question_dict["sentence"]
        question_variants: list = question_dict["variants"]
        if len(question_variants) > 0:
            response: dict = {
                'text': f'{question_body}. Варианты:\n {generate_var_string(question_variants)}',
                'tts': f'Конечно! {question_body}. Варианты: {generate_var_string(question_variants)}',
                'buttons': generate_var_buttons(question_variants),
                'end_session': 'False'
            }
        else:
            response: dict = {
                'text': f'{question_body}',
                'tts': f'Конечно! {question_body}',
                'buttons': [{'title': 'Дальше', 'hide': 'true'}],
                'end_session': 'False'
            }

    return {
            "response": response,
            "session_state": session_state
        }