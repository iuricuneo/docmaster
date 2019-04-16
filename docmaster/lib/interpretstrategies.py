"""
Interpreting strategy used by the user interface to generate its requests.

A request is received by the UI, which invokes the listener to generate a
request from it. The listener will create an instance of InterpretingStrategy
to know which command has been received and, with the command, a child of
InterpretingStrategy is invoked to return the request.

A InterpretingStrategy interface is given, after which each concretion of a
strategy should be modelled, but the interface can and should be used too.
"""

import os

from typing import List, Tuple

import userrequests as requests

KNOWN_COMMANDS = [
    "save",
    "show",
    "update",
    "remove"] #type: List[str]


class InterpretingStrategy:
    """Strategy to interpret the command received into a request"""
    def __init__(self) -> None:
        self.request = None #type: Request
        self.options = [] #type: List[str]
        self.filename = '' #type: str

    def _save_options(self, command: List[str]) -> List[str]:
        """Receives a command to be interpreted, will remove the options and
        return the command without the options.
        :command: List[str]
        """
        options = []
        for term in command:
            if term.startswith('-'):
                options.append(term[1:])
        for term in options:
            command.remove('-' + term)
        self.options = options
        return command

    def get_request(self, command: List[str]) -> None:
        """Receives the command as List of strings and returns a processed
        request.
        The request is also saved."""
        clean_command = self._save_options(command)
        for term in clean_command:
            if term in KNOWN_COMMANDS or term:
                continue
            break
        filepath = os.getcwd() + os.sep + term
        if not os.path.isfile(filepath):
            raise IOError('File not found.')
        self.filename = term

    def get_command(self, command: List[str]) -> str:
        """From the whole command, gets the user request and returns it.
        If no word is found, 'error' is returned."""
        for term in command:
            if term in KNOWN_COMMANDS:
                return term
        return 'error'


class CreateEntryStrategy(InterpretingStrategy):
    """Strategy to create a CreateEntryRequest"""
    def get_request(self, command: List[str]): # (...) -> Request:
        """Receives the command as list of strings and returns a processed
        request.
        The request is also saved."""
        super().get_request(command)
        self.request = requests.CreateEntryRequest(self.filename, self.options)
        return self.request


class ReadEntryStrategy(InterpretingStrategy):
    """Strategy to create a ReadEntryRequest"""
    def get_request(self, command: List[str]): # (...) -> Request:
        """Receives the command as list of strings and returns a processed
        request.
        The request is also saved."""
        super().get_request(command)
        self.request = requests.ReadEntryRequest(self.filename, self.options)
        return self.request


class UpdateEntryStrategy(InterpretingStrategy):
    """Strategy to create an UpdateEntryRequest"""
    def get_request(self, command: List[str]): # (...) -> Request:
        """Receives the command as list of strings and returns a processed
        request.
        The request is also saved."""
        super().get_request(command)
        self.request = requests.UpdateEntryRequest(self.filename, self.options)
        return self.request


class DeleteEntryStrategy(InterpretingStrategy):
    """Strategy to create a DeleteEntryRequest"""
    def get_request(self, command: List[str]): # (...) -> Request:
        """Receives the command as list of strings and returns a processed
        request.
        The request is also saved."""
        super().get_request(command)
        self.request = requests.DeleteEntryRequest(self.filename, self.options)
        return self.request

class ErrorStrategy(InterpretingStrategy):
    """Strategy to create an ErrorRequest"""
    def get_request(self, command: List[str]): # (...) -> Request:
        """Receives the command as list of strings and returns a processed
        request.
        The request is also saved."""
        self.request = requests.ErrorRequest('', [])
        return self.request
