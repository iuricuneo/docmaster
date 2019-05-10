"""
Results manager class, responsible for handling filehandler and search results
and making them readable for the user.

FIXME: Is it really necessary to receive a request here? -> I think so, but idk.
"""
import os

import action
import dialogues
import userrequests as ureq


class ResultsManager:
    """
    Will get the results from from filehandler and update the request to handle
    the display appropriately.
    Receives the request upon creation.
    """
    def __init__(self, request):
        self.req = request

    def handle_error(self, error_string: str) -> None:
        """
        Receives error message and updates request with it.
        """
        self.req.results = error_string
        self.req.flags['error'] = True

    def handle_search_failed(self, options) -> None:
        """
        If keywords were not enough to point to a specific file, then add dialog
        to ask user for more keywords.
        """
        self.req.add_action(actions.AskAction)
        self.req.add_dialog(dialogues.RefineSearchDialog())

    def handle_results_filehandler(self, results) -> None:
        """
        Handles results received from filehandler. Updates request accordingly.
        The results are given as parameter.
        :results: Any : Any result received by the filehandler to be handled
        """
        if not results:
            self.handle_error(
                "Could not reach saved file."
                + " Make sure that you have permissions to do so.")
        elif results == True:
            self.request.results = True
        elif os.path.exists(results):
            self.request.results = results
        else:
            self.handle_error(
                "Got successful result, but not sure what to do with it:\n"
                + str(results))
