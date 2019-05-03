"""
User interface module.

This module is responsible for receiving a user command and coordinating the
handling of the command until its completion. Its helpers are the listener, to
generate a request out of the command, the request handler, to handle an
interface to the search engine and the speaker, to get user input and print
output.
"""

import os

from typing import List

import actions

import interpreter.speaker as speaker
import interpreter.requesthandler as requesthandler
import interpreter.listener.Listener as Listener


class UserInterface:
    """Will receive a command upon creation and talk to speaker, listener and
    request handler to sort it out."""
    def __init__(self, command: List[str]) -> None:
        command.pop(0)
        self.request = Listener.listen(command)
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
                    actions.TalkAction,
                    actions.ShowAction]:
                speaker.Speaker(self.request)
            elif action == actions.DoNothingAction:
                # Done
                break
            # Other actions will be handled by handler here:
            action = self.handler.handle(self.request)
