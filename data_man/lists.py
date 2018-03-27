def pretty_list(array, exclude=''):
    pretty = [str(index) + ': ' + element for index, element in enumerate(array) if element != exclude]
    return str(pretty)

def receive_list(text1, text2, keys, exclude=''):
    print(text1 + ': ' + pretty_list(keys, exclude=exclude))
    types = input(text2 + ': ').split()
    types = [int(typ) for typ in types]
    names = [keys[index] for index in types]
    return names