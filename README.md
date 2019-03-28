# Plant Disease Detection and Diagnosis using Deep Learning

**It's a B.Tech Final Year - 2019 Project**

## Installation

1. Install [postgres](https://www.postgresql.org/download/) and complete it's configuration

2. Use the package manager [pip](https://pip.pypa.io/en/stable/installing/) for installation and [python3.6 or above](https://www.python.org/downloads/)

3. Create a virtual environment (using virtualenv etc.)
```python
    pip install virtualenv

# We use virtualenvwrapper for easy management of envs
    pip install virtualenvwrapper # for linux
    pip install virtualenvwrapper-win # for windows

# Create virtual environment
    mkvirtualenv env_name
    setprojectdir .     # assuming you are in git-directory
```
4. Install the requirements
```python
    pip install -r requirements.txt
```
5. To deactivate the env simply quit the terminal or enter
```python
    deactivate
```

## Usage
1. Copy "trained_model" folders to the path "/app/tf_disease_classifier/"
2. Change the configuration in [run.py](/run.py#L10) according to class from [config.py](/app/config.py)
3. Set your environment variables
    * use *Config* class to use sqlite
    * to use *DevelopmentConfig*, rename .env.example to .env and set the values as directed in the file
4. Run the following commands to set migrations:
```python
    python manage.py db init
    python manage.py db migrate -m "Inital commit"
    python manage.py db upgrade
```
4. Finally run the flask app
```python
    python run.py
```

## Postman environment setup
1. Load '*btp-2019.postman_collection.json*' into **Postman**
2. Create an enviroment and set {key:value} as:
    - key = url
    - value = http://localhost:5000/api
3. Now test the different apis:
    - first register admin and user
    - user admin to register plants and diseases