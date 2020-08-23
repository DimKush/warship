
def round_list(input_list, digit):
    if input_list:
        if isinstance(input_list[0], float):
            return [round(x, digit) for x in input_list]
        elif isinstance(input_list[0], list):
            res = []
            for sublist in input_list:
                res.append([round(x, digit) for x in sublist])
            return res


def remove_id(elem):
    if elem.get('id'):
        elem.pop('id')
        elem.pop('c')
        elem.pop('aabb')
    return elem
