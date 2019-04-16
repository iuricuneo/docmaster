class Action:
    """The concretions of Action never become objects!"""
    pass


class WaitForHandlingAction(Action):
    """Object just created, needs to be handled.
    If this appears again, it will be cause an exception."""
    pass


class ShowAction(Action):
    """Show item to user"""
    pass


class SearchAction(Action):
    """Search for file, request can be forwarded to searchengine"""
    pass


class AskAction(Action):
    """Something will be written and we will get an answer"""
    pass


class TalkAction(Action):
    """Something will be written without answer"""
    pass


class DoNothingAction(Action):
    """Nothing to be done, object can be deleted"""
    pass


class ProcessAction(Action):
    """Object needs to be processed"""
    pass
