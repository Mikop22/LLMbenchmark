
def score_classification(true_label, predicted_label):
    """
    Calculates the score for a single prediction based on the scoring matrix.

    Args:
        true_label: The true label of the statement.
        predicted_label: The label predicted by the model.

    Returns:
        The score for the prediction (a float between 0 and 1).
    """
    if predicted_label is None:
        return 0.0

    scoring_matrix = {
        "Fake": {"Fake": 1, "Mostly Fake": 0.75, "Mostly Real": 0.25, "Real": 0},
        "Mostly Fake": {"Fake": 0.75, "Mostly Fake": 1, "Mostly Real": 0.5, "Real": 0},
        "Mostly Real": {"Fake": 0, "Mostly Fake": 0.5, "Mostly Real": 1, "Real": 0.75},
        "Real": {"Fake": 0, "Mostly Fake": 0.25, "Mostly Real": 0.75, "Real": 1},
    }

    try:
        return scoring_matrix[true_label][predicted_label]
    except KeyError:
        print(f"Error: Invalid label combination: True - {true_label}, Predicted - {predicted_label}")
        return 0
print(score_classification("Fake","Mostly Real"))

data = {}

def calculate_total_score(results):
    """
        Calculates the total score for all predictions.

        Args:
            results (list): List of dictionaries, each containing 'true_label' and 'predicted_label'.

        Returns:
            float: The total score, or None if results is empty.
        """
    if not results:
        print("Error: No results provided to calculate total score.")
        return None

    total_score = 0
    num_statements = len(results)

    for result in results:
        true_label = result.get('true_label')
        predicted_label = result.get('predicted_label')
        if true_label is None or predicted_label is None:
            print("Error: 'true_label' or 'predicted_label' missing in results.")
            return None

        total_score += score_classification(true_label, predicted_label)

    return total_score