# vilicus

![Dashboard](https://github.com/PatrikFehrenbach/vilicus/assets/9072595/74e8e738-8f9b-40c5-8cf9-641ede1c279f)

Vilicus (from Latin, meaning overseer or supervisor) is a Bug Bounty API Dashboard. This platform is designed to simplify the process of bug bounty hunting by aggregating data from various sources and presenting it in an easy-to-understand dashboard.

## Requirements: 

To get Vilicus up and running, you'll need the following:

- Python3 
- Docker
- Docker-compose

## Installation Steps:

Follow these steps to install and run Vilicus:

1. Clone the Vilicus repository to your local machine.
   
    ```
    git clone https://github.com/PatrikFehrenbach/vilicus.git
    cd vilicus
    ```

2. Start the Docker services.

    ```
    docker-compose up
    ```
    
    Wait for Docker to pull the necessary images and start the services. This may take a while.
    

    This will start the server and the application will be accessible at `localhost:5000` (or whatever port you've configured).

3. Visit the dashboard in your web browser.

### Optional SecurityTrails integration

   The tool has the ability to automatically query the (https://securitytrails.com/) Securitytrails API once a domain has been added. If youwant too enable this feature, you have to rename the `env.example` to `.env` and insert your own API Key. It is also recommended to rebuild the container like so `docker-compose build --no-cache` 

<img width="1012" alt="Screenshot 2023-07-09 at 19 38 06" src="https://github.com/PatrikFehrenbach/vilicus/assets/9072595/9d527caa-5b25-4acb-9e29-1b6f28a94859">


## Contributing:

Contributions are always welcome. If you find a bug or want to add a new feature, feel free to create a new issue or open a pull request.

## License:

This project is open-source and available under the [MIT License](https://github.com/PatrikFehrenbach/vilicus/blob/main/LICENSE).


# Subdomain and Domain API

## Routes

### POST /add_domain

Create a new domain. The request body should contain a JSON object with a "name" field.

Request Body:

```{ "name": "domain name" }```

Responses:
 - 201: 'Domain added successfully!'
 - 400: 'No domain name provided'

---

### POST /update_domain/<string:domain_name>

Update the name of an existing domain. The request body should contain a JSON object with a "name" field.

Request Body:

```{ "name": "new domain name" }```

Responses:
 - 200: 'Domain updated successfully!'
 - 400: 'No new domain name provided'
 - 404: 'Domain not found'

---

### POST /delete_domain/<string:domain_name>

Delete a specific domain by its name.

Responses:
 - 200: 'Domain deleted successfully!'
 - 404: 'Domain not found'

---

### GET /domains/export

Export all domains.

Responses:

 - 200: List of all domains

---

### GET /domains/search?q=test

Search domains by query. The query should be passed as a URL parameter.

Responses:

 - 200: Search results

---

### POST /add_subdomain/<string:main_domain>

Create a new subdomain for a specific domain. The request body should contain a JSON object with a "subdomain_name" field.

Request Body:

```{ "subdomain_name": "subdomain name" }```

Responses:
 - 201: 'Subdomain added successfully!'
 - 400: 'No subdomain name provided'
 - 404: 'Main domain not found'
 - 409: 'Conflict'

---

### POST /update_subdomain/<string:main_domain>/<string:subdomain_name>

Update the name of an existing subdomain for a specific domain. The request body should contain a JSON object with a "name" field.

Request Body:

```{ "name": "new subdomain name" }```

Responses:
 - 200: 'Subdomain updated successfully!'
 - 400: 'No new subdomain name provided'
 - 404: 'Main domain not found'
 - 404: 'Subdomain not found'

---

### POST /delete_subdomain/<string:main_domain>/<string:subdomain_name>

Delete a specific subdomain for a specific domain.

Responses:
 - 200: 'Subdomain deleted successfully!'
 - 404: 'Main domain not found'
 - 404: 'Subdomain not found'

---

### GET /subdomains/export

Export all subdomains.

Responses:

 - 200: List of all subdomains

---

### GET /<string:domain_name>/subdomains/export

Export all subdomains of a specific domain.

Responses:
 - 200: List of all subdomains of the specified domain
 - 404: 'Domain not found'

---

### GET /subdomains/search?q=test

Search subdomains by query. The query should be passed as a URL parameter.

Responses:

 - 200: Search results

---

### GET /lastupdated

Fetch all subdomains added in the last hour.

Responses:

 - 200: List of all subdomains added in the last hour

---

### GET /sort_subdomains

Fetch all domains sorted by the count of their subdomains in descending order.

Responses:

 - 200: List of all domains sorted by subdomains count
