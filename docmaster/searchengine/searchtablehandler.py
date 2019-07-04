"""
FIXME: Remember to add an ID field
"""

from typing import Any
from typing import Dict
from typing import List

import tinydb

import exceptions as exc


class SearchTableHandler:
    """Class to handle the local database that stores the file entries, not
    the files per se."""
    def __init__(self, path_to_db="./filedata.json"):
        self.db = tinydb.TinyDB(path_to_db)
        self.next_id = len(self.db)

    def add(self, characts_dict: Dict[str, Any]) -> None:
        """Receives a dictionary with string keys and any values and saves it.
        Returns nothing.
        :Dict[str, Any] characts_dict: Dictionary with file data to be saved.
        :NoneType retval: None
        """
        characts_dict['id'] = self.next_id
        self.next_id += 1
        self.db.insert(characts_dict)

    def query(self, query_value: Any) -> List[Dict[str, Any]]:
        """
        Receives a value to look for in the database. If value is string,
        will look for a file with that name, if value is int, will look for a
        file with that ID. Returns empty list if no entry was found.

        :Any query_value: Value to look for. If string, file name, if int, id.
        :List[Dict[str, Any]] retval: List with entries that match.
        """
        results = []
        if isinstance(query_value, int):
            for entry in self.db:
                if query_value == entry['id']:
                    return [entry]
        elif isinstance(query_value, str):
            for entry in self.db:
                if query_value in entry['name']:
                    results.append(entry)
        return results

    def delete(self, delete_id: int) -> None:
        """
        Receives an entry to delete in the database. Will look for a
        file with given ID. Raises warning to misaligned DB if DB ID and entry
        ID don't match. Raises exception if no file was found.

        :int delete_id: ID of entry to delete.
        :NoneType retval: None
        """
        entry = tinydb.Query()
        removed = 0
        results = len(self.db.search(entry.id == delete_id))
        if results == 1:
            removed = len(self.db.remove(entry.id == delete_id))
        elif results > 1:
            raise exc.TooManyFieldsFoundError(
                "Given entry got too many results.")

        if removed < 1:  # Covers results = 0
            raise exc.FileDataNotFoundError("Could not delete file.")
        elif removed > 1:
            print("this must never happen... im sorry if it did [remove]")
            # *gives up life*

    def update(self, updated_entry: Dict[str, Any]) -> None:
        """
        Will receive a dictionary to update an entry. Entries are matched by
        ID, make sure to run query to get the right ID and update it in the
        entry before anything.
        :Dict[str, Any] updated_entry: Updated dictionary entry with old ID
        :NoneType retval: None
        """
        entry = tinydb.Query()
        results = len(self.db.search(entry.id == updated_entry['id']))
        if not results:
            raise exc.FileDataNotFoundError(
                "Could not update entry. No matching ID found for entry "
                + str(updated_entry))
        elif results > 1:
            raise exc.TooManyFieldsFoundError(
                "Given entry got too many results.")
        results = self.db.update(
            updated_entry, (entry.id == updated_entry['id']))
        if len(results) < 1:  # Covers results = 0
            raise exc.FileDataNotFoundError("Could not update file.")
        elif len(results) > 1:
            print("this must never happen... im sorry if it did [update]")
            # *gives up life*

    def get_file_name(self, id: int) -> str:
        """Function to get an ID and return its file name.
        :int id: ID to look for file
        :str retval: File name tied to corresponding ID
        """
        entry = tinydb.Query()
        results = self.db.search(entry.id == id)
        if not len(results):
            raise exc.FileDataNotFoundError(
                "Could not get entry name. No matches for ID " + str(id))
        elif len(results) > 1:
            raise exc.TooManyFieldsFoundError(
                "Given id got too many results. ID was " + str(id))
        return results[0]['name']
