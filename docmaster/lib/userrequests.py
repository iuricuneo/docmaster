"""
Requests to be generated after user command.

A request is received by the UI, which invokes the listener to generate a
request from it. The request will then be handled by the other modules and hold
log-sensitive data such as user options and choices.

A Request interface is given, after which each concretion of a request should be
modelled.
"""

import dialogues
import actions as act


class Request:

    """Abstract class Request. Will tell other modules what the user wants."""

    def __init__(self, filename: str, options):
        self.action = act.WaitForHandlingAction
        self.dialog_list = [] #type: Dialog
        self.filename = filename #type: str
        self.options = options #type: list[str]
        self.actions = [] #type: list[Action]
        self.results = None #type: Any
        self.flags = {
            'error': False} #type: Dict[str, bool]
        self.process_steps = [] #type: List[str]

        self.verbose = False #type: bool
        for option_stack in self.options:
            if 'v' in option_stack:
                self.verbose = True

    def update_action(self):
        """Gets next action from action list, do nothing action is taken when
        nothing left to do"""
        if len(self.actions):
            self.action = self.actions.pop(0)
        else:
            self.action = act.DoNothingAction

    def add_action(self, action):
        """Adds action to action list, to be next solved."""
        self.action.insert(0, action)

    def add_dialog(self, dialog):
        """Will add a dialog to the dialogs list
        dialogs are always added under index 0"""
        self.dialog_list.insert(0, dialog)

    def get_dialog(self):
        """Returns the first dialog object in the list."""
        return self.dialog_list[0]

    def solve_dialog(self):
        """Marks a dialog object as solved."""
        to_last = self.dialog_list.pop(0)
        self.dialog_list.append(to_last)

    def _print(self, txt: str) -> None:
        """Prints if in verbose mode"""
        if self.verbose: print(txt)

    def _forced(self) -> None:
        """Checks options to know if we're forcing or should ask user"""
        for option_stack in self.options:
            if 'f' in option_stack:
                return True
        return False


class CreateEntryRequest(Request):
    """Request to create file entry, user wants to save file."""
    def __init__(self, filename, options):
        super().__init__(filename, options)
        self.actions = [act.ProcessAction]
        self.process_steps = [
            "search-expect=no-results",
            "characteristics",
            "save",
            "require",
            "result"]


class ReadEntryRequest(Request):
    """Request to read file entry, user wants to get access to a file."""
    def __init__(self, filename, options):
        super().__init__(filename, options)
        self.actions = [act.SearchAction, act.ShowAction]
        self.add_dialog(dialogues.ShowResultsDialog())


class UpdateEntryRequest(Request):
    """Request to update file entry, user wants to modify a file.
    This request can be forced with flag -f to not ask for confirmation."""
    def __init__(self, filename, options):
        super().__init__(filename, options)
        self.actions = [act.SearchAction, act.ProcessAction]
        if not self._forced():
            self.actions.insert(1, act.AskAction)
            self.add_dialog(dialogues.ConfirmUpdateDialog())
        self.process_steps = [
            "search-expect=results",
            "characteristics",
            "update",
            "require",
            "result"]


class DeleteEntryRequest(Request):
    """Request to delete file entry, user wants to remove a file from storage.
    This request can be forced with flag -f to not ask for confirmation."""
    def __init__(self, filename, options):
        super().__init__(filename, options)
        self.actions = [act.SearchAction, act.ProcessAction]
        if not self._forced():
            self.actions.insert(1, act.AskAction)
            self.add_dialog(dialogues.ConfirmDeleteDialog())
        self.process_steps = [
            "search-expect=results",
            "delete",
            "require",
            "result"]


class ErrorRequest(Request):
    """Returns an error message for unrecognized command."""
    def __init__(self, filename, options):
        super().__init__(filename, options)
        self.actions = [act.TalkAction]
        self.add_dialog(dialogues.ErrorDialog())
