from Dependencies import *


def main():
    while True:
        print_welcome_message()
        print_options_menu()

        user_choice = input(Fore.CYAN + Style.BRIGHT + "Enter your choice (1-8): ")

        if user_choice == "1":
            encode_text_to_brainfuck()

        if user_choice == "2":
            encode_and_save_to_file()

        elif user_choice == "3":
            decode()

        elif user_choice == "4":
            decode_file()

        elif user_choice == "5":
            generate_random_code()

        elif user_choice == "6":
            simulate_tape_dynamics()
       
        elif user_choice == "7":
            print_help_menu()

        elif user_choice == "8":
            print(Fore.YELLOW + Style.BRIGHT + "Goodbye")
            break

        else:
            exit()

        input(Fore.CYAN + Style.BRIGHT + "Press Enter to continue...")
        clear_screen()


if __name__ == "__main__":
    main()
