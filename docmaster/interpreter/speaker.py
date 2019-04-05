import os

import actions

class Speaker:
    def __init__(self, request, results=None):
        self.request = request
        self.results = results
        dialog = self.request.get_dialog()
        if results is not None:
            self.handle_show_action()
        elif self.request.action is actions.AskAction:
            self.handle_ask_action(dialog)
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
                print(bytes(answer))
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
        os.system('cat ' + self.results)
