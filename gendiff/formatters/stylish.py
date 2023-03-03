from gendiff.tools import format_data


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
