# Import modules
import pandas as pd



# Let's get classy
class DoStuff:
    def __init__(self):
        pass

    # Function to sort values
    def sort_values(values, print):
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
    def calculate(values, print):
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
        except:
            # If it fails, try to perform the following non-numeric operations
            # Minimum value
            min_value = df[selected_column].min()
            print(f'Minimum Value: {min_value}')
            # Maximum value
            max_value = df[selected_column].max()
            print(f'Maximum Value: {max_value}')
        # Return the values
        return min_value, mean_value, max_value