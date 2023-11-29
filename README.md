# DeepWeb Scanning and Monitoring Solution #INPROGRESS

This is a basic framework to set up a deep web scanning and monitoring solution. The application's entry point is the `app.py` file, which can be executed using the command `python app.py`. Please ensure that you have PostgreSQL installed as the application requires it to run. The username and password for the PostgreSQL database should be passed to the `app.py` file as arguments or set as environment variables.

### Usage

1. Run the application by executing `app.py` using the command:
    
    ```
    python app.py
    
    ```
    
    Note: Make sure to have PostgreSQL installed and the database credentials set correctly.
    
2. Access the API locally using either the CLI or a web browser. When running locally, the API can be accessed at `http://localhost:5000`.
    
    The API has the following endpoints:
    
    - `/search`: Use this endpoint to search for keywords.
    - `/irc/run`: This endpoint is a work in progress and will be used to start an IRC scanner. #INPROGRESS
    - `/site/list`: Lists all the registered sites.
    - `/site/register`: A POST method endpoint to register a site. Use the following `curl` command to register a site:
        
        ```
        curl.exe -X POST -d 'url=<https://test.com>' http://127.0.0.1:5000/site/register
        
        ```
        
    - To perform a search, use the following `curl` command:
        
        ```
        curl.exe <http://127.0.0.1:5000/search?q=test+1>
        
        ```
        

### Installation

1. Install all Python dependencies by running the following command:
    
    ```
    pip install -r requirements.txt
    
    ```
    
2. Install Tor based on your operating system. For Debian-based systems, use the following command:
    
    ```
    apt update && apt install tor -y
    
    ```
    
3. Set up PostgreSQL by following the manual instructions for PostgreSQL installation, or alternatively, you can create a PostgreSQL Docker container using the following command:
    
    ```
    docker run -d --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -e PGDATA=/var/lib/postgresql/data/pgdata -v /custom/mount:/var/lib/postgresql/data -p 5432:5432 postgres
    
    ```
    
    Note: This is just a sample script and is not ready for production use yet.
    

**Note:** This is a basic framework, and further customization and hardening are necessary before deploying it in a production environment.


https://github.com/cabbagec2hlbGwK/IOC_Scan/assets/83215604/58213f70-c68e-44ce-9e8e-0857df6d42af


