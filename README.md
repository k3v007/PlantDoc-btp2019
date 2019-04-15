# Plant Disease Detection and Diagnosis using Deep Learning

**It's a B.Tech Final Year - 2019 Project** -- [*PlantDoc*](https://plant-doc-btp2019.herokuapp.com//login/google/authorized)

## Installation

1. Use the package manager [pip](https://pip.pypa.io/en/stable/installing/) for installation and [python3.6 or above](https://www.python.org/downloads/)

2. Create a virtual environment (using virtualenv etc.)
```python
    # For Windows 10
    pip install virtualenv
    pip install virtualenvwrapper-win
    mkvirtualenv env_name   # Create virtual environment
    setprojectdir .         # assuming git-directory

    # For linux System - using conda
    conda create -n env_name python=3.7.2
    conda activate env_name
```
4. Install the requirements
```python
    pip install -r requirements.txt
```
5. To deactivate the env simply quit the terminal or enter
```python
    deactivate
    
    # or
    conda deactivate    # for linux
```

## Usage

1. Set your database on heroku, aws or any other platform
2. Run the following commands to set migrations (already connected to above DB):
```python
    python manage.py db init
    python manage.py db migrate -m "Inital commit"
    python manage.py db upgrade
```
3. Host the app on Heroku or AWS

