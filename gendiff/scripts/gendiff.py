#!/usr/bin/env python3
import argparse
import json


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


def dict_diff(first_dict: dict, second_dict: dict) -> dict:
    result = {}
    first_dict_items = list(first_dict.items())
    second_dict_items = list(second_dict.items())
    union_list = first_dict_items + second_dict_items

    for item in union_list:
        if item in first_dict_items and item in second_dict_items:
            sign = ' '
        elif item in first_dict_items and item not in second_dict_items:
            sign = '-'
        else:
            sign = '+'

        result[f'{str(item[0])}: {str(item[1])}'] = sign

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
    args = argument_parser()
    print(generate_diff(args.first_file, args.second_file))


if __name__ == '__main__':
    main()
