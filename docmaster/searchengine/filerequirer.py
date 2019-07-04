"""
Class to handle creation of commands and interfacing with file handler.
"""

import commands
import filehandler
import userrequests as ureq

class FileRequirer:
    """
    Will receive the request upon creation and process it to create a command
    and forward to file handler. Holds instance of file handler.

    FIXME: merge this in SearchEngine?
    """
    def __init__(self):
        self.req = None

    def process_request(self, request):
        """
        Processes given request creating a command out of it and forwarding it
        to file handler. Once it has been handled, process returned value to
        return results to search engine.
        :request: userrequests.Request : Request to be handled.
        """
        self.req = request
        command = self.get_command()
        file_handler = filehandler.FileHandler(command)
        file_handler.handle_command()
        return command.result

    def get_command(self):
        """
        Operates on the request to generate a command out of it. Returns an
        instance of the command.
        """
        req_type = type(self.req)

        if req_type == ureq.CreateEntryRequest:
            return commands.CreateCommand(self.req.results)
        elif req_type == ureq.ReadEntryRequest:
            return commands.ReadCommand(self.req.results)
        elif req_type == ureq.UpdateEntryRequest:
            return commands.UpdateCommand(self.req.results)
        elif req_type == ureq.DeleteEntryRequest:
            return commands.DeleteCommand(self.req.results)
