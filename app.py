import PySimpleGUI as sg
import os
import webbrowser

from tester.tester import Tester


def run_tests(problem_path: str, sol_path: str = "") -> None:
    tester = Tester(problem_path, sol_path)
    result = tester.evaluate()
    for line in result:
        print(line)
    tester.close()


TITLE = "D - tester🤙"
problem_path = ""

sg.theme("BluePurple")

layout = [
    [sg.Text("D - tester", font=("Arial Bold", 15), justification="center")],
    [sg.Text("Open problem directory:")],
    [sg.InputText(key="FOLDER"), sg.FolderBrowse()],
    [
        sg.Text("Open solution file:"),
        sg.Text(
            "(if not provided, we'll just take /sol/sol.{py/cpp})",
            text_color="red",
        ),
    ],
    [sg.InputText(key="SOL"), sg.FileBrowse()],
    [sg.Button("Check solution", key="RUN")],
    [sg.Output(size=(60, 20), key="OUTPUT")],
    [
        sg.Push(),
        sg.Button(
            "Exit",
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

window = sg.Window(
    TITLE,
    layout,
    margins=(50, 50),
)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event == "RUN":
        window["OUTPUT"].update("")
        problem_path = values["FOLDER"]
        sol_path = values["SOL"]
        if problem_path:
            run_tests(problem_path, sol_path)
        else:
            sg.Popup("No directory selected!")
    elif event == "GITHUB":
        webbrowser.open("github.com")

window.close()
