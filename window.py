# Import modules
import PySimpleGUI as sg
import threading
import pandas as pd
from readwrite import *

# Let's get classy
class Window:
    def __init__(self):
        self.calculate_tab_layout = [
            # Calculate button
            [sg.Button(
                "Calculate", 
                key = "-CALCULATE-", 
                expand_x = True, 
                expand_y = True)],
            # Output field
            [sg.Column([[
                sg.Multiline(
                    size = (50, 8), 
                    key = '-OUTPUT1-', 
                    reroute_stdout = True,
                    expand_x = True, 
                    expand_y = True)]], 
                    justification = 'b', 
                    expand_x = True, 
                    expand_y = True)]]
        self.sort_tab_layout = [
            # Sort button
            [sg.Button(
                "Sort", 
                key = "-SORT-", 
                expand_x = True, 
                expand_y = True),
            # Radio buttons for sorting order
                sg.Radio(
                    'Ascending', 
                    "RADIO1", 
                    default = True, 
                    key = '-ASC-', 
                    expand_x = True, 
                    expand_y = True), 
                sg.Radio(
                    'Descending',
                    "RADIO1",
                    key = '-DESC-', 
                    expand_x = True, 
                    expand_y = True)],
            # Output field
            [sg.Column([[
                sg.Multiline(
                    size = (50, 8),
                    key = '-OUTPUT2-', 
                    reroute_stdout = True,
                    expand_x = True, 
                    expand_y = True)]], 
                    justification = 'b', 
                    expand_x = True, 
                    expand_y = True)]]
        self.layout = [
            # I never know what to say here
            [sg.Text("Let's try to save some time together:", 
                expand_x = True, 
                expand_y = True)],
            # File selection
            [sg.Input(
                key = '-FILE-', 
                enable_events = True, 
                # default_text = "Click Browse to select", 
                expand_x = True, 
                expand_y = True), 
            # Browse button
            sg.FileBrowse(
                file_types = (("CSV Files", "*.csv"),))],
            # Dropdown for headers
            [sg.Combo(
                [], 
                size = (10, 1), 
                key = '-HEADERS-', 
                enable_events = True)],
            # Tab group
            [sg.TabGroup(
                [[sg.Tab(
                    'Calc', 
                    self.calculate_tab_layout, 
                    expand_x = True, 
                    expand_y = True),
                sg.Tab(
                    'Sort', 
                    self.sort_tab_layout, 
                    expand_x = True, 
                    expand_y = True)]], 
                expand_x = True, 
                expand_y = True)]]
        self.window = sg.Window(
            'CSV Analysis Navigation and Data Optimization Resource', 
            self.layout,
            size = (470, 300))
        
    def run(self):
        w = self.window

        


        while True:
            event, values = w.read()
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break
            elif event == '-FILE-':
                if values['-FILE-']:
                    df = pd.read_csv(
                        values['-FILE-'], 
                        nrows = 0)
                    headers = df.columns.tolist()
                    max_length = max(len(header) for header in headers)
                    w['-HEADERS-'].update(
                        values = headers, 
                        size = (max_length + 2, None), 
                        set_to_index = 0)
            elif event == '-SORT-':
                threading.Thread(
                    target = DoStuff.sort_values, 
                    args = (values, self.print_to_outputs), 
                    daemon = True).start()
            elif event == '-CALCULATE-':
                threading.Thread(
                    target = DoStuff.calculate, 
                    args = (values, self.print_to_outputs), 
                    daemon = True).start()


        w.close()

    def print_to_outputs(self, *args, **kwargs):
        self.window['-OUTPUT1-'].print(*args, **kwargs)
        self.window['-OUTPUT2-'].print(*args, **kwargs)
