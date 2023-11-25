import PySimpleGUI as sg
import webbrowser
from typing import List

from tester.tester import Tester

APP_NAME = "Dizzy Tester"
OUT_WINDOW = "OUTPUT"
EXIT = "EXIT"
RUN = "RUN"
FOLDER_KEY = "FOLDER"
SOL_KEY = "SOL"
TITLE = f"{APP_NAME}🤙"


def run_tests(problem_path: str, sol_path: str = "") -> List[str]:
    tester = Tester(problem_path, sol_path)
    result = tester.evaluate()
    tester.close()
    return result


def set_layout() -> List:
    layout = [
        [sg.Text(APP_NAME, font=("Arial Bold", 15), justification="center")],  # Title

        [sg.Text("Open problem directory:")],
        [sg.InputText(key=FOLDER_KEY), sg.FolderBrowse()],

        [
            sg.Text("Open solution file:"),
            sg.Text(
                "(if not provided, we'll just take /sol/sol.{cpp/py})",
                text_color="red",
            ),
        ],
        [sg.InputText(key=SOL_KEY), sg.FileBrowse()],

        [sg.Button("Check solution", key=RUN)],  # Run button

        [sg.Output(size=(60, 20), key=OUT_WINDOW)],  # Output log

        [
            sg.Push(),
            sg.Button(
                EXIT,
            ),
        ],

        [
            sg.Text(
                "Made by Diego🤙, 2023",
                font=("Helvetica", 9),
                enable_events=True,
                key="GITHUB",
            )
        ],
    ]
    return layout


def main_loop(window) -> None:
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == EXIT:
            break
        elif event == RUN:
            window[OUT_WINDOW].update("")
            problem_path = values[FOLDER_KEY]
            sol_path = values[SOL_KEY]
            if problem_path:
                result = run_tests(problem_path, sol_path)
                for line in result:
                    window[OUT_WINDOW].print(line, colors=("green" if "OK" in line else "red"))
            else:
                sg.Popup("No directory selected!")
        elif event == "GITHUB":
            webbrowser.open("https://github.com/diegoPenguino/Dizzy-tester")


def main():
    sg.theme("BluePurple")
    layout = set_layout()

    window = sg.Window(
        TITLE,
        layout,
        margins=(50, 50),
        icon='img/ChillyWilly.ICO'
    )

    main_loop(window)
    window.close()


if __name__ == "__main__":
    main()
