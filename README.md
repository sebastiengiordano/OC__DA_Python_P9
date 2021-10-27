<p align="center">
    <a href="https://user.oc-static.com/upload/2020/09/18/16004297044411_P7.png" class="oc-imageLink oc-imageLink--disabled"><img src="https://user.oc-static.com/upload/2020/09/18/16004297044411_P7.png" alt="Logo"></a>
    <h1 align="center">Book reviews</h1>
    <h2 align="center">(MVP version)</h2>
    </br>
    <p align="left">
        This program is the minimum viable product of a web site used to :
<ul>
<li>Find book reviews or specific article on books</li>
<li>Find interesting book based on reviews of other users</li>
</ul>
    </p>
</p>

<br>
<br>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [How run this program](#how-run-this-program)
  * [Installation](#installation)
  * [Run the program](#run-the-program)
  * [Additional informations](#additional-informations)
  * [Requirements Specification](#requirements-dpecification)
  * [A user could](#a-user-could)
  * [A developer could](#a-developer-could)
  * [The site will need to](#the-site-will-need-to)
  * [The codebase will need to](#the-codebase-will-need-to)

<br>
<br>

<!-- HOW RUN THIS PROGRAM -->
## How run this program

<br>

### Installation

1. Created a folder for this project. Then, open a terminal and go to this folder:
```sh
cd "folder project path"
```
2. Clone the repository:
```sh
git clone https://github.com/sebastiengiordano/OC__DA_Python_P9
```
3. Go to folder OC__DA_Python_P9:
```sh
cd OC__DA_Python_P9
```
4. Create a virtual environment:
```sh
virtualenv env -p python3
```
5. Activate the virtual environment :
```sh
.\env\Scripts\activate
```
6. From the "requirements.txt" file, install needed packets:
```sh
python -m pip install -r requirements.txt
```

<br>
<br>

### Run the program
1. Open a terminal and go to the folder OC__DA_Python_P9 (if its not already the case):
```sh
cd "folder project path" & cd OC__DA_Python_P9
```
2. Activate the virtual environment (if its not already the case):
```sh
.\env\Scripts\activate
```
3. Run the server
```sh
cd "LITReview"
python manage.py runserver
```
4. Use the following url
```sh
http://127.0.0.1:8000/reviews/
```

<br>
<br>

### Additional informations
Here after, some account in order to use this MVP version:
* Name                  Password
* Freddie Mercury       kXkk6jgkiiZELz
* Guido van Rossum      sC8KYyZzPq89Ji
* Mattéo                8frxJVB5NmfVhN
* Yann18                P6Pkrh6Bw4d2bM
* Lolo                  hYzB9i5EEGeBGy

<br>

For admin permission, in order to display information from the database, which could be dynamically update.
1. Use the followinf link:
```sh
http://127.0.0.1:8000/admin/
```
2. And this account:
* Admin                 6SKBtB*jFLwvpTW

<br>
<br>

<!-- Requirements Specification -->
## A user could:
*	Log in and sign up - the site should not be accessible to a non-logged-in user.
*	View a feed containing the latest tickets and reviews from users that they follow ordered by time with the latest first.
*	Create new tickets requesting a review on a book/article.
*	Create reviews as a response to tickets.
*	Create reviews not in response to a ticket.  As part of a one-step process, the user could create a ticket and then a review responding to their own ticket.
*	View, edit, and delete their own tickets and reviews,
*	Follow other users by entering their username,
*	View who they follow and unfollow whoever they want. 

<br>

### A developer could:
*	Create a local environment using venv and run the site based on this detailed documentation.

<br>

### The site will need to:
*	Have a UI matching those of the wireframes.
*	Have a clean and minimal UI.
*	Use server-side rendering to display information from the database on the page dynamically. 

<br>

### The codebase will need to:
*	Use the Django framework.
*	Use the Django template language for server-side rendering.
*	Use SQLite as a local development DB (your db.sqlite3 file should be included in the repository).
*	Have a database design that matches the database schema.  Have syntax that meets PEP8 guidelines. 
A user could:
*	Log in and sign up - the site should not be accessible to a non-logged-in user.
*	View a feed containing the latest tickets and reviews from users that they follow ordered by time with the latest first.
*	Create new tickets requesting a review on a book/article.
*	Create reviews as a response to tickets.
*	Create reviews not in response to a ticket.  As part of a one-step process, the user could create a ticket and then a review responding to their own ticket.
*	View, edit, and delete their own tickets and reviews,
*	Follow other users by entering their username,
*	View who they follow and unfollow whoever they want. 

<br>
