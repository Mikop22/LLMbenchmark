1. **Clone the repository:**


2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    Or
        ```bash
    pip3 install -r requirements.txt
    ```
    Create a `requirements.txt` file containing:
        ```
        pandas
        requests
        ```

## Configuration

1. **API Key:**
    *   Obtain an API key from Perplexity AI or use another LLM
    *   Replace `YOUR_PERPLEXITY_AI_API_KEY` in `src/main.py` with your actual API key.

2. **API Endpoint:**
    *   Verify the Perplexity AI API endpoint in `src/api_integration.py`. Update it if necessary or using another LLM

3. **Dataset:**
    *   Place your dataset of product specifications in `data/statements.csv`.
    *   The CSV file should have the following columns:
        *   `specification` (the product spec being evaluated)
        *   `truth_score` (Real, Mostly Real, Mostly Fake, Fake)

4. **Regex Patterns:**
    *   Carefully review and adjust the regular expression patterns in `src/api_integration.py`'s `parse_api_response` function to match the specific format of the Perplexity AI API's text output. This is crucial for accurate information extraction.

## Usage

1. Navigate to the `src` directory:

    ```bash
    cd src
    ```

2. Run the main script:

    ```bash
    python main.py
    ```
    Or
    ```bash
    python3 main.py
    ```

## Output

The benchmark results will be saved in `results/results.txt`. The file will contain:

*   **Final Score:** The overall accuracy score of the LLM in verifying product specifications.
*   **Detailed Results:** For each specification:
    *   `Statement ID`
    *   `Statement` (Product Specification)
    *   `Truth score`
    *   `Confidence Score` (if available)
    *   `API Response Summary`
    *   `Score`

## Documentation

### `data_loader.py`

This module handles loading and preprocessing of the product specification dataset.

**Functions:**

*   `load_dataset(filepath)`: Loads the dataset from the specified CSV file path.
*   `preprocess_data(df)`: Performs any necessary preprocessing on the dataset (e.g., data cleaning, normalization). Currently a placeholder for future extensions.

### `api_integration.py`

This module manages the interaction with the Perplexity AI API.

**Functions:**

*   `parse_api_response(response_text)`: Parses the raw text response from the API using regular expressions to extract the predicted label, confidence score (if available), and a summary of the evidence.
### `evaluation.py`

This module contains the logic for evaluating the LLM's predictions.

**Functions:**

*   `score_classification(truth_score, confidence_score)`: Calculates the score for a single prediction based on a predefined scoring matrix.
*   `calculate_total_score(results)`: Computes the total score across all predictions in the dataset.

### `main.py`

This is the main script that orchestrates the entire benchmark process.

**Functions:**

*   `main()`:
    1. Loads and preprocesses the dataset using `data_loader.py`.
    2. Iterates through each product specification in the dataset.
    3. Sends the specification to the Perplexity AI API using `api_integration.py`.
    4. Parses the API response using `api_integration.py`.
    5. Scores the prediction using `evaluation.py`.
    6. Accumulates the results and calculates the final score.
    7. Writes the detailed results and final score to `results/results.txt`.

## Contributing

Contributions to this project are welcome! Please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with clear and concise messages.
4. Open a pull request, describing the changes you've made.


---
