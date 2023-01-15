#!/usr/bin/env python3
import argparse
import json

parser = argparse.ArgumentParser(
    prog='gendiff',
    usage='gendiff [-h] [-f FORMAT] first_file second_file',
    description='Compares two configuration files and shows a difference.',
)

parser.add_argument('-f', '--format', help='set format of output')
parser.add_argument('first_file', help='path to the first file')
parser.add_argument('second_file', help='path to the second file')

args = parser.parse_args()


def dict_diff(first_dict: dict, second_dict: dict) -> dict:
    result = {}

    for key, value in first_dict.items():
        if key in second_dict and value == second_dict[key]:
            result[f'{str(key)}: {str(value)}'] = ' '
        elif key in second_dict and value != second_dict[key]:
            result[f'{str(key)}: {str(value)}'] = '-'
            result[f'{str(key)}: {str(second_dict[key])}'] = '+'
        else:
            result[f'{str(key)}: {str(value)}'] = '-'

    for key, value in second_dict.items():
        if key not in first_dict:
            result[f'{str(key)}: {str(value)}'] = '+'

    return result


def generate_diff(path_to_first_file: str, path_to_second_file: str) -> str:
    first_file_data = json.load(open(path_to_first_file))
    second_file_data = json.load(open(path_to_second_file))
    result = ''

    diff = dict_diff(first_file_data, second_file_data)
    sorted_diff = sorted(diff)
    for i in sorted_diff:
        result += f'\n {diff[i]} {i}'
    result = '{%s\n}' % result

    return result


def main():
    print(generate_diff(args.first_file, args.second_file))


if __name__ == '__main__':
    main()
