# Import modules
import PySimpleGUI as sg 
import pandas as pd
import os
import threading


# Get the current directory
current_directory = os.getcwd()

# Function to sort values
def sort_values(values):
    print('Reading file...')
    df = pd.read_csv(values['-FILE-'])
    # Determine the sort order
    sort_order = 'asc' if values['-ASC-'] else 'desc'
    print(f'Sorting file by {values["-HEADERS-"]} in {sort_order}ending order...')
    # Sort the file
    sorted_df = df.sort_values(
        by = values['-HEADERS-'], 
        ascending = values['-ASC-'])
    # Save the sorted file
    sorted_df.to_csv(
        values['-FILE-'], 
        index = False)
    print(f'File sorted in {sort_order}ending order')

# Function to calculate values
def calculate(values):
    # Figure out what the selected column is
    selected_column = values['-HEADERS-']
    # Read the selected column
    df = pd.read_csv(
        values['-FILE-'], 
        usecols = [selected_column])
    # Looks at numeric columns and non-numeric columns and treats them differently
    try:
        # Try to convert the column to numeric to see if it's a numeric column
        df[selected_column] = pd.to_numeric(df[selected_column])
        # If it succeeds, try to perform the following numeric operations
        # Minimum value
        min_value = df[selected_column].min().round(3)
        try:
            min_value = f'{min_value:,}'
        except:
            pass
        print(f'Minimum Value: {min_value}')
        # Average value
        mean_value = df[selected_column].mean().round(3)
        try:
            mean_value = f'{mean_value:,}'
        except:
            pass
        print(f'Average Value: {mean_value}')
        # Maximum value
        max_value = df[selected_column].max().round(3)
        try:
            max_value = f'{max_value:,}'
        except:
            pass
        print(f'Maximum Value: {max_value}')
        # Sum total
        sum_total = df[selected_column].sum().round(3)
        try:
            sum_total = f'{sum_total:,}'
        except:
            pass
        print(f'Sum Total: {sum_total}')
        # Value count
        value_count = df[selected_column].count()
        try:
            value_count = f'{value_count:,}'
        except:
            pass
        print(f'Value Count: {value_count}')
    except ValueError:
        # If the conversion fails, perform categorical operations
        unique_values = df[selected_column].unique()
        # Differentiates between columns with small and large number of unique values
        if unique_values.size <= 25:  # Arbitrary threshold
            for value in unique_values:
                count = df[selected_column].value_counts()[value]
                print(f'{selected_column}: {value} \nTimes counted: {count}\n')
        else:
            count_unique = len(unique_values)
            print(f'Unique values: {count_unique}')

# Tab 2 - Sort
sort_tab_layout = [
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
            key = '-OUTPUT1-', 
            expand_x = True, 
            expand_y = True)]], 
            justification = 'b', 
            expand_x = True, 
            expand_y = True)]
]

# Tab 1 - Calculate
calculate_tab_layout = [
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
            key = '-OUTPUT2-', 
            expand_x = True, 
            expand_y = True)]], 
            justification = 'b', 
            expand_x = True, 
            expand_y = True)]
]

# Main window layout
layout = [
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
         file_types = (("CSV Files", "*.csv"),), 
         initial_folder = current_directory)],
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
            calculate_tab_layout, 
            expand_x = True, 
            expand_y = True),
        sg.Tab(
            'Sort', 
            sort_tab_layout, 
            expand_x = True, 
            expand_y = True)]], 
        expand_x = True, 
        expand_y = True)]
]

# Redirect print to the Multiline elements
def print_to_outputs(*args, **kwargs):
    window['-OUTPUT1-'].print(*args, **kwargs)
    window['-OUTPUT2-'].print(*args, **kwargs)

# Replace standard print with print_to_outputs
print = print_to_outputs

window = sg.Window(
    'CSV Analysis Navigation and Data Optimization Resource', 
    layout,
    size = (470, 300))

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == '-FILE-':
        if values['-FILE-']:
            df = pd.read_csv(
                values['-FILE-'], 
                nrows = 0)
            headers = df.columns.tolist()
            max_length = max(len(header) for header in headers)
            window['-HEADERS-'].update(
                values = headers, 
                size = (max_length + 2, None), 
                set_to_index = 0)
    elif event == '-SORT-':
        threading.Thread(
            target = sort_values, 
            args = (values,), 
            daemon = True).start()
    elif event == '-CALCULATE-':
        threading.Thread(
            target = calculate, 
            args = (values,), 
            daemon = True).start()


window.close()