from colorama import Fore, init

# Auto reset style with colorama
init(autoreset=True)


class Logger:
    def __init__(self) -> None:
        pass

    @staticmethod
    def print_yello(text):
        print(Fore.YELLOW + text)

    @staticmethod
    def print_cyan(text):
        print(Fore.CYAN + text)

    @staticmethod
    def print_red(text):
        print(Fore.RED + text)

    @staticmethod
    def print_green(text):
        print(Fore.GREEN + text)
