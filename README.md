# Pytagora

![Mockup Pytagora different screen sizes](readme/pyt_overview.png)


Pytagora is a software service that can help jobseekers get the a reference from their
previous employers and let them save references to be used in multiple future job interviews.


| Problem | Solution |
|---------|----------|
| Multiple recruiters contacting the same reference for a reference check | Pytagora allows the candidate to initiate the reference check and send the request to the reference |
| No way for the candidate to save the answers from a reference for future recruitment processes | Pytagora allows the candidate to store completed reference checks for future use |
| Recruiter and reference may not have time to talk at the same time, leading to rescheduling and lost productivity for the recruiter | Pytagora allows the reference to answer the questions on their own time, avoiding the need for scheduling |
| Candidate is not the owner of their own reference information | Pytagora allows the candidate to be the owner of their own reference information, stored digitally |
| Reference checks can be time-consuming for recruiters | Pytagora streamlines the reference check process, allowing recruiters to spend more time on other tasks |
| Recruiters may not have access to all relevant reference information | Pytagora allows the candidate to provide access to multiple references, ensuring that all relevant information is available |
| Candidates may not have access to past colleagues or managers to use as references | Pytagora allows the candidate to use any professional contact as a reference, regardless of their current employment status |


### Prerequisites


Before running this project, make sure you you have an environment with python3.10.6 or later installed. 

there are also a few neccesary environment variables to include before running the project. On step 3 in "getting started" copy the following code into your **_env.py_** file and change the placeholder text to your personal information. 

``` python
# copy this entire block of code
# into a file named env.py
import os

# change this to YOUR secret key 
# new key can be generated here: https://djecrety.ir/
os.environ["SECRET_KEY"] = "<your secret key>"

#can be set to "None" if DEBUG and TEST_SERVER is set to true
os.environ["DATABASE_URL"] = "None"

# By having both these variables set to true
# django's SQL lite will be running as application server, 
# and emails will be logged in the console.
os.environ["DEBUG"] = "True"
os.environ["TEST_SERVER"] = "True"


#in development emails will be logged in the console. 
# so these can be set to "None" like this.
# if debug and testServer is NOT "True", 
# this must details for a real gmail account.
os.environ["EMAIL_HOST_USER"] = "None"
os.environ["EMAIL_HOST_PASSWORD"] = "None"

```


## Getting Started in 5 steps

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

> **1. clone repository and cd**
> - open  terminal
> - change current work-directory to where you want the cloned directory
> - type git clone then the url to this project
> > $ ``` git clone https://github.com/4ntm4n/ms-four```
> - then change directory into the project folder:
> > $ ```cd ms-four```

> **2. Start environment and install dependencies**
> - Create a development environment with python 3.10.6. example with virtualenv and python 3.10.6 as default:
> > $ ```virtualenv pytagora_env```
> 
> > $ ```source pytagora_env/bin/activate```
>  - then, in your development environment run:
> >$ ``` pip install -r requirements.txt```

> **3.  set up environment variables**
> - create env.py file and set up mandetory environent variables shown below
> > $```nano env.py``` 
> - then paste in the code from **_Prerequisites_** above.
> - exit by pressing **'ctrl** + **x'** and **'y'** to save **_env.py_** and hit **enter** to exit nano.

> **4. Make Migrations and Migrate**
>  - run the following code to make migrations (should not be needed, but good practice before migration):
> > $ ```python3 manage.py makemigrations```
> - then migrate. 
> > $ ```python3 manage.py migrate```

> **5. run the dev server and you are done!**
> - in the terminal, type:
> > $ ```python3 manage.py runserver```
> -  go to **_http://localhost:8000/_** to run the project locally.
> > Note that the server will be hosted on **_localhost_**  and that the specific adress: **_127.0.0.1_** is not an allowed host by default in this project. 
> >
> >It can, however, be added to the **ALLOWED_HOSTS** list in **settings.py** if you want to.