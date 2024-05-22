# web
A retro python web framework that's fun to use! Just download web.py to get started

# Getting Started
Create a folder named cgi-bin next to your index.html file. This is where your python scripts will be stored.

## Api
tag <- using with statements you can easily manage your html tags while printing your web page
form <- similar to tag but for managing forms
input <- a dictonary that allows you to get any form input. 
settings <- allows you to get various enviroment variables
Table <- dict like access to sql database so you can easily store data, also enables storage of lists, tuples, dicts, and sets in the database
start <- a start a web server quickly for debugging and testing your web pages
cookie <- easily create a cookie to temporaily store data

## Deployment
When deploying for production don't use web.start. It uses Python's server library which is not production ready or secure. Use a CGI compabitalbe server such as Apache or lighttpd.

## Why CGI?
Even though it is an old api it's easy and fun to use and most websites don't get enough traffic to start hitting its performance problems and if you do you can use fast-cgi instead.
