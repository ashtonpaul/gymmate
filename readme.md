The gym goers best friend. Quickly track your workout and progress when you go workout.

get token
=========
curl -L -X POST http://<url>/api-token-auth/ --data "username=<username>&password=<password>”

use token
=========
curl -L -H "Authorization: Token <token>“ -X GET http://<url>/progress


[![Build Status](https://semaphoreci.com/api/v1/projects/12d10e5f-41fe-4596-aad9-e7934b2612b4/645193/shields_badge.svg)](https://semaphoreci.com/ashtonpaul/gymmate)