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

3. In a new terminal window, install the required Python packages.

    ```
    python3 -m pip install -r requirements.txt
    ```

4. Start the Vilicus server.

    ```
    python3 run.py
    ```

    This will start the server and the application will be accessible at `localhost:5000` (or whatever port you've configured).

5. Visit the dashboard in your web browser.

## Contributing:

Contributions are always welcome. If you find a bug or want to add a new feature, feel free to create a new issue or open a pull request.

## License:

This project is open-source and available under the [MIT License](https://github.com/PatrikFehrenbach/vilicus/blob/main/LICENSE).