The gym goers best friend. Quickly track your workout and progress when you go workout.

get token
=========
curl -L -X POST -d "grant_type=password&client_id=<your_client_id>&username=<username>&password=<password>” http://<url>/o/token/

use token
=========
curl -L -H "Authorization: Bearer <token>“ -X GET http://<url>/<endpoint>/

refresh token
=============
curl -L -X POST -d "grant_type=refresh_token&client_id=<your_client_id>&refresh_token=<your_refresh_token>" http://<url>/o/token/


[![Build Status](https://semaphoreci.com/api/v1/projects/12d10e5f-41fe-4596-aad9-e7934b2612b4/645193/shields_badge.svg)](https://semaphoreci.com/ashtonpaul/gymmate)