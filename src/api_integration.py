
import re

from openai import OpenAI

def verify_statement_with_api(statement,apikey):
    """

    Args:
        statement: The statement to verify.
        api_key: LLM API key.

    Returns:
        The raw text response from the API, or None if the request fails.
    """

    YOUR_API_KEY = apikey

    messages = [
    {
        "role": "system",
        "content": (
            "You are a the perfect product finder, you will be given a product and its specifications each seperated by commas. Some of the specifiations could be fake, Your job is to classify the nature of the entire statement using a metric called confidence score from 0.00 to 1.00, do not obsess over how specific a statement is just evaluate the blanket truth of it, if it is true consider that fully accurate and remove 0 points from the final score, for each spec you find to be a outright lie subtract 0.05 from the final confidence score. output in the following format: Confidence Score:, follow by you reasons for the score you gave "
        ),
    },
    {   
        "role": "user",
        "content": (
            str(statement)
        ),
    },
    ]

    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="llama-3.1-sonar-large-128k-online",
        messages=messages,  
    )
    return str(response)
def parse_api_response(response_text):
    """
    Parses the raw text response from the API

    Args:
        response_text: The raw text response from the API.

    Returns:
        A dictionary containing:
        - confidence_score: The confidence score (if extracted).
        - api_response_summary: A summary of the evidence.
    """

    if not response_text:
        return {
            "truth_score": None,
            "confidence_score": None,
            "api_response_summary": "API request failed."
        }

    # Extract confidence score using regex (example)
    confidence_score_match = re.search(r"Confidence Score:\s*([\d.]+)", response_text, re.IGNORECASE)
    confidence_score = float(confidence_score_match.group(1)) if confidence_score_match else None
    # Extract summary (example - assuming it's the rest of the text)
    summary_start = 0
    if confidence_score_match:
        summary_start = max(summary_start, confidence_score_match.end())

    api_response_summary = response_text[summary_start:].strip()

    # If predicted_label is not found use thresholds
    print(confidence_score)
    print(api_response_summary)
    return {
        "confidence_score": confidence_score,
        "api_response_summary": api_response_summary
    }

