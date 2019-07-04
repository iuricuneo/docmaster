"""
Speaker class.

This class is responsible for handling communication with the user. It will ask
a question from a dialogues.Ask object and get an answer, if any, to be recorded
in the dialogues.Dialog object of each request. This will then be processed
wherever it is needed.

Much like the listener, it works as a function. Call with speaker.Speaker(req) .
"""

import os

import actions


class Speaker:
    """Speaker class. Called from the user interface whenever needed to print
    something or get user input. Received a request to handle, works pretty much
    like a function, invoke with speaker.Speaker(request) ."""
    def __init__(self, request):
        self.request = request
        dialog = self.request.get_dialog()
        if self.request.action is actions.AskAction:
            self.handle_ask_action(dialog)
        elif self.request.action is actions.TalkAction:
            self.handle_talk_action(dialog)
        elif request.results is not None:
            self.handle_show_action()
        else:
            self.handle_talk_action(dialog)

    def handle_talk_action(self, dialog):
        """Handles a request with talk action.
        :dialog_text: Dialog
        """
        print(dialog.say().text)

    def handle_ask_action(self, dialog):
        """Handles a request with ask action.
        :dialog_text: Dialog
        """
        dialog_text = dialog.say() #type: dialogues.Ask
        line_to_print = dialog_text.text
        num_opts = len(dialog_text.options)
        tmp = ""
        if num_opts:
            tmp += " ["
            if dialog_text.pref is not None:
                dialog_text.options.remove(dialog_text.pref)
                dialog_text.options.insert(0, dialog_text.pref.upper())
            for option in dialog_text.options:
                tmp += option + "|"
            tmp = tmp[:-1] + "] "
        line_to_print += tmp
        answer = input(line_to_print)

        answer = answer.lower()
        for ind in range(num_opts):
            dialog_text.options[ind] = dialog_text.options[ind].lower()

        if num_opts:
            if answer == '' and dialog_text.pref is not None:
                answer = dialog_text.pref.lower()
            line_to_print = (
                "Sorry, I could not understand you... \n" + line_to_print)
            while answer not in dialog_text.options:
                answer = input(line_to_print).lower()
                if answer == '' and dialog_text.pref is not None:
                    answer = dialog_text.pref.lower()
                print(answer)
        else:
            line_to_print = (
                "Please say something to help me...\n" + line_to_print)
            while answer == '':
                answer = input(line_to_print).lower()

        dialog.hear((line_to_print, answer))
        dialog.has_been_fulfilled()

    def handle_show_action(self):
        """Handles a request with show action.
        :dialog: str
        """
        if not self.request.flags['error']:
            os.system('cat ' + self.request.results["orig_name"])
        else:
            print("Error found processing request.")
            print(self.request.results)
