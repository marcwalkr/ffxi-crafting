from command import Command

if __name__ == "__main__":
    while True:
        command = Command.prompt_command()

        if command == "1":
            Command.add_item()
        elif command == "2":
            Command.add_vendor()
        elif command == "3":
            Command.add_vendor_item()
        elif command == "4":
            Command.add_recipe()
        elif command == "5":
            Command.remove_item()
        elif command == "6":
            Command.remove_vendor()
        elif command == "7":
            Command.remove_vendor_item()
        elif command == "8":
            Command.remove_auction_item()
        elif command == "9":
            Command.remove_recipe()
        elif command == "10":
            Command.update_vendor_price()
        elif command == "11":
            Command.update_auction_items()
        elif command == "12":
            Command.print_products()
        elif command == "q" or command == "Q":
            break
