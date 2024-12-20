import json
from data_loader import load_dataset
from api_integration import verify_statement_with_api, parse_api_response
from evaluation import score_classification, calculate_total_score

def main():
    """
    Main function to run the LLM verification benchmark.
    """
    api_key = ""  # Replace with your actual API key
      # Replace with your dataset path

    # 1. Load data
    df = load_dataset()

    # 2. Iterate through statements and get predictions
    results = []
    for index, row in df.iterrows():
        statement = row["statement"]
        truth_score = row["truth_score"]

        print(f"Verifying statement {index + 1}/{len(df)}: {statement}")

        # 3. Call API and parse response
        api_response = verify_statement_with_api(statement, api_key)
        parsed_response = parse_api_response(api_response)

        confidence_score = parsed_response["confidence_score"]
        api_response_summary = parsed_response["api_response_summary"]

        # 4. Score the prediction (relative error percentage)
        score = score_classification(truth_score, confidence_score)

        results.append({
            "statement_id": index + 1,
            "statement": statement,
            "truth_score": truth_score,
            "confidence_score": confidence_score,
            "api_response_summary": api_response_summary,
            "score": score
        })
        print(f"Predicted Label: {confidence_score}, Summary: {api_response_summary}")

    # 5. Calculate total score (lower is better)
    total_score = calculate_total_score(results)

    # 6. Prepare output data
    output_data = {
        "final_score": total_score,
        "predictions": results
    }

    # 7. Save results to JSON file
    output_filepath = "data/results.json"  # Replace with your desired output path
    try:
        with open(output_filepath, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"Results saved to {output_filepath}")
    except Exception as e:
        print(f"Error saving results to JSON: {e}")

main()
