import os
from datetime import datetime

def CharacteristicsHandler(file_path: str): # (str) -> Dict[str, str]
    """
    Function to receive a file string and return its characteristics as a
    dictionary. To be treated as a class, maybe will become one in the future.
    """
    chars = {
        "name": '',
        "extension": '',
        "orig_name": '',
        "entry_date": '',
        "read_last": '',
        "updated_last": ''}

    file_name = file_path.split(os.sep)[-1]
    chars['orig_name'] = chars['name'] = file_name
    chars['read_last'] = chars['updated_last'] = chars['entry_date'] = str(
        datetime.now())
    split_name = file_name.split('.')
    if len(split_name) > 1:
        chars['extension'] = split_name[-1]
    return chars


if __name__ == '__main__':
    os.system('touch test test.txt test.testing.tested.txt')

    print(CharacteristicsHandler('test'))
    print(CharacteristicsHandler('test.txt'))
    print(CharacteristicsHandler('test.testing.tested.txt'))

    os.system('rm test test.txt test.testing.tested.txt')
