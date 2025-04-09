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

#What this website is about
- 
- We have two main services at RentBuy HUB
- **Rent Your Cloths**:
- You can list your clothes on our platform and rent them out to our users. 
- We'll take care of the logistics and delivery, so you can earn a passive income from your closet. 
- **Buy Rented Cloths**: If you're looking to purchase high-quality, gently used clothes, you can check out our listings and find great deals on your favorite items.
- Many of our items are available for a lower price than buying new, and you can try before you buy! Both services come with benefits like free delivery for rentals and a safe, secure way to exchange clothes.
- Would you like to know more about how it works?