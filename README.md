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
  * [Generate flak8 report](#generate-flak8-report)
* [Folder structure](#folder-structure)
  * [Folder controllers](#folder-controllers)
  * [Folder models](#folder-models)
  * [Folder tools](#folder-tools)
  * [Folder views](#folder-views)

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

<!-- FOLDER STRUCTURE -->
## Folder structure

From OC__DA_Python_P9\ChessTournaments folder, you will find the following folders:
* controllers
* models
* tools
* views
* env

<br>

### Folder controllers
In the folder controllers, you retreive all the controllers which aim to manage the application.

<br>

### Folder models
In the folder models, you have the subfolder "database" where the players and tournaments are saved.
There is also all objets link to tournamanent, player and menu which  aloow to manage them.

<br>

### Folder tools
In the folder tools, where is some boilerplate functions for this project.

<br>

### Folder views
In the folder views, you retreive the human machin interface.

<br>

### Folder env
This folder aim to manage the virtual environment where run this application.

<br>
