from command import Command

if __name__ == "__main__":
    while True:
        command = Command.prompt_command()

        if command == "1":
            pass
        elif command == "q" or command == "Q":
            break
