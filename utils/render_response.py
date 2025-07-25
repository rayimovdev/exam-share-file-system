

def render_data(data, success) -> dict:
    data = {
        'data': data,
        'success': success,
    }
    return data


def render_message(message, success) -> dict:
    data = {
        'message': message,
        'success': success,
    }
    return data