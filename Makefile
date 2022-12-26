# include .env
# # ENV_VARS = $(shell sed -nr "s@^([A-Za-z_]+): (.+)@\1=\2@ p" env-vars-local.yaml)
# ENV_VARS = $(shell cat .env)

# env_setup:
# 	$(foreach v,$(ENV_VARS),$(eval export $(v)))

# run_local: env_setup
# 	flask run

remove_simbolic_links:
	rm nsj_rest_lib
	rm tests

create_simbolic_links:
	ln -s ./../nsj_rest_lib/src/nsj_rest_lib/ ./
	ln -s ./../nsj-rest-test-util/tests/ ./

recreate_simbolic:
	make remove_simbolic_links
	make create_simbolic_links

recreate_image:
	make down 
	docker rmi -f pcp
	docker build -t pcp ./

recreate_up:
	make recreate_image
	make up

up_redis:
	docker-compose up -d --remove-orphan redis_cache
	docker-compose logs -f

up:
	docker-compose up -d app
	docker-compose up -d postgres
	docker-compose up -d redis_cache 
	docker-compose logs -f

upa:
	docker-compose up -d postgres
	docker-compose up -d redis_cache
	docker-compose logs -f

down:
	docker-compose down

up_postgres:
	docker-compose up -d postgres
	docker-compose logs -f