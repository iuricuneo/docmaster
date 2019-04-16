"""
Listener module.

Listener is a function responsible for receiving a full user command and
interpreting it into a request with the given options.

It is a function and has a behaviour similar to the one of the speaker. To call,
use:
request = listener.Listener(command)

Options so far are:
v - verbose
f - force
---
Commands (in lib/interpretstrategies):
save
show
update
remove
"""

from typing import List

import interpretstrategies as strat


def Listener(command: List[str]): # (...) -> Request:
    """To be called by the user interface, it will receive a command and handle
    it, returning a request to it."""

    strategy = strat.InterpretingStrategy()
    pure_command = strategy.get_command(command)

    map = {
        'save': strat.CreateEntryStrategy,
        'show': strat.ReadEntryStrategy,
        'update': strat.UpdateEntryStrategy,
        'remove': strat.DeleteEntryStrategy,
        'error': strat.ErrorStrategy}

    return map[pure_command]().get_request(command)
