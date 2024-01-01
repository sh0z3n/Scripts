import random
import argparse
import os
import time
from colorama import Fore, Back, Style, init
import tkinter as tk
from tkinter import messagebox
import cProfile

pr = cProfile.Profile()
pr.enable()

init(autoreset=True)


class BrainfuckInterpreter:
    def __init__(self):
        self.tape = [0] * 30000
        self.pointer = 0
        self.brackets = {}

    def interpret(self, code, output_callback=None):
        code = self.match_brackets(code)

        i = 0
        while i < len(code):
            command = code[i]

            if command == ">":
                self.pointer += 1
            elif command == "<":
                self.pointer -= 1
            elif command == "+":
                self.tape[self.pointer] = (self.tape[self.pointer] + 1) % 256
            elif command == "-":
                self.tape[self.pointer] = (self.tape[self.pointer] - 1) % 256
            elif command == ".":
                if output_callback:
                    output_callback(chr(self.tape[self.pointer]))
                else:
                    print(Fore.CYAN + chr(self.tape[self.pointer]), end="")
            elif command == ",":
                user_input = input(Fore.YELLOW + Style.BRIGHT + "Enter a character: ")
                if user_input:
                    self.tape[self.pointer] = ord(user_input[0])
            elif command == "[" and self.tape[self.pointer] == 0:
                i = self.brackets[i]
            elif command == "]" and self.tape[self.pointer] != 0:
                i = self.brackets[i]

            i += 1

    def match_brackets(self, code):
        stack = []
        brackets = {}
        for i, char in enumerate(code):
            if char == "[":
                stack.append(i)
            elif char == "]":
                start = stack.pop()
                brackets[start] = i
                brackets[i] = start
        return brackets


def generate_random_code():
    brainfuck_characters = [">", "<", "+", "-", "[", "]", ".", ","]

    code_length = random.randint(500, 1200)

    generated_code = "".join(
        random.choice(brainfuck_characters) for _ in range(code_length)
    )

    print(Fore.YELLOW + Style.BRIGHT + "Generating random Brainfuck code...")
    print(generated_code)


def simulate_tape_dynamics(tape_size=30, steps=100):
    tape = [0] * tape_size
    pointer = 0
    for _ in range(steps):
        operation = random.choice([">", "<", "+", "-"])

        if operation == ">":
            pointer = (pointer + 1) % tape_size
        elif operation == "<":
            pointer = (pointer - 1) % tape_size
        elif operation == "+":
            tape[pointer] = (tape[pointer] + 1) % 256
        elif operation == "-":
            tape[pointer] = (tape[pointer] - 1) % 256

    print(tape)


pr.disable()
pr.print_stats(sort="cumulative")


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()


def write_to_file(file_path, data):
    with open(file_path, "w") as file:
        file.write(data)


def encode_text_to_brainfuck():
    text_input = input(
        Fore.YELLOW + Style.BRIGHT + "Enter text to encode to Brainfuck: "
    )
    brainfuck_code = text_to_brainfuck(text_input)
    print(Fore.YELLOW + Style.BRIGHT + "Generated Brainfuck code:")
    print(Fore.CYAN + Style.BRIGHT + brainfuck_code)


def text_to_brainfuck(text):
    brainfuck_code = ""
    for char in text:
        ascii_value = ord(char)
        brainfuck_code += "+" * ascii_value + ".>"
    return brainfuck_code[:-1]


def bf_to_text(bf_code):
    output = []
    bf_interpreter = BrainfuckInterpreter()
    bf_interpreter.interpret(bf_code, output.append)
    return "".join(output)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    print(
        Fore.YELLOW
        + Style.BRIGHT
        + r"""      
        ╔╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╗
        ╠╬╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╬╣
        ╠╣                                                   ╠╣
        ╠╣                                                   ╠╣
        ╠╣    _______           ______   _______  _______    ╠╣
        ╠╣   (  ____ )|\     /|(  ___ \ (  ____ )(  ___  )   ╠╣
        ╠╣   | (    )|( \   / )| (   ) )| (    )|| (   ) |   ╠╣
        ╠╣   | (____)| \ (_) / | (__/ / | (____)|| (___) |   ╠╣
        ╠╣   |  _____)  \   /  |  __ (  |     __)|  ___  |   ╠╣
        ╠╣   | (         ) (   | (  \ \ | (\ (   | (   ) |   ╠╣
        ╠╣   | )         | |   | )___) )| ) \ \__| )   ( |   ╠╣
        ╠╣   |/          \_/   |/ \___/ |/   \__/|/     \|   ╠╣
        ╠╣                                                   ╠╣
        ╠╣                                                   ╠╣
        ╠╣                                                   ╠╣
        ╠╬╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╬╣
        ╚╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╝
    """ )




def print_welcome_message():
    print_banner()
    print(Fore.CYAN + Style.BRIGHT + f"Welcome, {os.getenv('USER')}! Use a command.")


def encode_and_save_to_file():
    text_to_encode = input(
        Fore.YELLOW + Style.BRIGHT + "Enter text to encode to Brainfuck: "
    )
    encoded_result = text_to_brainfuck(text_to_encode)
    output_file = input(Fore.YELLOW + Style.BRIGHT + "Enter the output file name: ")
    write_to_file(output_file, encoded_result)
    print(Fore.YELLOW + Style.BRIGHT + f"Encoded Brainfuck saved to '{output_file}'.")


def decode():
    textdeco = input("Enter text to decode: ")
    print(decode_brainfuck(textdeco))


def decode_file():
    dec = input("Enter text to decode: ")
    c = input("what is the file name ?")
    with open(c, "w") as f:
        f.write(decode_brainfuck(dec))


def print_help_menu():
    print(Fore.CYAN + Style.BRIGHT + "Help Menu:")
    print(
        "1. Encode text to Brainfuck: Converts text to Brainfuck code and saves it to a file."
    )
    print("2. Encode text to Brainfuck: Converts text to Brainfuck code")
    print("3. Decode Brainfuck to text: Decodes Brainfuck code and prints the text.")
    print("4. Decode Brainfuck to file")
    print("5. Generate random Brainfuck code: Generates random Brainfuck code.")
    print(
        "6. Simulate Brainfuck tape dynamics: Simulates the dynamics of a Brainfuck tape."
    )
    print("7. Help: Displays this help menu.")
    print("8. Exit: Exits the program.")


def help_option():
    print_help_menu()


def decode_brainfuck(code):
    memory = [0] * 30000
    pointer = 0
    output = ""
    i = 0
    while i < len(code):
        command = code[i]

        if command == ">":
            pointer += 1
        elif command == "<":
            pointer -= 1
        elif command == "+":
            memory[pointer] = (memory[pointer] + 1) % 256
        elif command == "-":
            memory[pointer] = (memory[pointer] - 1) % 256
        elif command == "[":
            if memory[pointer] == 0:
                depth = 1
                while depth > 0:
                    i += 1
                    if code[i] == "[":
                        depth += 1
                    elif code[i] == "]":
                        depth -= 1
            else:
                i += 1
                continue
        elif command == "]":
            if memory[pointer] != 0:
                depth = 1
                while depth > 0:
                    i -= 1
                    if code[i] == "]":
                        depth += 1
                    elif code[i] == "[":
                        depth -= 1
            else:
                i += 1
                continue
        elif command == ".":
            output += chr(memory[pointer])
        elif command == ",":
            pass

        i += 1

    return output

def print_options_menu():
    print(Fore.CYAN + Style.BRIGHT + "Options:")
    print(Fore.YELLOW + Style.BRIGHT + "1. Encode text to Brainfuck")
    print("2. Encode and save to file")
    print("3. Decode Brainfuck to text")
    print("4. Decode Brainfuck to file")
    print("5. Generate Random Brainfuck Code")
    print("6. Simulate Tape Dynamics")
    print("7. Help Menu")
    print("8. Exit")
    print("~ : New function will come soon to interact with shellgpt")
