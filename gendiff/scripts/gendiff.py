#!/usr/bin/env python3
from gendiff.utils import argument_parser, generate_diff


def main():
    args = argument_parser()
    print(generate_diff(args.first_file, args.second_file, args.format))


if __name__ == '__main__':
    main()
