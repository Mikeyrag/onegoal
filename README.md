# OneGoal Classroom Progress Dashboard

This dashboard provides an interactive visualization of student progress across various milestones in the OneGoal program.

## Setup Instructions

1. Ensure you have Python 3.7+ installed on your system.

2. Clone or download this repository to your local machine.

3. Open a terminal/command prompt and navigate to the project directory.

4. (Optional but recommended) Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Dashboard

1. In the terminal, ensure you're in the project directory and your virtual environment is activated (if you created one).

2. Run the following command:
   ```
   python dashboard-onegoal.py
   ```

3. Open a web browser and go to http://127.0.0.1:8050/ to view the dashboard.

## Using the Dashboard

- Use the dropdown menu to select a specific teacher and view their class data.
- Click on different points in the graph to see detailed information about student progress.
- Navigate between the Classroom View and Student Table using the sidebar.

## Data Files

Ensure the following CSV files are present in the project directory:
- onegoal_best_fit_list_milestone.csv
- onegoal_champion_milestone.csv
- onegoal_data_dictionary.csv
- onegoal_gpa_goal_milestone.csv
- onegoal_student_information.csv

## Troubleshooting

If you encounter any issues:
1. Ensure all required packages are installed correctly.
2. Check that all CSV files are present in the project directory.
3. Make sure you're using a compatible Python version (3.7+).

For further assistance, please contact [Your Contact Information].