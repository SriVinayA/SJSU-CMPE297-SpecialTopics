# API Integration with Claude Dev Extension

This directory demonstrates how the Claude Dev Extension can assist with integrating external APIs into a Python application.

## Use Case

Integrating the OpenWeatherMap API to create a weather information retrieval system.

## Example

Let's create a Python script that retrieves current weather information for a given city using the OpenWeatherMap API.

## How Claude Dev Extension Helps

1. Analyze the requirements for API integration.
2. Provide the necessary code structure for making API requests.
3. Handle API authentication and parameter formatting.
4. Process and present the API response data.
5. Implement error handling and provide usage examples.

Here's how the Claude Dev Extension might assist in creating this API integration:

```python
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherAPI:
    """
    A class to interact with the OpenWeatherMap API for retrieving weather information.
    """

    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        """
        Initialize the WeatherAPI class.
        
        Raises:
            ValueError: If the API key is not found in environment variables.
        """
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key not found. Please set the OPENWEATHERMAP_API_KEY environment variable.")

    def get_weather(self, city, country_code):
        """
        Retrieve current weather information for a given city.

        Args:
            city (str): The name of the city.
            country_code (str): The two-letter country code.

        Returns:
            dict: A dictionary containing weather information.

        Raises:
            requests.RequestException: If there's an error with the API request.
            ValueError: If the API response is invalid or contains an error message.
        """
        params = {
            "q": f"{city},{country_code}",
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if "main" not in data or "weather" not in data:
                raise ValueError("Invalid API response format")

            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }

        except requests.RequestException as e:
            raise requests.RequestException(f"Error fetching weather data: {str(e)}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"Error processing weather data: {str(e)}")

def main():
    weather_api = WeatherAPI()
    
    try:
        city = input("Enter city name: ")
        country_code = input("Enter country code (e.g., US, GB, JP): ")
        
        weather_info = weather_api.get_weather(city, country_code)
        
        print(f"\nWeather in {weather_info['city']}, {weather_info['country']}:")
        print(f"Temperature: {weather_info['temperature']}°C")
        print(f"Feels like: {weather_info['feels_like']}°C")
        print(f"Description: {weather_info['description']}")
        print(f"Humidity: {weather_info['humidity']}%")
        print(f"Wind speed: {weather_info['wind_speed']} m/s")
    
    except (ValueError, requests.RequestException) as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
```

To use this script:

1. Install required packages: `pip install requests python-dotenv`
2. Create a `.env` file in the same directory as the script with your OpenWeatherMap API key:
   ```
   OPENWEATHERMAP_API_KEY=your_api_key_here
   ```
3. Run the script and enter a city name and country code when prompted.

## Benefits

- Structured API integration: The extension provides a well-organized class for API interactions.
- Error handling: Robust error handling is implemented to deal with various potential issues.
- Security: API key is securely stored in environment variables.
- User-friendly interface: The script provides a simple command-line interface for user interaction.
- Reusability: The `WeatherAPI` class can be easily imported and used in other projects.
- Clear documentation: Docstrings and comments explain the purpose and usage of each component.
- Data processing: The API response is processed into a more usable format.
- Customization: The script can be easily modified to include additional weather data or features.

By using the Claude Dev Extension for API integration, developers can quickly create robust and well-structured code for interacting with external APIs. This approach ensures that API integrations are secure, error-resistant, and easily maintainable. The extension's ability to provide a complete solution, including error handling and user interaction, saves development time and promotes best practices in API integration.