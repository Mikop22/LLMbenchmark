
import re

from openai import OpenAI

def verify_statement_with_api(statement,apikey):
    """
    Sends a statement to the Perplexity AI API for verification.

    Args:
        statement: The statement to verify.
        api_key: Your Perplexity AI API key.
        max_retries: Maximum number of retries if API fails.
        retry_delay: Time to wait in seconds before retrying.

    Returns:
        The raw text response from the API, or None if the request fails.
    """

    YOUR_API_KEY = apikey

    messages = [
    {
        "role": "system",
        "content": (
            "You are a the perfect product finder, you will be given a will its specifications each seperated by commas. Some of the specifiation could be fake, Your job is to classify the nature of the entire statement using 2 metrics in your output, Firstly any 1 of the following: Real, Mostly Real, Mostly Fake, or Fake, do not obsess over how specific a statement is just evaluate the blanket truth of it, if it is true consider that fully accurate. finally if the statement has any inaccuracy explain which part "
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
    Parses the raw text response from the Perplexity AI API.

    Args:
        response_text: The raw text response from the API.

    Returns:
        A dictionary containing:
        - predicted_label: The predicted label (Real, Mostly Real, etc.).
        - confidence_score: The confidence score (if extracted).
        - api_response_summary: A summary of the evidence.
    """

    if not response_text:
        return {
            "predicted_label": None,
            "confidence_score": None,
            "api_response_summary": "API request failed."
        }

    # Extract predicted label using regex (example)
    # You'll need to adapt these patterns based on the actual API response format
    predicted_label_match = re.search(r"(Real|Mostly Real|Mostly Fake|Fake)", response_text, re.IGNORECASE)
    predicted_label = predicted_label_match.group(0) if predicted_label_match else None

    # Extract confidence score using regex (example)
    confidence_score_match = re.search(r"confidence(?: score)?:?\s*([\d.]+)", response_text, re.IGNORECASE)
    confidence_score = float(confidence_score_match.group(1)) if confidence_score_match else None
    if confidence_score is not None and confidence_score > 1:
        confidence_score /= 100

    # Extract summary (example - assuming it's the rest of the text)
    summary_start = 0
    if predicted_label_match:
        summary_start = predicted_label_match.end()
    if confidence_score_match:
        summary_start = max(summary_start, confidence_score_match.end())

    api_response_summary = response_text[summary_start:].strip()

    # If predicted_label is not found use thresholds
    print(predicted_label)
    print(confidence_score)
    print(api_response_summary)
    return {
        "predicted_label": predicted_label,
        "confidence_score": confidence_score,
        "api_response_summary": api_response_summary
    }

