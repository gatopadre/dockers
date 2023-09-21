# creating a base nodejs enviroment for any project

- using ubuntu:22.04 as base image
- installing nodejs
- installing npm


# usefull commands 
´docker-compose up´
´docker-compose down´

- en la terminal:
´docker run -it --entrypoint /bin/bash image_id´

- en la terminal:
´docker system prune´

# files explanation:
- Dockerfile: 
    - contains the instructions to build the image
- docker-compose.yml:
    - contains the instructions to run the container
- .dockerignore:
    - contains the files to ignore when building the image
- .gitignore:
    - contains the files to ignore when pushing to git