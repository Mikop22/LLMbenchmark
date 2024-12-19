
def score_classification(truth_score, confidence_score):
    """
    Calculates the score for a single prediction based on the scoring matrix.

    """
    if confidence_score is None:
        return 0.00

    return ((truth_score - confidence_score)/truth_score) * 100

def calculate_total_score(results):
    """
        Calculates the total score for all predictions.

        """
    if not results:
        print("Error: No results provided to calculate total score.")
        return None

    total_score = 0

    for result in results:
        score = abs(result.get("score"))
        if score is None:
            print("Error:")
            return None

        total_score += score

    return total_score