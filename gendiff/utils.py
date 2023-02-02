import argparse
import json
import yaml


def argument_parser():
    parser = argparse.ArgumentParser(
        prog='gendiff',
        usage='gendiff [-h] [-f FORMAT] first_file second_file',
        description='Compares two configuration files and shows a difference.',
    )

    parser.add_argument('-f', '--format', help='set format of output')
    parser.add_argument('first_file', help='path to the first file')
    parser.add_argument('second_file', help='path to the second file')

    return parser.parse_args()


def to_lower(arg):
    if type(arg) is bool:
        return str(arg).lower()
    return str(arg)


def dict_diff(first_dict: dict, second_dict: dict) -> dict:
    result = {}

    for key, value in first_dict.items():
        if key not in second_dict or key in second_dict \
                and second_dict[key] != value:
            sign = '-'
        else:
            sign = ' '
        result[f'{str(key)}: {to_lower(value)}'] = sign

    for key, value in second_dict.items():
        if key not in first_dict or key in first_dict \
                and first_dict[key] != value:
            sign = '+'
        else:
            sign = ' '
        result[f'{str(key)}: {to_lower(value)}'] = sign

    return result


def generate_diff(path_to_first_file: str, path_to_second_file: str) -> str:
    yaml_extensions = ('.yml', 'yaml')
    json_extensions = '.json'
    result = ''

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
            'Format is not supported. Supported format are JSON and YAML'
        )

    diff = dict_diff(first_file_data, second_file_data)
    sorted_diff = sorted(diff)
    for i in sorted_diff:
        result += f'\n {diff[i]} {i}'
    result = '{%s\n}' % result

    return result
