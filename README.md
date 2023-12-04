# Library Database Project 📚

Welcome to the Library Database Project! This project is designed to simulate a library's structure and relationships using Django, MySQL, and MongoDB. It offers a hands-on approach to understanding how different database systems can integrate and function in a web application.

## Project Overview

In this project, we model the various entities and relationships found in a library. This includes managing data about books, authors, publishers and more. The project demonstrates the use of both SQL (MySQL) and NoSQL (MongoDB) databases.

## Technologies Used

- **Django**: A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
- **MySQL**: A widely used open-source relational database management system.
- **MongoDB**: A popular document-oriented NoSQL database program.

## Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.8 or later
- pip (Python package manager)
- MySQL Server
- MongoDB Community Server

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/albipuliga/Databases_Library_Project.git
   cd Databases_Library_Project
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Database Configuration

1. **MySQL Database Setup**
   - Start your MySQL server.
   - Create a new MySQL database for the project:
     ```sql
     CREATE DATABASE library_db;
     ```
   - Create a user and grant all privileges to the database:
     ```sql
     CREATE USER 'yourusername'@'localhost' IDENTIFIED BY 'yourpassword';
     GRANT ALL PRIVILEGES ON library_db.* TO 'yourusername'@'localhost';
     FLUSH PRIVILEGES;
     ```
   - Update the `DATABASES` configuration in `settings.py` to reflect your MySQL settings.

2. **MongoDB Setup**
   - Start the MongoDB service.
   - Create a new MongoDB database named `library_db`.
   - Update the MongoDB connection string in `settings.py` to connect to your MongoDB instance.

### Running the Project

1. **Run Migrations:**
   This will create the necessary tables in the MySQL database based on the django models.
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Running the Web Scraping Script:**
   The `webscraping.py` script is used to scrape book data from a specific source, Feel free to stop the running of the program at any point since it will scrape about 30.000 datapoints if ran fully.
   The ISBN codes are taken from `books.csv` file. Then those codes are used to make API calls to the [Open Library API](https://openlibrary.org/developers/api) to get the book data. The data is then stored in the MySQL database.

   ```bash
   python webscraping.py
   ```

4. **Start the streamlit app:**
   Running the following command will start the streamlit app, which can be accessed at `http://localhost:8000/` adn this will allow you to interact with the SQL database.
   ```bash
   streamlit run app.py
   ```

3. **_Optional_ - Start the Django Server:**
   Running the following command will start the Django server, which can be accessed at `http://localhost:8501/`; you can also access the admin panel at `http://localhost:8501/admin/` in which the models can be found.
   ```bash
   python manage.py runserver
   ```


## Contact

For any queries or feedback, feel free to contact [Project Maintainer](mailto:apuliga.ieu2022@student.ie.edu).
