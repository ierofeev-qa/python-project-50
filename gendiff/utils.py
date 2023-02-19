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


def to_lower(arg):
    if type(arg) is bool:
        return str(arg).lower()
    return str(arg)


def to_primitive(arg):
    a = '\'\"'
    for i in a:
        arg = str(arg).replace(i, '')
    return arg


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
        else:
            sign = ' '
        result.append({'key': str(key), 'value': to_lower(value), 'sign': sign})

    for key, value in second_dict.items():
        if key not in first_dict or key in first_dict \
                and first_dict[key] != value and type(value) != dict:
            sign = '+'
        else:
            continue
        result.append({'key': str(key), 'value': to_lower(value), 'sign': sign})

    return result


def stylish(value, replacer, spaces_count, counter):
    result = ''
    sorted_value = sorted(value, key=lambda x: x['key'])

    for item in sorted_value:
        if type(item['value']) is list:
            result += \
                f'{replacer*spaces_count}{to_primitive(item["sign"])}' \
                f' {to_primitive(item["key"])}:' \
                f' {{\n{stylish(item["value"], replacer, spaces_count=spaces_count + counter, counter=counter)}' \
                f'{replacer*spaces_count}}}\n'  # noqa: E501
        else:
            result += \
                f'{replacer*spaces_count}{to_primitive(item["sign"])}' \
                f' {to_primitive(item["key"])}: {to_primitive(item["value"])}\n'

    return result


def stringify(value, format, replacer=' ', spaces_count=1):
    if type(value) in (str, bool, int, float):
        return to_primitive(value)
    if format == 'stylish':
        return '{\n' + stylish(value, replacer, spaces_count, spaces_count) + '}'  # noqa: E501
    return 'LOOOL'


def generate_diff(
        path_to_first_file: str,
        path_to_second_file: str,
        format: str
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
