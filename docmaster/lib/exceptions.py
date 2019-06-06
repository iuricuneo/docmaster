"""
Holds exceptions to be thrown in the software.
"""

class DialogUnfulfilledError(Exception):
    """Called when dialog has not been fulfilled but is set as so."""
    pass

class FileDataNotFoundError(Exception):
    """Called by searchengine.SearchTableHandler when file data has not been
    found for given ID/name."""
    pass

class TooManyFieldsFoundError(Exception):
    """Called by searchengine.SearchTableHandler when file data has returned
    more than 1 entry."""
    pass
