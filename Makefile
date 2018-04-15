run: initdb
	docker-compose -f docker-compose.yaml up

initdb:
	docker-compose -f docker-compose.yaml run web scripts/initdb.sh

create-user:
	docker-compose -f docker-compose.yaml run web scripts/create_super_user.sh

