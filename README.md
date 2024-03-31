
# Rick and Morty API Documentation

## Introduction
This documentation provides detailed information about the Rick and Morty API, which is designed to access information about characters, episodes, and locations from the Rick and Morty universe. It includes information on installation, running the API, available endpoints, and their usage.

## Installation
To install and run the Rick and Morty API, follow these steps:

Clone the repository:
```bash
git clone https://github.com/Tomer-Lavan/rick-and-morty-api.git
```

Navigate to the project directory:
```bash
cd rick-and-morty-api
```
Install the required dependencies:
```bash
pip install -r requirements.txt
```

Run the API server:
```bash
uvicorn app.main:app --reload
```

The API server will start running on http://localhost:8000.

## Endpoints

Get the endponits list by reaching the Swagger docs at the adress:
http://localhost:8000/docs

## Structure Explanation
The API is structured using the FastAPI framework. It consists of several components:

- Models: Defined using Pydantic, models represent the structure of data objects such as characters, episodes, and locations.

- Endpoints: Located in the app/api/endpoints directory, endpoints define the API routes and their logic.

- Services: Located in the app/services directory, services contain business logic and data manipulation.

- Dependencies: Defined in the app/dependencies.py file, dependencies are used for authentication and in the future other common functionality.

- Main: The main.py file is the entry point of the application. It sets up the FastAPI app and includes the routers for the endpoints.

- Cache: A simple caching mechanism is implemented in the app/services/cache.py file to improve the performance of data fetching and there is a decorator implementation to reduce code boilerplate.

- Tests: The folder tests contain all endpoints testing using pytest.

## Usage Explanation
The project is attached with a postman collection that can be downloaded from the postman folder. To use the API, you need to follow these steps:

- Authentication: Obtain an access token by sending a POST request to the /auth/login endpoint with your username and password. Use this token in the Authorization header for subsequent requests.

- Fetching Data: Access the desired endpoint by sending a GET request with any required query parameters. Add the token Authorization header Bearer token. For example, to fetch characters with the status "Alive", you would send a GET request to /characters?status=Alive.

- Filtering and Pagination: Use query parameters to filter results and paginate through them. For example, to get the second page of episodes, you would send a GET request to /characters?page=2.

- Analyzing Data: Access the insights endpoints to get analysis on the data, such as the most common species or survival rates based on location.

## Testing Explanation
Navigate to the project directory:
```bash
cd rick-and-morty-api
```

Run the testing command:
```bash
pytest tests/
```

## Future Improvments
- Improve Caching: Use a cache system like redis and add other services to the cache.
- Add Other Sources: Use api's such IMDB and Rottem Tomatos to get more data such episodes raitings to robust insghts endpoints.
- Improve Sutrvival Prediction: Use machine learning/satistical models to get more accurate weights to location, gender and species.
- Optimise Performence: In some endpoints that are getting top k of a metric we can use a heap to make the function more efficient.
                        Due to the nature of the api data is limited I decided that currently it is unnecessary.
- Improve Testing: Currently most of the testing are straight forward and do not cover all cases.
- Improve Auth: Change auth to be cookie based and improve to be by a real DB.