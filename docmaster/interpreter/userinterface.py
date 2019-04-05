import os

from typing import List

import actions

import interpreter.speaker as speaker
import interpreter.listener as listener
import interpreter.requesthandler as requesthandler


class UserInterface:
    """Will receive a command upon creation and talk to speaker, listener and
    request handler to sort it out."""
    def __init__(self, command: List[str]) -> None:
        command.pop(0)
        self.request = listener.Listener(command)
        self.handler = requesthandler.RequestHandler()

    def handle_request(self) -> None:
        """Will iterate over the request handler and speaker to handle the
        request.
        Initial handle call will make sure we don't reach the action
        WaitForHandlingAction"""
        action = self.handler.handle(self.request)
        while action != actions.DoNothingAction:

            if action in [
                    actions.AskAction,
                    actions.TalkAction]:
                speaker.Speaker(self.request)
            elif action == actions.ShowAction:
                results = self.handler.get_search_results()
                speaker.Speaker(self.request, results=results)
            elif action in [actions.SearchAction, actions.ProcessAction]:
                # Action will have been handled in next iteration
                pass
            elif action == actions.DoNothingAction:
                break
            else:
                raise NotImplementedError(
                    "Should not have reached this point... "
                    + "Something went wrong.")

            action = self.handler.handle(self.request)
