

def repeat_replies(event):

    user_say = event['request']['command']

    response: dict = {
            'text': user_say,
            'tts': user_say,
            'end_session': 'false'
    }

    return response
