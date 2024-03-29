# News-Nexus

News Nexus is a sophisticated web platform designed to streamline the management of newspaper editors and their articles. Editors can effortlessly publish, browse, and add their names to articles they have edited, enhancing transparency and collaboration within the editorial process. Additionally, editors have the flexibility to remove their names from articles as needed. Only authenticated users can leave comments on articles, ensuring a quality discourse environment. Administrative privileges empower administrators to delete or modify articles as necessary, maintaining the integrity of the platform.

## Check it out!
https://news-nexus.onrender.com/

## Quick Start:

Python3 must be already installed


For macOS:
```shell
git clone https://github.com:Anna728560/News-Nexus.git
cd news_nexus
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```
For Windows:
```shell
git clone https://github.com:Anna728560/News-Nexus.git
cd news_nexus
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```
For Linux:
```shell
git clone https://github.com:Anna728560/News-Nexus.git
cd news_nexus
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```

## Running the tests:
```shell
python manage.py test
```


## Features:
* Secure authentication functionality for Redactor/User
* Intuitive interface for managing newspaper redactors and topics.
* Robust admin panel for advanced management capabilities.

## Built With:
* Django - The web framework used
* HTML/CSS - Frontend design
* Python - Backend programming language

## DataBase Structure:
![img_3.png](img_3.png)


## Demo:
Explore the sleek interface of News Nexus in the demo image provided:
![img_1.png](img_1.png)
![img_2.png](img_2.png)
