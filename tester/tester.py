import os
import subprocess
from timeit import default_timer as timer
import sys
import re
from typing import List

from .Constants import *


class Tester:
    def __init__(self, problem_path: str, sol_path=""):
        self.problem_path = problem_path

        self.lang = "cpp" if not sol_path else sol_path.split(".")[-1]

        self.sol_path = (
            f"{problem_path}/sol/sol.{self.lang}" if not sol_path else sol_path
        )

        self.input_files = [file for file in os.listdir(f"{problem_path}/input")]
        self.output_files = [file for file in os.listdir(f"{problem_path}/output")]

        self.compile_command = COMPILE_COMMANDS[self.lang]
        if self.lang == "cpp":
            self.compile_command[1] = self.sol_path

        self.compile()

    def compile(self) -> None:
        if self.compile_command:
            subprocess.run(self.compile_command, shell=True)

            self.compiled_name = self.compile_command[-1]
            self.compiled_name += ".exe" if sys.platform == "win32" else ""

        print("Compiled successfully!")

    def run(self, input_file: str) -> str:
        with open(f"{self.problem_path}/input/{input_file}", "r") as in_file:
            in_content = in_file.read()

        start = timer()
        out_content = (
            subprocess.check_output(
                self.compiled_name, shell=True, text=True, input=in_content
            )
            if self.lang == "cpp"
            else subprocess.check_output(
                ["python", self.sol_path], shell=True, text=True, input=in_content
            )
        )
        time_taken = timer() - start

        return out_content, time_taken

    def check_testcase(self, input_file: str) -> str:
        out_content, time_taken = self.run(input_file)

        try:
            number = self.get_input_id(input_file)
        except AssertionError as e:
            print(e)
            return ""

        try:
            with open(
                f"{self.problem_path}/output/output{number}.txt", "r"
            ) as out_file:
                out_correct = out_file.read()
        except FileNotFoundError as e:
            print(e)
            return ""

        verdict = "OK" if self.check_OK(out_correct, out_content) else "WA"
        #  This part should be improved later, adding TLE, RE, etc.
        # implementing another function is recommended

        return f"Case {number}: \t{verdict}, time = {time_taken}"

    def evaluate(self) -> List[str]:
        result = [self.check_testcase(input_file) for input_file in self.input_files]
        return result

    def close(self) -> None:
        if self.lang == "cpp":
            try:
                os.remove(self.compiled_name)
            except FileNotFoundError:
                pass

    @staticmethod
    def get_input_id(input_file: str) -> int:
        match = re.search(r"input(\d+)", input_file)

        assert match, f"Wrong format used in file {input_file}."

        return int(match.group(1))

    @staticmethod
    def check_OK(out_correct: str, out_user: str) -> bool:
        return (
            out_correct == out_user
            or out_user[:-1] == out_correct
            or out_correct[:-1] == out_user
        )
