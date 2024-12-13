import pandas as pd

def load_csv(filepath):
    """
    Loads a CSV file into a pandas DataFrame.
    Raises an exception if file not found or CSV is invalid.
    """
    data = pd.read_csv(filepath)
    return data

def save_csv(data, filepath):
    """
    Saves a pandas DataFrame to a CSV file.
    """
    data.to_csv(filepath, index=False) # What is this one doing?
