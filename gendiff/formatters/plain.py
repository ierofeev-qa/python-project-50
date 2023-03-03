from gendiff.tools import format_data


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

            result.append(f"Property '{current_node}' was added with value: {new_value}")

    result = sorted(list(set(result)))
    return result
