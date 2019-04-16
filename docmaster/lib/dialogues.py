from actions import AskAction
from actions import TalkAction
from actions import DoNothingAction


class Ask:
    def __init__(self, text, options, pref=None):
        assert pref is None or pref in options
        self.text = text
        self.options = options
        self.pref = pref


class Dialog:

    def __init__(self):
        self.is_fulfilled = False
        self.history = []

    def hear(self, voice):
        """
        Adds entry to dialog history. Expected a tuple with 2 strings in format:
        (question, answer)
        :voice: Tuple(str, str)
        """
        self.history.append(voice)

    def has_been_fulfilled(self):
        """Marks dialog as fulfilled"""
        self.is_fulfilled = True

    def remember_last_answer(self):
        """Returns last answer from dialog."""
        return self.history[0][1]

    def __repr__(self):
        fulfilled = "fulfilled" if self.is_fulfilled else "open"
        string = "Dialog is " + fulfilled + " with history:\n"
        for message in self.history:
            string += message + '\n'
        return string

    def __str__(self):
        return self.__repr__()

    def say(self):
        """This should return an Ask object"""
        raise NotImplementedError(
            "Interface Dialog.say() not implemented in concretion.")


class ConfirmLargeRequestDialog(Dialog):
    """User wants to do a huge action, confirm
    Gets an ask action
    >>doesn't belong to minimal application<<"""
    def say(self):
        return Ask(
            "This is a large request, are you sure of it?",
            ['yes', 'cancel'],
            'yes')


class ConfirmDeleteDialog(Dialog):
    """User wants to delete a file, confirm, unless force option
    Gets an ask action"""
    def say(self):
        return Ask(
            "Are you sure you want to delete the file?",
            ['yes', 'cancel'],
            'yes')


class ConfirmUpdateDialog(Dialog):
    """User wants to update a file, confirm, unless force option
    Gets an ask action"""
    def say(self):
        return Ask(
            ("Are you sure you want to update the file?\n"
            + "The old entry will be lost."),
            ['yes', 'cancel'],
            'yes')


class RefineSearchDialog(Dialog):
    """Search didn't find results, get more terms
    Gets an ask action"""
    def say(self):
        return Ask(
            "Your search did not match any results, please refine it.",
            [])


class ShowResultsDialog(Dialog):
    """Shows results of search
    Gets a show action"""
    def say(self):
        return Ask("", [])


class HowToShowResultsDialog(Dialog):
    """Asks user how he wants his results to be presented
    Gets an ask action"""
    def __init__(self, show_options):
        assert type(show_options) is list and len(show_options)
        super().__init__()
        self.options = show_options

    def say(self):
        return Ask(
            "How do you wish to visualize the file?",
            self.options,
            self.options[0])


class ErrorDialog(Dialog):
    """Tells user that the request wasn't understood.
    Gets a talk action"""
    def say(self):
        return Ask(
            ("Command could not be interpreted.\nMake sure to use the format\n"
            + "save|show|update|remove [-options] <filepath> [-options]"),
            [])
