from command import Command

if __name__ == "__main__":
    while True:
        command = Command.prompt_command()

        if command == "1":
            Command.print_crafted_products()
        elif command == "2":
            Command.print_flipped_products()
        elif command == "3":
            Command.print_recipe()
        elif command == "4":
            Command.monitor_auctions()
        elif command == "q" or command == "Q":
            break
