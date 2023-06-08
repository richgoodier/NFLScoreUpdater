# NFLScoreUpdater

This Python script allows you to track National Football League (NFL) games in real-time. It fetches the live score data from the web, specifically from thescore.com, and then parses and presents this data in a clean and easy-to-understand format in a terminal window. I designed this in order to avoid expensive APIs.

#### Video Demo: <https://youtu.be/y_v8K6ANQqM>

## Features

- Real-time game tracking
- Automatic game updates every 1-2 minutes
- Display of game status (e.g. end of quarter, half-time, end of game)
- Alerts for score changes, with details about how points were likely scored (e.g. touchdown, field goal, etc.)

## Prerequisites

- Python 3.6 or later
- Libraries: BeautifulSoup, requests, re, time, random

## Installation

To install the necessary libraries, you can use pip:
pip install beautifulsoup4 requests

## Usage

To run the script, use the following command:
python nfl_game_tracker.py

## Code Structure

- `main()`: The main function that runs the game tracking loop.
- `get_game_data(url)`: Fetches the raw HTML data from the given URL.
- `clean_data(games_raw)`: Cleans the raw data and returns a list of games with relevant data.
- `compare_games(game, updated_game)`: Compares the previous and updated data for a game, and returns an alert if the score has changed.
- `print_game(game)`: Prints the data for a single game in a clean format.

## Limitations

- This script was built for educational purposes and does not handle all potential edge cases. Use at your own risk.
- This script was built for the NFL season starting in 2022.  It may or may not work for future seasons.
- This script is dependent on http://www.thescore.com/nfl/events and its html structure.  Any changes the site makes may break this script.
