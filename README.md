# My Language Trainer

## About This Project
This is a python flask application which was made to help people to learn and practice vocabulary based on what the user came across in daily life.

## APIs
1. Google Cloud Text To Speech
2. Twillio SMS API

## Built With
- ![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
- ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
- ![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black)
- ![HTML](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
- ![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
- ![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
- ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) / SQLAlchemy

## Getting Started
1. Fork and clone my code into your coding environment such as PyCharm, Atom and etc.
Here's the document of the instruction of forking and cloning.
[GitHub Pages](https://docs.github.com/en/get-started/quickstart/fork-a-repo)

2. Put your own flask app key and database url in the main.py file.
``` 
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
```

3. Put your own credentials for the Text To Speech API.
```
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'YOUR_CREDENTIALS'
```

4. Put your own authentication info for the Twillio SMS API
```
account_sid = "YOUR_SID"
auth_token = "YOUR_TOKEN"
client = Client(account_sid, auth_token)
tw_phone = "YOUR_TWILLIO_PHONE_NUMBER"
your_phone = "YOUR_DAILY_PHONE_NUMBER"
```

## Contact
![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white) 
Username: bochan#0244

Let me know how it works for you and what you think I should improve about this application.
