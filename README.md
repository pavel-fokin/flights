# Flights API

This service has API to create and search information about flights.
JWT tokens are used for authorization.

This app was deployed at Heroku. Swagger documentation is availalble at https://flights-service.herokuapp.com/api/docs/

## Requirments

 - Python >= 3.8

`Makefile` can be used to run few simple commands like `requirements`,
`run`, `lint` and `tests`.

`pip-tools` is using to manage requirements

```sh
(venv) $ pip install pip-tools
```

## Run

 There are few options to run application.

 - First option is to use virtual enviroment.

 Install requirements.
 ```sh
 (venv) $ make install
 ```
 Apply database migrations.
 ```sh
 (venv) $ make migrate
 ```
 Run application.
 ```sh
 (venv) $ make run
 ```

 - To run it with `docker`.
 ```sh
 $ docker build -t flights-service .
 $ docker run --name flights-service -it -p 5000:5000 flights-service run
 ```
 Swagger documentation will be available http://localhost:5000/api/docs/.
 Apply migrations in running docker container.
 ```sh
 $ docker exec -ti flights-service bash
 (docker) $ make migrate 
 ```

Docker image extended with additional packages to make possible run unittests with `docker`.
 ```sh
 $ docker run -it flights-service tests
 ```
