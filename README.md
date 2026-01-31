# LLM Product Specification Verification Benchmark

A benchmarking tool for evaluating Large Language Models (LLMs) on their ability to verify product specifications and detect incorrect or fake information in product descriptions.

## Overview

This project provides a framework for testing how accurately an LLM can identify false or misleading specifications in product descriptions. It uses a dataset of product statements (like gaming consoles, CPUs, cameras, etc.) with known truth scores and evaluates how well the LLM can detect inaccuracies.

## Features

- **Automated Product Specification Verification**: Sends product statements to an LLM API for truth verification
- **Confidence Score Evaluation**: Measures the LLM's confidence in the accuracy of product specifications
- **Scoring System**: Calculates relative error percentage to benchmark LLM performance
- **Detailed Results**: Provides comprehensive output with predictions, scores, and summaries
- **Flexible API Integration**: Currently configured for Perplexity AI but adaptable to other LLM providers

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Mikop22/LLMbenchmark.git
    cd LLMbenchmark
    ```

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
    openai
    ```

## Configuration

1. **API Key:**
    * Obtain an API key from [Perplexity AI](https://www.perplexity.ai/) or use another LLM provider
    * Replace the empty string in `src/main.py` with your actual API key:
    ```python
    api_key = "YOUR_PERPLEXITY_AI_API_KEY"
    ```

2. **API Endpoint:**
    * The project is configured to use Perplexity AI's Llama 3.1 Sonar Large model
    * To use a different LLM provider, update the API integration in `src/api_integration.py`
    * Current endpoint: `https://api.perplexity.ai`
    * Current model: `llama-3.1-sonar-large-128k-online`

3. **Dataset:**
    * Place your dataset of product specifications in `data/statements.csv`
    * The CSV file should have the following columns:
        * `statement` - The product specification text being evaluated
        * `truth_score` - A decimal value from 0.00 to 1.00 representing the accuracy (1.00 = completely true, 0.00 = completely false)
    * Example format:
    ```csv
    "statement","truth_score"
    "The PS5 pro has the following specs: WIFI 7, 2 TB SSD, USB-C...","1.00"
    "The Xbox series X has specs: 52 compute units, RDNA 2...","0.95"
    ```

4. **Regex Patterns:**
    * Review and adjust the regular expression patterns in `src/api_integration.py`'s `parse_api_response` function to match the specific format of your LLM's response
    * Current pattern extracts: `Confidence Score: X.XX`

## Usage

1. Navigate to the project root directory:

    ```bash
    cd LLMbenchmark
    ```

2. Run the main script:

    ```bash
    python src/main.py
    ```
    Or
    ```bash
    python3 src/main.py
    ```

3. The script will:
    * Load the dataset from `data/statements.csv`
    * Send each product specification to the LLM for verification
    * Parse the LLM's confidence score and reasoning
    * Calculate the relative error between the truth score and confidence score
    * Save detailed results to `data/results.json`

## Output

The benchmark results will be saved in `data/results.json`. The file will contain:

* **final_score**: The total cumulative relative error score across all predictions (lower is better)
* **predictions**: An array of detailed results for each specification:
    * `statement_id` - Sequential ID for the statement
    * `statement` - The product specification text
    * `truth_score` - The ground truth accuracy score (0.00-1.00)
    * `confidence_score` - The LLM's predicted confidence score (0.00-1.00)
    * `api_response_summary` - The LLM's reasoning and explanation
    * `score` - The relative error percentage for this prediction

Example output structure:
```json
{
  "final_score": 15.67,
  "predictions": [
    {
      "statement_id": 1,
      "statement": "The PS5 pro has...",
      "truth_score": 1.0,
      "confidence_score": 0.95,
      "api_response_summary": "The specifications are mostly accurate...",
      "score": 5.0
    }
  ]
}
```

## Documentation

### Project Structure

```
LLMbenchmark/
├── data/
│   ├── statements.csv      # Input dataset with product specifications
│   └── results.json        # Output results (generated after running)
├── src/
│   ├── __init__.py
│   ├── main.py            # Main orchestration script
│   ├── data_loader.py     # Dataset loading and preprocessing
│   ├── api_integration.py # LLM API communication
│   └── evaluation.py      # Scoring and evaluation logic
└── README.md
```

### Module Documentation

#### `data_loader.py`

Handles loading and preprocessing of the product specification dataset.

**Functions:**

* `load_dataset()`: Loads the dataset from `data/statements.csv`
    * Returns: A pandas DataFrame with `statement` and `truth_score` columns
    * Validates that required columns are present
    * Handles file not found and parsing errors

#### `api_integration.py`

Manages the interaction with the LLM API (Perplexity AI by default).

**Functions:**

* `verify_statement_with_api(statement, apikey)`: Sends a product specification to the LLM for verification
    * Args:
        * `statement`: The product specification text to verify
        * `apikey`: Your LLM API key
    * Returns: The raw API response object as a string
    * Uses a system prompt that instructs the LLM to act as a product finder and rate specifications
    
* `parse_api_response(response_text)`: Parses the raw text response from the API
    * Args:
        * `response_text`: The raw API response
    * Returns: A dictionary containing:
        * `confidence_score`: Extracted confidence score (0.00-1.00)
        * `api_response_summary`: The LLM's reasoning and explanation
    * Uses regex pattern to extract: `Confidence Score: X.XX`

#### `evaluation.py`

Contains the logic for evaluating the LLM's predictions against ground truth.

**Functions:**

* `score_classification(truth_score, confidence_score)`: Calculates the relative error for a single prediction
    * Args:
        * `truth_score`: Ground truth accuracy (0.00-1.00)
        * `confidence_score`: LLM's predicted confidence (0.00-1.00)
    * Returns: Relative error percentage: `((truth_score - confidence_score) / truth_score) * 100`
    * Returns 0.00 if confidence_score is None
    
* `calculate_total_score(results)`: Computes the total error across all predictions
    * Args:
        * `results`: List of prediction result dictionaries
    * Returns: Sum of absolute values of all individual scores
    * Lower total score indicates better performance

#### `main.py`

The main script that orchestrates the entire benchmark process.

**Workflow:**

1. Loads and preprocesses the dataset using `data_loader.py`
2. Iterates through each product specification in the dataset
3. Sends the specification to the LLM API using `api_integration.py`
4. Parses the API response to extract confidence score and reasoning
5. Scores the prediction using `evaluation.py`
6. Accumulates results and calculates the final total score
7. Writes detailed results and final score to `data/results.json`

**Note**: Remember to set your API key in the `api_key` variable before running.

## Scoring System

The benchmark uses a relative error calculation to measure LLM performance:

* **Individual Score**: `((truth_score - confidence_score) / truth_score) * 100`
* **Total Score**: Sum of absolute values of all individual scores
* **Lower scores are better** - indicating smaller discrepancies between predicted and actual accuracy

Example:
- Truth score: 1.00 (completely accurate)
- LLM confidence: 0.95
- Individual score: `((1.00 - 0.95) / 1.00) * 100 = 5.0%` error

## Example Dataset

The included `data/statements.csv` contains product specifications for:
- Gaming consoles (PS5 Pro, Xbox Series X)
- Graphics cards (RTX 2070 Super)
- CPUs (Intel Xeon Platinum 8180, AMD Ryzen 7 4800U)
- Cameras (Nikon Df, Canon PowerShot SX200, Nikon Z6III)

Each statement mixes accurate specifications with intentional inaccuracies to test the LLM's ability to detect false information.

## Requirements

- Python 3.7+
- pandas
- openai (used for API client, compatible with Perplexity AI)

## Contributing

Contributions to this project are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a new branch for your feature or bug fix: `git checkout -b feature/your-feature-name`
3. Make your changes with clear and concise commit messages
4. Test your changes thoroughly
5. Open a pull request describing the changes you've made

### Ideas for Contributions

- Add support for additional LLM providers (OpenAI, Anthropic, etc.)
- Implement different scoring algorithms
- Add more comprehensive test datasets
- Create visualization tools for benchmark results
- Add unit tests and CI/CD integration
- Improve error handling and logging

## License

This project is open source. Please add an appropriate license file for your specific use case.

## Acknowledgments

- Uses the Perplexity AI API for LLM-powered product verification
- Built with Python and pandas for efficient data processing

---

**Note**: Remember to keep your API keys secure and never commit them to version control. Consider using environment variables or a `.env` file for sensitive configuration.
