Weather Application
A desktop weather application built with PyQt5 that displays current weather conditions and a 7-day forecast for any city. The app integrates APIs from OpenWeatherMap, Open-Meteo, and OpenCage to provide real-time weather data, with a user-friendly interface featuring temperature unit conversion (°C/°F), city search with autocomplete, and a visually appealing design with icons and shadow effects.
Features

Current Weather (Page 1):

Displays temperature, humidity, pressure, visibility, wind speed, sunrise, and sunset.
Supports temperature conversion between Celsius and Fahrenheit.
Shows weather description and an icon based on conditions.
Includes city name, country, region, and local time with a calendar icon.


7-Day and Hourly Forecast (Page 2):

Provides a 7-day forecast with daily high/low temperatures, humidity, and weather icons.
Shows hourly temperature and weather conditions for the next 20 hours.
Supports temperature unit conversion (°C/°F) for forecasts.


City Search:

Autocomplete search bar to find cities using OpenWeatherMap's geocoding API.
Displays up to 5 matching cities with country names.


UI Design:

Two-page layout with navigation buttons for switching between current weather and forecasts.
Custom widgets with hover effects, shadow effects, and icons for a polished look.
Background image and semi-transparent overlays for improved readability.



Prerequisites

Python 3.7+
PyQt5: For the graphical user interface.
Requests: For making HTTP requests to APIs.
**python-dotenv: For loading environment variables from a .env file.
API Keys:
OpenWeatherMap API key (for current weather and geocoding).
OpenCage API key (for region information).



Installation

Clone the Repository:
git clone <repository-url>
cd weather-app


Install Dependencies:Create a virtual environment (optional but recommended) and install the required packages:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install PyQt5 requests python-dotenv


Set Up Environment Variables:Create a .env file in the project root directory with the following content:
API_KEY=<your-openweathermap-api-key>
OPENCAGE_API_KEY=<your-opencage-api-key>


Sign up at OpenWeatherMap to get an API key.
Sign up at OpenCage to get an API key.


Add Image Assets:Ensure the images/ directory contains the required icon files (e.g., sunny_icon.png, cloudy_icon.png, etc.) as referenced in the get_icone function. The application expects these images to be present.


Usage

Run the Application:
python main.py


Interact with the App:

Page 1 (Current Weather):
Enter a city name in the search bar and press the "Search" button or select a city from the autocomplete list.
View current weather details, including temperature, humidity, and more.
Use the °C/°F dropdown to switch temperature units.
Click the right arrow button to navigate to Page 2.


Page 2 (Forecast):
View the 7-day forecast with daily high/low temperatures and humidity.
Check the hourly forecast for the next 20 hours in the list widget.
Use the °C/°F dropdown to switch temperature units.
Click the left arrow button to return to Page 1.





Project Structure

main.py: The main application script containing the PyQt5 GUI and API integration logic.
images/: Directory for icon files used in the UI (e.g., weather icons, search icon).
.env: File for storing API keys (not included in version control).
README.md: This documentation file.

Dependencies

PyQt5==5.15.10
requests==2.32.3
python-dotenv==1.0.1

Install specific versions using:
pip install -r requirements.txt

Notes

API Rate Limits: Be mindful of the free tier limits for OpenWeatherMap (1,000 calls/day) and OpenCage (2,500 calls/day). Excessive search bar usage may trigger rate limits.
Image Assets: Missing or incorrect image paths will cause the app to fail when loading icons. Ensure all paths in get_icone are correct.
Error Handling: The app displays "Not Found" for invalid cities but may not handle all API errors gracefully. Check the console for debugging information.
Performance: Frequent API calls during city search typing may slow down the app. Consider implementing a debounce mechanism to limit requests.

Future Improvements

Add debounce to the search bar to reduce API calls during typing.
Improve error handling for API failures and display user-friendly messages.
Cache API responses to reduce redundant network requests.
Add support for multiple languages or units (e.g., wind speed in mph).
Enhance accessibility (e.g., keyboard navigation, screen reader support).

License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

OpenWeatherMap for weather and geocoding data.
Open-Meteo for forecast data.
OpenCage for geocoding region information.
PyQt5 for the GUI framework.

