up:
	docker-compose up -d --build

down:
	docker-compose down

restart:
	docker-compose restart app

logs:
	docker-compose logs -f --tail=200
