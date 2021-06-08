import sys


class Tui:
    def __init__(self, controller):
        self.controller = controller

    def process_input(self, input):
        inputs = input.split()

        if len(inputs) >= 2:
            if inputs[0] == "connect":
                self.controller.connect(inputs[1])
            elif inputs[0] == "stups":
                self.controller.stups(inputs[1])
            elif inputs[0] == "chat":
                self.controller.start_chat(inputs[1], inputs[2])
            else:
                print("ungültige Eingabe")

        elif len(inputs) == 1:
            if inputs[0] == "quit":
                print("Auf Wiedersehen!")
                sys.exit(0)
            elif inputs[0] == "disconnect":
                self.controller.disconnect()
            elif inputs[0] == "broadcast":
                self.controller.broadcast()
            else:
                print("ungültige Eingabe!")
        else:
            print("ungültige eEingabe!")
