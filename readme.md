The gym goers best friend. Quickly track your workout and progress when you go workout.

Overview
========
This acts as only the backend for the project, the API. Written in [Python](https://www.python.org/) using the [Django Framework](https://www.djangoproject.com/) as a base and extended using the [Django Rest Framework](http://www.django-rest-framework.org/)as the API provider. Users are authorized using OAuth2 tokens (using [Django Oauth Toolkit](https://django-oauth-toolkit.readthedocs.org/en/latest/)).


Setup
=====
There are 4 simple steps into getting you API consumer to access the API.
1) Create a super user in django
2) Setup an API _application_
3) Sign up a _user_
4) Retrieve that _user_'s token

__Create a super user in django__
After migrating the database `python manage.py migrate --settings=gymmate.settings.local`, create a super user using `python manage.py createsuperuser --settings=gymmate.settings.local`. Fill out the necessary information for the user. 

__Setup an API application__
To get access to create an application you need to be logged in as a super user. Go to url `http://<localhost:port>/admin/` to sign in. Once signed in under the Django OAuth Toolkit section go to _Applications_, then hit the _Add Application_ button. __User__ should be the _superuser_ you just created, preferred __Client type__ is _Public_ and __Authorization grant type__ is _Resource owner password-based_. Name can be anything you want it to be and check _Skip authorization_. Take note of the Client ID as you will be needing this to get the user's token. This process only needs to be done once per application e.g 3 times if you have an Angular app, Android app and an iOS app.

__Sign up a user__
Sign up a user using the endpoint `http://<localhost:port>/v1/signup/`. POST form-data or x-www-form-urlencoded 1) email:<email address> 2) password: <password>. If successful your response status code is 201.

__Retrieve that user's token__
Go to `http://<localhost:port>/o/token/` to obtain your authorization token to be able to log into the application.  POST form-data or x-www-form-urlencoded 1) grant_type: password 2) username: <user email address> 3) password: <user password> 4) client_id: <client id of application>. If successful your repsonse status code is 200 and you will get a json response with the token information. 

{
    access_token: is your Bearer token to access the application,
    token_type: Bearer (default Authorization type),
    expires_in: 36000 (default amount of time is 10hrs)
    refresh_token: after token expires use this token to re-authenticate the user
    scope: different scopes you have access to in the application
}

_To refresh an expired token_ go to `http://<localhost:port>/o/token/' and simply POST using the Header information : Authorization: Bearer <refresh token> and you will get a json response with new token information.


Useful CURL command examples
============================
__get token__
curl -L -X POST -d "grant_type=password&client_id=<your_client_id>&username=<username>&password=<password>” http://<url>/o/token/

__use token__
curl -L -H "Authorization: Bearer <token>“ -X GET http://<url>/<endpoint>/

__refresh token__
curl -L -X POST -d "grant_type=refresh_token&client_id=<your_client_id>&refresh_token=<your_refresh_token>" http://<url>/o/token/


[![Build Status](https://semaphoreci.com/api/v1/projects/12d10e5f-41fe-4596-aad9-e7934b2612b4/645193/shields_badge.svg)](https://semaphoreci.com/ashtonpaul/gymmate)