class Command:
    """
    Command interface created by the search engine to be sent to the file
    handler, avoiding further propagation of the request. If result is False,
    command failed. If None, command not processed yet.
    file_identifier : str : file id or path
    result : Any : result of the command, to be updated by the file handler
    """
    file_identifier = ''
    result = None
    def __init__(self, file_identifier: str) -> None:
        self.file_identifier = file_identifier


class CreateCommand(Command):
    """
    Command to create file. file_identifier contains id of file and
    new_file_path contains path to file to be added.
    result contains True for success, False for fail.
    """
    new_file_path = ''


class ReadCommand(Command):
    """
    Read command to return a path of a file. file_identifier contains id of file
    and result contains path to file, or False for fail.
    """
    pass


class UpdateCommand(CreateCommand):
    """
    Command to update file entry. file_identifier contains id of file to be
    updated and new_file_path contains path of file to take the place.
    result contains True for success and False for fail.
    """
    pass


class DeleteCommand(Command):
    """
    Delete command to delete saved file. file_identifier contains id of the file
    and result contains True for success, or False for fail.
    """
    pass
