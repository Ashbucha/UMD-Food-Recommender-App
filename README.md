# UMD Food Recommender App

## Overview
The Food Recommender App is a Python-based project designed to help users explore, rate, and bookmark dining hall food items. The app focuses on community-driven feedback and leaderboard-style rankings to highlight popular dishes and encourage users to try new options.

This project originated as a conceptual design assignment in INST311 and is being implemented as a final project for INST326, with the goal of translating a metadata-driven design into a working Python application.

## Project Status
### Work in Progress
This project is currently unfinished and under active development. The core logic, data structures, and file organization are still evolving as features are implemented and refined.

## Academic Context
Course: INST326 (Python Programming for Information Science)
Purpose: Final course project
Status: Educational / academic use only

Disclaimer:
This project is not affiliated with, endorsed by, or officially connected to the University of Maryland or UMD Dining Services. Any references to dining halls or menu items are for educational and demonstration purposes only.

## Current Functionality
Defines item types such as Food Items, Users, Ratings, Comments, and Bookmarks

Supports basic data modeling for:
- Food recommendations
- Thumbs-up / thumbs-down ratings
- Bookmarking food items
- Uses fabricated sample data to simulate dining hall menus
- dining_hall_menus Folder
- The dining_hall_menus/ directory currently contains nine fabricated Python files that act as placeholders for dining hall menu data.
   - These files do not represent real or complete dining hall menus
   - They are included solely for testing and development purposes
   - In the intended final version of the project, this data would be dynamically generated using a web scraping system (e.g., requests + BeautifulSoup) rather than hardcoded files

## Planned Features
- Replace fabricated menu files with a web scraper that pulls real-time menu data
- Store user interactions and ratings using a database (e.g., SQLite)
- Generate dynamic leaderboards based on ratings and bookmarks
- Improve error handling and input validation
- Add automated testing using Pytest

## Technologies Used
- Python 3
- File handling and data structures
- Object-Oriented Programming
- (Planned) Web scraping with BeautifulSoup
- (Planned) SQLite for persistent storage

## Notes
This repository reflects the development process, not just the final product. Incomplete features, placeholder data, and experimental code are expected as part of the project’s progression.
