from P2PChat.Client.Controller.Controller import Controller
from P2PChat.Client.Model.Client import Client
from P2PChat.Client.View.TUI import Tui
import colorit


def main():
    controller = Controller(Client())
    tui = Tui(controller)

    print("-------------------------------------------\n"
          "꧁༒☬𝓦𝓲𝓵𝓵𝓴𝓸𝓶𝓶𝓮𝓷 𝔃𝓾𝓻 𝓗𝓣𝓦𝓖 𝓒𝓱𝓪𝓽 𝓐𝓟𝓟☬༒꧂ \n"
          "-------------------------------------------\n"
          "connect <Name> : Anmelden\n"
          "quit           : Beenden ")
    while True:
        user_input = input()
        tui.process_input(user_input)


if __name__ == '__main__':
    main()
