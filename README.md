# Django Project Documentation: Backend for The MobieDB Data Management and Cinema Scraping

This documentation provides an overview and usage guide for the Django project that serves as the backend for managing data from The MobieDB and performs scraping to obtain cinema data. The project allows access to and manipulation of information related to movies and cinemas.

## Requirements

- Python 3.x
- Django 3.x
- BeautifulSoup (for web scraping)
- Requests (for making HTTP requests)

## Installation

1. Clone the repository:

```
git clone <repository_url>
```

2. Navigate to the project directory:

```
cd django-backend-project
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

4. Set up the database:

```
python manage.py migrate
```

## Configuration

1. Open the `settings.py` file located in the project's main directory.

2. Configure the database settings according to your requirements. Update the `DATABASES` section with the appropriate credentials.

3. Obtain an API key from The MobieDB (https://www.themoviedb.org/) and update the `TMDB_API_KEY` variable in `settings.py` with your API key.

## Usage

### Running the Development Server

To start the Django development server, execute the following command:

```
python manage.py runserver
```

The server will start running at `http://localhost:8000/`.


## Conclusion

This documentation provides an overview and instructions for using the Django backend project for managing data from The MobieDB and performing cinema data scraping. Use the provided API endpoints to interact with movie and cinema data, and utilize the data scraping command to retrieve cinema information. For further assistance or issues, refer to the project's documentation or contact the project maintainers.
