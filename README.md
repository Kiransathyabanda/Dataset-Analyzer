# Dataset Visualization App

This is a Streamlit web application that allows users to upload datasets, preprocess them, and visualize the data using various types of charts. The app supports `.csv` and `.xlsx` file formats.

## Features

- **Upload Multiple Datasets**: Users can upload multiple CSV or Excel files which will be combined into a single dataset.
- **Preprocess Data**: Convert categorical columns to numerical codes.
- **Visualize Data**: Generate various types of charts including line charts, area charts, bar charts, scatter plots, histograms, box plots, and violin plots.
- **Summary Statistics**: Display summary statistics and visualizations (histograms and box plots) for selected columns.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/dataset-visualization-app.git
    cd dataset-visualization-app
    ```

2. **Create and activate a virtual environment** (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Streamlit app**:
    ```sh
    streamlit run main.py
    ```

2. **Navigate to the app in your browser**:
    - The app will typically be running at `http://localhost:8501`.

3. **Interact with the app**:
    - Use the file uploader to upload your datasets.
    - Select columns and chart types for visualization.
    - Preprocess data if necessary.
    - View summary statistics and visualizations for selected columns.

## Files

- `main.py`: Main Streamlit application file.
- `requirements.txt`: List of Python dependencies.

## Dependencies

- streamlit
- pandas
- plotly

## Credits

- Developed by [kiransathyabanda].

## License

This project is licensed under the [MIT License](LICENSE).
