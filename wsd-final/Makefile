# Define the paths and environment variables
DOCKER_IMAGE_PATH=../wsd-proxy-test.tar
DOCKER_IMAGE_NAME=wsd-proxy-test:latest
PORT1=8080
PORT2=3000
RESPONSE_SEQUENCE=200;2cba8153f2ff;1000|404;;200
INPUT_FILE=input.txt
ADDRESSES_FILE=addresses.txt
OUTPUT_FILE=output.txt

# Default target
all: run_docker_container

# Load the Docker image
load_docker_image:
	docker load --input $(DOCKER_IMAGE_PATH)

# Run the Docker container
run_docker_container:
	docker run -d -p "$(PORT1):$(PORT2)" \
	  $(DOCKER_IMAGE_NAME)


.PHONY: all load_docker_image run_docker_container run_main_and_tests_new