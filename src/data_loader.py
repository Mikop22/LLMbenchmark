import pandas as pd

def load_dataset():
    """
    Loads the dataset from the CSV file.

    Args:
        filepath: Path to the CSV file.

    Returns:
        A pandas DataFrame containing the dataset.
    """
    try:
        df = pd.read_csv("data/statements.csv")
        if not all(col in df.columns for col in ["statement", "truth_score"]):
            raise ValueError("CSV file must contain 'statement', 'truth_score'.")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {"data/statements.csv"}")
        return None
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

print(load_dataset())