import argparse
import json
import yaml


def argument_parser():
    parser = argparse.ArgumentParser(
        prog='gendiff',
        usage='gendiff [-h] [-f FORMAT] first_file second_file',
        description='Compares two configuration files and shows a difference.',
    )

    parser.add_argument(
        '-f', '--format', help='set format of output', default='stylish'
    )
    parser.add_argument('first_file', help='path to the first file')
    parser.add_argument('second_file', help='path to the second file')

    return parser.parse_args()


# def to_lower(arg):
#     if type(arg) is bool:
#         return str(arg).lower()
#     return str(arg)
#
#
# def to_primitive(arg):
#     a = '\'\"'
#     for i in a:
#         arg = str(arg).replace(i, '')
#     arg = str(arg).replace('None', 'null')
#     return arg


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


def dict_diff(first_dict: dict, second_dict: dict) -> list:
    result = []

    for key, value in first_dict.items():

        if key in second_dict and \
                type(value) is dict and \
                type(second_dict[key]) is dict:
            sign = ' '
            result.append({
                'key': str(key),
                'value': dict_diff(value, second_dict[key]),
                'sign': sign
            })
            continue

        if key not in second_dict or key in second_dict \
                and second_dict[key] != value:
            sign = '-'
            if type(value) == dict:
                result.append({'key': str(key), 'value': added_dict(value), 'sign': sign})
            else:
                result.append({'key': str(key), 'value': value, 'sign': sign})
        else:
            sign = ' '
            result.append({'key': str(key), 'value': value, 'sign': sign})

    for key, value in second_dict.items():
        sign = '+'

        if key not in first_dict and type(value) == dict:
            result.append({'key': str(key), 'value': added_dict(value), 'sign': sign})

        elif key not in first_dict and type(value) != dict:
            result.append({'key': str(key), 'value': value, 'sign': sign})

        elif key in first_dict and type(value) == dict and type(first_dict[key]) != dict:
            result.append({'key': str(key), 'value': added_dict(value), 'sign': sign})

        elif key in first_dict and first_dict[key] != value and type(value) != dict:
            result.append({'key': str(key), 'value': value, 'sign': sign})

        else:
            continue

    return result


def stylish(value, replacer, spaces_count, counter):
    result = ''
    sorted_value = sorted(value, key=lambda x: x['key'])

    for item in sorted_value:
        if type(item['value']) is list:
            result += \
                f'{replacer*spaces_count}{format_data(item["sign"])}' \
                f' {format_data(item["key"])}:' \
                f' {{\n{stylish(item["value"], replacer, spaces_count=spaces_count + 2, counter=counter)}' \
                f'{replacer*spaces_count}  }}\n'  # noqa: E501

        else:
            result += \
                f'{replacer*spaces_count}{format_data(item["sign"])}' \
                f' {format_data(item["key"])}: {format_data(item["value"])}\n'

    return result


def plain(value, previous_node=''):
    result = []
    replacer = '[complex value]'

    for item in value:
        current_node = item['key']

        if previous_node:
            current_node = f"{previous_node}.{current_node}"

        if type(item['value']) is list:
            result += plain(item['value'], previous_node=current_node)

        if len(s := [b for b in value if b['key'] == item['key']]) == 2:
            # print(s)
            old_value = [f['value'] for f in s if f['sign'] == '-'][0]
            new_value = [f['value'] for f in s if f['sign'] == '+'][0]

            if type(new_value) is list:
                new_value = replacer
            elif type(new_value) is str:
                new_value = f'\'{format_data(new_value)}\''
            else:
                new_value = format_data(new_value)

            if type(old_value) is list:
                old_value = replacer
            elif type(old_value) is str:
                old_value = f'\'{format_data(old_value)}\''
            else:
                old_value = format_data(old_value)

            # old_value_replacer = replacer if type(old_value) is list else old_value
            # new_value_replacer = '[complex value]' if type(new_value) is list or f'\'{new_value}\'' if type(new_value) is str else new_value
            result.append(f"Property '{current_node}' was updated. From {old_value} to {new_value}")

        elif item['sign'] == '-':
            result.append(f"Property '{current_node}' was removed")

        elif item['sign'] == '+':
            if type(item["value"]) is list:
                new_value = replacer
            elif type(item["value"]) is str:
                new_value = f'\'{format_data(item["value"])}\''
            else:
                new_value = format_data(item["value"])

            # replacer = '[complex value]' if type(item["value"]) is list else item['value']
            result.append(f"Property '{current_node}' was added with value: {new_value}")

    result = sorted(list(set(result)))
    return result


def json_format(value):
    return json.dumps(value)


def stringify(value, format, replacer='  ', spaces_count=1):
    if type(value) in (str, bool, int, float):
        return format_data(value)
    if format == 'stylish':
        return '{\n' + stylish(value, replacer, spaces_count, spaces_count) + '}'  # noqa: E501
    elif format == 'plain':
        return '\n'.join(plain(value))
    elif format == 'json':
        return json_format('{\n' + stylish(value, replacer, spaces_count, spaces_count) + '}')


def generate_diff(
        path_to_first_file: str,
        path_to_second_file: str,
        format: str = 'stylish'
) -> str:
    yaml_extensions = ('.yml', '.yaml')
    json_extensions = '.json'

    if path_to_first_file.endswith(yaml_extensions) \
            and path_to_second_file.endswith(yaml_extensions):
        first_file_data = yaml.safe_load(open(path_to_first_file))
        second_file_data = yaml.safe_load(open(path_to_second_file))

    elif path_to_first_file.endswith(json_extensions) \
            and path_to_second_file.endswith(json_extensions):
        first_file_data = json.load(open(path_to_first_file))
        second_file_data = json.load(open(path_to_second_file))

    else:
        raise AssertionError(
            'Format is not supported. Supported formats are JSON and YAML'
        )

    diff_dict = dict_diff(first_file_data, second_file_data)
    result = stringify(diff_dict, format)

    return result
