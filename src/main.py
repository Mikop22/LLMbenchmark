import json
from data_loader import load_dataset
from api_integration import verify_statement_with_api, parse_api_response
from evaluation import score_classification, calculate_total_score

def main():
    """
    Main function to run the LLM news verification benchmark.
    """
    api_key = "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"  # Replace with your actual API key
      # Replace with your dataset path

    # 1. Load data
    df = load_dataset()

    # 2. Iterate through statements and get predictions
    results = []
    for index, row in df.iterrows():
        statement = row["statement"]
        true_label = row["true_label"]

        print(f"Verifying statement {index + 1}/{len(df)}: {statement}")

        # 3. Call API and parse response
        api_response = verify_statement_with_api(statement, api_key)
        parsed_response = parse_api_response(api_response)

        predicted_label = parsed_response["predicted_label"]
        api_response_summary = parsed_response["api_response_summary"]

        # 4. Score the prediction
        score = score_classification(true_label, predicted_label)

        results.append({
            "statement_id": index + 1,
            "statement": statement,
            "true_label": true_label,
            "predicted_label": predicted_label,
            "api_response_summary": api_response_summary,
            "score": score
        })
        print(f"Predicted Label: {predicted_label}, Summary: {api_response_summary}")

    # 5. Calculate total score
    total_score = calculate_total_score(results)
    final_percentage_score = (10 - total_score / 10 ) * 100

    # 6. Prepare output data
    output_data = {
        "final_score": final_percentage_score,
        "predictions": results
    }

    # 7. Save results to JSON file
    output_filepath = "data"  # Replace with your desired output path
    try:
        with open(output_filepath, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"Results saved to {output_filepath}")
    except Exception as e:
        print(f"Error saving results to JSON: {e}")

main()