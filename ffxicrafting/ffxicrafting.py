from command import Command

if __name__ == "__main__":
    while True:
        command = Command.prompt_command()

        if command == "1":
            Command.print_synth_table()
        elif command == "2":
            Command.print_recipe()
        elif command == "3":
            Command.simulate_synth()
        elif command == "q" or command == "Q":
            break
