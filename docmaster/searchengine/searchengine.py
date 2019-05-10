"""
Search engine is responsible for organizing the search and process requests for
a file. It receives a request and works on it to delegate the tasks between
other required methods. Its principle is similar to interpreter's user
interface. After processing, if direct file handling is needed, it will send a
command to file handler in order to process a request.
"""

from typing import Dict, Any

import searchengine.characteristicshandler as chrh
import searchengine.resultsmanager as resman

class SearchEngine:
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
