#!/usr/bin/env python3

"""
docmaster __main__
Starts the software up.
"""

import os
import sys

# Temporarily adds lib folder to path, so imports are direct.
sys.path.append(__loader__.path.replace("/__main__.py","") + "/lib/")

import interpreter.userinterface as ui

if __name__ == '__main__':
    try:
        command = [] #type: list[str]
        for term in sys.argv:
            command.append(term)
        user_interface = ui.UserInterface(command)
        user_interface.handle_request()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\nTerminated.")
