"""
The CharacteristicsHandler will receive a file path, read out its
characteristics as needed and return a dictionary with them.
More functions can will be added in the future.

Tip for usage:
import characteristicshandler.CharacteristicsHandler as chan
chars = chan.handle_file_path("/path/to/file.hi")
"""

import os
from datetime import datetime


class CharacteristicsHandler:
    """
    Class to read out file properties.
    """
    @staticmethod
    def handle_file_path(file_path: str): # (str) -> Dict[str, str]
        """
        Function to receive a file string and return its characteristics as a
        dictionary. To be treated as a class, maybe will become one in the future.
        """
        chars = {
            "name": '',
            "extension": '',
            "orig_name": '',
            "entry_date": '',
            "keywords": '', # e.g. "word1, word2, word3" to be used with "in"
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

    chan = CharacteristicsHandler()
    print(chan.handle_file_path('test'))
    print(chan.handle_file_path('test.txt'))
    print(chan.handle_file_path('test.testing.tested.txt'))

    os.system('rm test test.txt test.testing.tested.txt')
