"""
Search engine is responsible for organizing the search and process requests for
a file. It receives a request and works on it to delegate the tasks between
other required methods. Its principle is similar to interpreter's user
interface. After processing, if direct file handling is needed, it will send a
command to file handler in order to process a request.
"""

import os
from typing import Dict, Any

import actions

import searchengine.characteristicshandler as chrh
import searchengine.searchtablehandler as sth
import searchengine.resultsmanager as resman
import searchengine.filerequirer as filereq

import exceptions as exc

PATH_TO_ENTRIES_DB = os.get_cwd() + "/entriesdb.json"





class Searcher:
    """
    Class responsible for search and processing actions of a request. It will
    receive a request, process it as needed and, if required, send a command
    down to file handler.
    :request: Request : Request do be processed.
    """

    def __init__(self, request):
        self.request = request
        self.results_manager = resman.ResultsManager(self.request)

    def _get_file_characts(self) -> Dict[str, str]:
        """Sends file to characteristics handler and gets the result of the
        analysis back.
        :return: Dict[str, str] : Dictionary with file characteristics.
        """
        return chrh.CharacteristicsHandler.handle_file_path(
            self.request.filename)

    def _handle_results(self, results: Any) -> None:
        """Receives results as parameter. Updates results to request.
        :results: Any : Results to be passed on to the request.
        """
        self.results_manager.handle_results_filehandler(results)

    def process_request(self) -> None:
        """Will check which action request has and process it. Can be called
        several times over the same request. Updates results on request object.

        Action of the request will be updated when back on request handler.
        """
        entries_table = sth.SearchTableHandler(PATH_TO_ENTRIES_DB)
        tmp_results = entries_table.query(self.request.filename)
        if self.request.action == actions.SearchAction:
            # FIXME: Maybe it should just send a warning and return [0]?
            if len(tmp_results) > 1:
                self.results_manager.handle_search_failed()
            elif not len(tmp_results):
                self.results_manager.handle_error(
                    "Could not find any file from given data.")
            else:
                self._handle_results(tmp_results[0])
        elif self.request.action == actions.ProcessAction:
            # FIXME: Failed require results do not update table search entry
            # FIXME: Maybe think of a better way of doing this?
            while len(self.request.process_steps):
                step = self.request.process_steps.pop(0)
                if step.startswith('search-expect'):
                    if step.endswith('no-results') and len(tmp_results):
                        self.results_manager.handle_error(
                            "File already entried, expected non-existing file.")
                        break
                    elif step.endswith('results') and not len(tmp_results):
                        self.results_manager.handle_error(
                            "File search returned nothing, expected results.")
                        break
                    else:
                        raise NotImplementedError(
                            "Unexpected processing option: " + step)
                elif step == 'characteristics':
                    tmp_results = self._get_file_characts()
                elif step == "save":
                    entries_table.add(tmp_results)
                elif step == "require":
                    # FIXME: check that dict has ID keyword here
                    tmp_results = filereq.FileRequirer().process_request(
                        self.request)
                elif step == "result":
                    self._handle_results(tmp_results)
                elif step == "update":
                    entries_table.update(tmp_results)
                elif step == "delete":
                    try:
                        entries_table.delete(tmp_results[0]["id"])
                    except KeyError:
                        self.results_manager.handle_error(
                            "File was not saved or not retreived correctly,"
                            + " no ID found.")
