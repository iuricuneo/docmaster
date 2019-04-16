"""
Request handler module.

Will receive a request and handle its actions regarding processing and search.
Will also handle some of user's input after an ask.
"""

import dialogues
import actions as act

class RequestHandler:
    """The request handler will receive a request and decide what to do with it
    next, whether to send to the speaker, to say something or to send to the
    search engine."""
    def __init__(self) -> None:
        self.results = ''

    def handle(self, request): # (RequestHandler, Request) -> Action:
        """Receives a request and returns the next action as a class
        :request: Request
        """
        should_process = True
        request.update_action()
        while request.action in [act.SearchAction, act.ProcessAction]:
            request._print(
                "Action: "
                + request.action.__name__.replace(
                    "Action","."))
            # Can't think of a use case when we'd do these two in a row, but
            # since it's just change a if for a while, why not leave it there?
            for dialog in request.dialog_list:
                if dialog.is_fulfilled:
                    should_process = self._check_dialog_fulfilled(dialog)
            if not should_process:
                while request.action is not act.DoNothingAction:
                    request.update_action()
                request._print("Cancelled by user. Exiting...")
                continue
            request._print("Processing request...")
            self.results = request.filename
            request._print("Done processing request.")
            request.update_action()
        request._print(
            "Action: "
            + request.action.__name__.replace(
                "Action","."))
        return request.action

    def _check_dialog_fulfilled(self, dialog):
        """
        Received a fulfilled dialog and checks what user wants to do with it.
        Returns boolean with whether request should be processed further or not.

        :dialog: Dialog
        :return: bool
        """
        if (type(dialog) in [
                dialogues.ConfirmUpdateDialog,
                dialogues.ConfirmDeleteDialog,
                dialogues.ConfirmLargeRequestDialog]):
            if dialog.remember_last_answer() == 'cancel':
                return False
        return True

    def get_search_results(self) -> str:
        """Returns search results and clears it."""
        tmp = self.results
        self.results = ""
        return tmp
