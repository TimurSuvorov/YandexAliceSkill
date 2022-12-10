import random


def generate_var_buttons(question_variants) -> list:
    buttons_list = []

    for var in question_variants:
        buttons_list.append({'title': f'⚡{var.capitalize()}', 'hide': 'true'})
        random.shuffle(buttons_list)
    buttons_list.append({'title': "🤔Не знаю", 'hide': 'true'})
    return buttons_list


if __name__ == '__main__':
    f = generate_var_buttons(['окиара', 'таска', 'фича'])
    print(f)