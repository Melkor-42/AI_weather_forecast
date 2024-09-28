
# Weather Forecast Generator Application

## Overview
This application generates weather forecast articles using two models: 
- A **local model** for generating concise and factual articles.
- A **large language model (LLM)** for more diverse article generation (factual, concise, or tabloid style).

The user provides a city, language, and style, and the application uses weather data from OpenWeatherMap to generate weather reports for either current weather or forecast. 

The application supports two main article types:
1. **Current Weather**: Generates an article based on current weather conditions.
2. **Weather Forecast**: Generates a forecast article for upcoming days.

The generated article includes:
- A **headline** summarizing the weather.
- A **lead** introducing the key information.
- A **body** providing detailed weather news.

## Requirements
To run this application locally, you will need:
- Python 3.8+
- FastAPI
- Uvicorn
- Jinja2
- OpenWeatherMap API credentials

## Installation
1. Clone this repository to your local machine.
   ```
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required Python packages.
   ```
   pip install -r requirements.txt
   ```

## Endpoints
The application provides several API endpoints:

### 1. Get City Suggestions
   - **URL**: `/location/cities`
   - **Method**: `GET`
   - **Query Parameters**:
     - `query`: Partial city name (for autocomplete)
   - **Response**: List of suggested cities with their country names.

### 2. Get City Coordinates
   - **URL**: `/location/coordinates`
   - **Method**: `GET`
   - **Query Parameters**:
     - `city`: City name
     - `country`: Country name
   - **Response**: Latitude and longitude of the city.

### 3. Generate Current Weather Article (Replicate LLM)
   - **URL**: `/articles/current/replicate`
   - **Method**: `POST`
   - **Request Body**:
     - `lat`: Latitude of the city
     - `lon`: Longitude of the city
     - `style`: Article style (`factual`, `concise`, `tabloid`)
     - `language`: Article language (`EN`, `SK`)
   - **Response**: Generated article (headline, lead, body).

### 4. Generate Current Weather Article (Local Model)
   - **URL**: `/articles/current/local`
   - **Method**: `POST`
   - **Request Body**:
     - `lat`: Latitude of the city
     - `lon`: Longitude of the city
     - `style`: Article style (`factual`, `concise`)
     - `language`: Article language (`EN`)
   - **Response**: Generated article (headline, lead, body).

### 5. Generate Forecast Weather Article
   - **URL**: `/articles/forecast`
   - **Method**: `POST`
   - **Request Body**:
     - `lat`: Latitude of the city
     - `lon`: Longitude of the city
     - `style`: Article style (`factual`, `concise`, `tabloid`)
     - `language`: Article language (`EN`, `SK`)
   - **Response**: Generated article (headline, lead, body).

## Running the Application Locally
To run the application locally:

1. Start the FastAPI server:
   ```
   uvicorn app:app --reload
   ```

2. The application will be available at:
   ```
   http://127.0.0.1:8000/
   ```

3. Documentation is available at:
   ```
   http://127.0.0.1:8000/docs
   ```

You can test the API through the FastAPI's interactive documentation or by sending HTTP requests to the listed endpoints.

## License
This project is licensed under the MIT License.
