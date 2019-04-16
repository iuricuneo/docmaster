import dialogues
import actions as act

from exceptions import DialogUnfulfilledError


class Request:

    def __init__(self, filename, options):
        self.action = act.WaitForHandlingAction
        self.dialog_list = [] #type: Dialog
        self.filename = filename #type: str
        self.options = options #type: list[str]
        self.actions = [] #type: list[Action]

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

    def add_dialog(self, dialog):
        """Will add a dialog to the dialogs list
        dialogs are always added under index 0"""
        self.dialog_list.insert(0, dialog)

    def get_dialog(self):
        """Returns a dialog object."""
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
    def __init__(self, filename, options):
        super().__init__(filename, options)
        self.actions = [act.ProcessAction]


class ReadEntryRequest(Request):
    def __init__(self, filename, options):
        super().__init__(filename, options)
        self.actions = [act.SearchAction, act.ShowAction]
        self.add_dialog(dialogues.ShowResultsDialog())


class UpdateEntryRequest(Request):
    def __init__(self, filename, options):
        super().__init__(filename, options)
        self.actions = [act.SearchAction, act.ProcessAction]
        if not self._forced():
            self.actions.insert(1, act.AskAction)
            self.add_dialog(dialogues.ConfirmUpdateDialog())


class DeleteEntryRequest(Request):
    def __init__(self, filename, options):
        super().__init__(filename, options)
        self.actions = [act.SearchAction, act.ProcessAction]
        if not self._forced():
            self.actions.insert(1, act.AskAction)
            self.add_dialog(dialogues.ConfirmDeleteDialog())


class ErrorRequest(Request):
    def __init__(self, filename, options):
        super().__init__(filename, options)
        self.actions = [act.TalkAction]
        self.add_dialog(dialogues.ErrorDialog())
