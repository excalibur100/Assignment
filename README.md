# Assignment

# Assignment 1: Rule Engine Implementation
_______________________________________________

## Overview
This project implements a Rule Engine that can fetch, parse, and evaluate business rules stored in a SQL Server database. The engine processes rules to derive logical outcomes based on defined conditions.

## Technologies Used
Python: The main programming language for implementing the rule engine.
Microsoft SQL Server Management Studio: Used to manage the SQL Server database and execute SQL queries.
Libraries:
          pyodbc: For connecting to the SQL Server database.
          re: For regular expressions to parse conditions.
          operator: For operator functions in Python.

## Getting Started

### Prerequisites
- Python 3.x
- SQL Server with a `Rules` table containing `RuleID` and `RuleString`.
- Required Python libraries:
  ```bash
  pip install sqlalchemy pyodbc
Installation
1. Clone the repository:
    git clone [YOUR_GITHUB_REPOSITORY_LINK]
    cd Rule_Engine_Implementation
2. Update the database connection details in the get_connection function:
    conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=YOUR_SERVER_NAME;'
    'DATABASE=YOUR_DATABASE_NAME;'
    'Trusted_Connection=yes;'
)
3. Database Setup
    Use Microsoft SQL Server Management Studio to create a database named Rule_engine.
    Create a table named Rules with the following schema:
        CREATE TABLE Rules (
    RuleID INT PRIMARY KEY IDENTITY(1,1),
    RuleString NVARCHAR(MAX)
);
4. Insert some initial rules into the Rules table.

5. Features
    Fetches rules from the SQL Server database.
    Parses rules into an Abstract Syntax Tree (AST).
    Evaluates rules against provided input data.
6. Testing
   The application has been tested with various input scenarios to ensure the correctness of rule parsing and evaluation.
7. Bonus Points
   The project includes error handling for unknown conditions and operators.
  The code is modular and can be extended easily for additional functionalities.

# Assignment 2: Real-Time Data Processing System for Weather Monitoring
___________________________________________________________________________
## Overview
This project implements a real-time data processing system that continuously retrieves and processes weather data from the OpenWeatherMap API. It provides summarized insights and alerts based on weather conditions.

## Technologies Used
- Python
- SQLAlchemy
- Matplotlib
- OpenWeatherMap API

## Getting Started

### Prerequisites
- Python 3.x
- Required Python libraries:
  ```bash
  pip install sqlalchemy matplotlib requests

1. Setup Instructions
  Clone this repository:

    git clone [YOUR_GITHUB_REPOSITORY_LINK]
    cd Weather_Monitoring_System
  Obtain your OpenWeatherMap API key and replace it in the code:

  API_KEY = '08bb73cf460aa638d38ed76b86dabe33'
2. Run the application:
    
    python Weather_monitor.py

4.Key Features
  Retrieves weather data every 5 minutes for specified cities in India.
  Calculates daily aggregates (average, max, min temperatures, and dominant weather condition).
  Triggers alerts for specific weather conditions.
  Visualizes daily weather trends using Matplotlib.
5. Testing
  The system includes tests for:

    API connectivity and data retrieval.
    Temperature conversion functionality.
    Daily weather summary calculations.
    Alert mechanisms based on user-defined thresholds.
6. Acknowledgements
    OpenWeatherMap API documentation for weather data access.
    Matplotlib documentation for visualization techniques.

  
