"""
Results manager class, responsible for handling filehandler and search results
and making them readable for the user.

FIXME: Is it really necessary to receive a request here? -> I think so, but idk.
"""
import os

import actions
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

    def handle_search_failed(self, options=None) -> None:
        """
        If keywords were not enough to point to a specific file, then add dialog
        to ask user for more keywords.
        """
        self.req.add_action(actions.AskAction)
        self.req.add_dialog(dialogues.RefineSearchDialog())
        self.req.add_action(actions.SearchAction)

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
        else:
            self.req.results = results
