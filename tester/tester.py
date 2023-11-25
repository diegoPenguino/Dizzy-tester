import os
import subprocess
from timeit import default_timer as timer
import sys
import re
from typing import List, Tuple

from .Constants import *


class Testcase:
    def __init__(self, problem_path: str, test_id: int):
        self.input_file = f"{problem_path}/input/input{test_id}.txt"
        self.output_file = f"{problem_path}/output/output{test_id}.txt"
        self.test_id = test_id
        self.created = True

        if not os.path.exists(self.input_file) or not os.path.exists(
                self.output_file or test_id == -1
        ):
            self.created = False

    def __lt__(self, other):
        return self.test_id < other.test_id


class Tester:
    def __init__(self, problem_path: str, sol_path=""):
        self.problem_path = problem_path

        self.lang = "cpp" if not sol_path else sol_path.split(".")[-1]

        self.sol_path = (
            f"{problem_path}/sol/sol.{self.lang}" if not sol_path else sol_path
        )

        self.test_cases = [Testcase(problem_path, self.get_input_id(file)) for file in
                           os.listdir(f"{problem_path}/input")]
        self.test_cases = [test_case for test_case in self.test_cases if test_case.created]
        self.test_cases.sort()

        self.compile_command = COMPILE_COMMANDS[self.lang]
        if self.lang == "cpp":
            self.compile_command[1] = self.sol_path

            self.compiled_name = self.compile()

    def compile(self) -> str:
        subprocess.run(self.compile_command, shell=True)

        compiled_name = self.compile_command[-1]
        compiled_name += ".exe" if sys.platform == "win32" else ""

        return compiled_name

    def run(self, in_content: str) -> tuple[str, float]:
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

    def check_testcase(self, test_case: Testcase) -> str:
        with open(test_case.input_file, "r") as in_file:
            out_content, time_taken = self.run(in_file.read())

        with open(test_case.output_file, "r") as out_file:
            out_correct = out_file.read()

        verdict = "OK" if self.check_OK(out_correct, out_content) else "WA"
        # This part should be improved later, adding TLE, RE, etc.
        # implementing another function is recommended

        return f"Case {test_case.test_id}: \t{verdict}, time = {time_taken}"

    def evaluate(self) -> List[str]:
        result = [self.check_testcase(test_case) for test_case in self.test_cases]
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

        if not match:
            return -1

        return int(match.group(1))

    @staticmethod
    def check_OK(out_correct: str, out_user: str) -> bool:
        return (
                out_correct == out_user
                or (out_user[:-1] == out_correct and out_user[-1] == '\n')
                or (out_correct[:-1] == out_user and out_correct[-1] == '\n')
        )
