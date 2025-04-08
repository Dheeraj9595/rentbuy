#How to get coverage report
-
- coverage report -m

#How to get coverage pytest run
-
- coverage run -m pytest

#How to run pytest in print mode
-
- pytest -s

#How to get started docker project
-
- docker-compose up -d

#How to stop docker container
-
- docker-compose down

#How to both build and up the container
-
- docker-compose up --build -d

#How to check container stats
-
- docker stats <container id>

#How to create renter from django shell
- 
-User.objects.create_user(username=fake.simple_profile().get('username'),email=fake.simple_profile().get('mail'), password='testpassword', role="renter")

