
Welcome to Spotifest!
Spotifest is an innovative web application that integrates with Spotify to create festival-specific playlists. Leveraging the power of Python, Flask, and Spotify's API, Spotifest offers a unique experience for festival-goers and music enthusiasts.

Features
Festival Database: Utilize our comprehensive database to explore various festivals and their details.
Dynamic Playlist Creation: Automatically generate Spotify playlists featuring top songs from bands playing at selected festivals.
API Integration: Seamlessly integrates with Spotify to enhance your music experience.
User-Friendly Interface: Easy-to-navigate web interface with clear instructions and documentation.
Getting Started
Install Dependencies: Run pip install -r requirements.txt to install the necessary Python packages.
Database Setup: Initialize and migrate your database using Flask-Migrate commands:
csharp
Copy code
flask db init
flask db migrate
flask db upgrade
Run the Server: Start the Flask server with flask run.
Populate Database: Add festivals to the database by accessing the endpoint /database/<country_code>.
Explore API: Check out our Swagger documentation at /swagger for detailed API usage.
Technology Stack
Flask: A lightweight WSGI web application framework.
SQLAlchemy: SQL toolkit and ORM for database interactions.
Spotipy: A lightweight Python library for the Spotify Web API.
Beautiful Soup: Library for web scraping purposes.
Contributing
We welcome contributions! If you have suggestions or want to improve Spotifest, feel free to fork the repository and submit a pull request.

License
Spotifest is open-sourced under the MIT License.

Acknowledgements
Special thanks to everyone who contributed to the development of Spotifest, making it a valuable tool for music lovers everywhere.
