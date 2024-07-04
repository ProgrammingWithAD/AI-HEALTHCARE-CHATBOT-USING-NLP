# AI-HEALTHCARE-CHATBOT-USING-NLP


## Overview

This project implements an AI-powered Healthcare Chatbot using Natural Language Processing (NLP) techniques. The chatbot is designed to simulate a general physician's diagnosis process by asking users a series of questions about their symptoms and providing a potential diagnosis along with recommended next steps.

## Features

- User-friendly graphical interface
- Symptom-based disease prediction
- Confidence level calculation for diagnoses
- Doctor recommendations based on predicted conditions
- Links to further medical resources

## Technologies Used

- Python 3.x
- Tkinter for GUI
- Pandas for data manipulation
- Scikit-learn for machine learning models
- Natural Language Processing techniques

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/AI-HEALTHCARE-CHATBOT-USING-NLP.git
   ```

2. Navigate to the project directory:
   ```
   cd AI-HEALTHCARE-CHATBOT-USING-NLP
   ```

3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the main application:
   ```
   python QuestionDiagonosisTkinter.py
   ```

2. Use the GUI to interact with the chatbot:
   - Click "Start" to begin the diagnosis process
   - Answer "Yes" or "No" to the prompted symptoms
   - Review the diagnosis and recommendations provided

## Data Sources

- `Training.csv`: Contains the training data for symptom-disease relationships
- `Testing.csv`: Contains test data for model validation
- `doctors_dataset.csv`: Contains information about doctors and their specialties

## Project Structure

- `QuestionDiagonosisTkinter.py`: Main application file with GUI implementation
- `healthcare_chatbotConsole.py`: Console version of the chatbot (for testing purposes)
- `newlogin.py`: User authentication module

## Future Improvements

- Implement more advanced NLP techniques for better understanding of user inputs
- Expand the symptom and disease database
- Integrate with external medical APIs for more comprehensive information
- Add multi-language support

## Contributors

- Akash Deep Sarkar

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Thanks to [mention any datasets, libraries, or resources you've used]
- Inspired by [mention any inspirations or similar projects]

## Disclaimer

This chatbot is for educational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.