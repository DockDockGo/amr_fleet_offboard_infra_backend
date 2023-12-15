# Setup Instructions for AMR Testbed Offboard Infra backend server

TODO[sid]: Dockerize to make deployment push-button

## Setting up the Development Environment

To run this project, you need to set up a Python virtual environment and install the required dependencies. Follow these steps:

### Prerequisites

- Python 3.x
- pip (Python package installer)
- postgres (See instructions below)

### Installation steps

#### Postgres

To install PostgreSQL on Ubuntu, you can follow these steps:

1. **Update Your System:**
  First, make sure your system's package list is up to date:
  ```
  sudo apt update
  ```
2. **Install PostgreSQL:**
  Install PostgreSQL using the following command:
  ```
  sudo apt install postgresql postgresql-contrib
  ```
3. Verify Installation:
  Once the installation is complete, you can check if PostgreSQL is running with:
  ```
  systemctl status postgresql.service
  ```
4. Configure mfi user
  By default, PostgreSQL creates a user named postgres. To use PostgreSQL, switch to this user:
  ```
  sudo -i -u postgres
  ```
  Then, you can access the PostgreSQL prompt by typing:
  ```
  psql
  ```
  Inside this prompt, Create a New Role and Database:
  ```
  CREATE ROLE mfi WITH LOGIN PASSWORD 'mfi';
  ```
  Now create a database that will be used by the django app:
  ```
  CREATE DATABASE testbed_emulator_2023_12_15;
  ```
  Grant all privileges of this database to the user 'mfi':
  ```
  GRANT ALL PRIVILEGES ON DATABASE testbed_emulator_2023_12_15 TO mfi;
  ```
4. Ensure that this newly created database name, user and password match the project settings in https://github.com/siddhantwadhwa/testbed_emulator_backend/blob/98b826921d837b10147dac8daef453ceac379e48/testbed_emulator_backend/settings.py#L80
  
5. Restart postgres to reflect these changes:
  ```
  sudo systemctl restart postgresql
  ```


#### Project dependencies

1. **Clone the Repository**

   First, clone the repository to your local machine using git:

   ```
   git clone [Your Repository URL]
   cd [Your Repository Name]
   ```

2. **Create a Virtual Environment**

  Create a new virtual environment in the project directory:

  ```
  python -m venv venv
  ```

3. **Activate the Virtual Environment**

  Before installing dependencies, activate the virtual environment:

  ```
  source venv/bin/activate
  ```

4. **Install Dependencies**

  Install all the required dependencies using `pip`:
  ```
  pip install -r requirements.txt
  ```

### Migrate Django models to postgres instance

Run the following command to deploy django model migrations to the newly created postgres db instance:
```
python manage.py migrate
```
**Important**: Ensure that these migrations apply successfully.

## Running the Django server

The installation steps above only need to be executed once. In order to run the django server for the webapp, navigate to the cloned repo directory and execute:
```
source venv/bin/activate;
gunicorn testbed_emulator_backend.wsgi -b <you-ip-address>:8000 --threads 10
```
replacing <your-ip-address> with the appropriate value for the discoverable ip address of your machine on mfi's NETGEAR-5G / NETGEAR network. (starts with 192.*). This will launch the django server on port 8000 of your machine.
