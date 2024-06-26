# Technical Test for White Swan Data on Concurrent Requests

# Setup
  * Clone the repo into an appropriate location
  * Open the Docker Desktop app (or install and open if you do not have it)
  * Open the repo in VSCode (or other editor if you prefer)
  
# Using the Application
  * Step 1: To load the image and then run to initiate the server within a docker service:
    ```bash
    make
    ```
  * Step 2: To Run the actual Application:
    ```bash
    python main.py input.txt addresses.txt output.txt
    ```
  * Step 3: To Run the unit tests:
    ```bash
    python  -m unittest test_main.py
    ```

## Note
  * If you try running make twice it will say the port is already in use and you will need to go and shut it down in docker. 
  * or 
  ```bash
  docker stop $(docker ps -q)
  ```

## Using the proxy image manually

The proxy image (wsd-proxy-test.tar) is a docker image bundled as a tarball. It can be loaded using

```bash
docker load --input /path/to/wsd-proxy-test.tar
```

and then run with default setup (used for our tests) with

```bash
docker run -p "8080:3000" wsd-proxy-test:latest
```

where the http endpoint is bound to port 8080 on the docker host. You can manually set its responses for testing purposes, this is done via an environment variable like so:

```bash
docker run -p "8080:8080" \
  -e "RESPONSE_SEQUENCE=200;2cba8153f2ff;1000|404;;200" \
  wsd-proxy-test:latest
```

## Contact
Ed Pasfield
edward.pasfield@gmail.com
