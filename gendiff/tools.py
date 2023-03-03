def format_data(data):
    a = '\'\"'

    if type(data) is bool:
        data = str(data).lower()

    elif type(data) is not str:
        for i in a:
            data = str(data).replace(i, '')

    data = str(data).replace('None', 'null')
    return data


def added_dict(data):
    result = []
    for key, value in data.items():
        result.append({
            'key': key,
            'value': added_dict(value) if type(value) is dict else value,
            'sign': ' '
        })
    return result
