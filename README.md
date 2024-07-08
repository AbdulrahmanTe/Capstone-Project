# Capstone Project - Steam Profile Tracker

## Overview

The Steam Profile Tracker is a web application built with Streamlit that allows users to search for Steam profiles and view their top games. The application fetches user data using the Steam Web API and displays it in a user-friendly interface. If a user is not already in the database, the application retrieves their details from the Steam API and stores them for future queries.

## Features

- **Search for Steam Users:** Enter a Steam username to search for their profile.
- **View Recently Viewed Users:** A sidebar displays a list of recently viewed users for quick access.
- **Display User Information:** Shows the user's name, avatar, and top 3 games with playtime.
- **Automatic Data Insertion:** If a searched user is not found in the database, their details are fetched from the Steam API and inserted into the database.

## Prerequisites

- Python 3.x
- Streamlit
- psycopg2
- steam-web-api (or any library for accessing Steam API)
- PostgreSQL database

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/steam-profile-tracker.git
   cd steam-profile-tracker

2. Install the required packages:
   ```bash
   pip install -r requirements.txt

3. Set up environment variables:
Create a .env file in the project root and add your Steam API key and database credentials:
    ```bash
    STEAM_API_KEY=your_steam_api_key
    User=your_db_user
    Password=your_db_password
    Host=your_db_host
    Database=your_db_name
    Port=your_db_port

## Usage

1. Run the Streamlit application:

    ```bash
    streamlit run app.py
2. Open your web browser and go to the provided URL (typically http://localhost:8501).

3. Use the sidebar to search for a Steam user by their username or select from recently viewed users.

4. View the user's profile and top 3 games.

## Database Schema

The application uses a PostgreSQL database with the following schema for storing user information:

    
    CREATE TABLE student.de10ATCapstoneProject (
    user_name VARCHAR(255) PRIMARY KEY,
    steam_id VARCHAR(255),
    avatar_url TEXT,
    game_name1 VARCHAR(255),
    game_img1 TEXT,
    game_url1 TEXT,
    playtime1 INTEGER,
    game_name2 VARCHAR(255),
    game_img2 TEXT,
    game_url2 TEXT,
    playtime2 INTEGER,
    game_name3 VARCHAR(255),
    game_img3 TEXT,
    game_url3 TEXT,
    playtime3 INTEGER
    );
