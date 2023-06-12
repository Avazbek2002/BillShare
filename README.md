# BillShare web application

## Login page
<img width="916" alt="image" src="https://github.com/Avazbek2002/BillShare/assets/64166521/d2a6b40c-3a02-4d07-bb15-68489797f959">


## HTML files in _templates_ folder
index.html, badlogin.html, index.html, register.html, welcome.html and wrongemail.html 
files (pages) are only used for loging in to the account.
register.html is for registering.
index.html and register.html have their own corresponding javascript files in **_static folder_**: 
index.js and registration.js.
Both of the javascript files contains code for input validation. 
Particularly for valdidating an email address I used regular expressions function.

In **_static/uploads_** folder I decided to store the image of the bills uploaded by the users.

## **cwk.py** file contains all of the backend code of the website. 
function _topUp()_ is called when the post request is made using ajax from _bills.js_ file to top-up the balance of the user.
function _display()_ is called when the post request is made using ajax from _bills.js_ file to display the uploaded image of
the correspoding bill.
function _remove()_ is called to delete the bill that was paid by the user. **The _bill_ row gets removed from the database when all of the users pay for that particular bill.**

function _paid()_ is called when the post request is made when the user presses the _pay_ button to pay his share of the bill.

