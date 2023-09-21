# image base ubuntu 22.04
FROM ubuntu:22.04

# install nodejs
RUN apt-get update && apt-get install -y nodejs

# install npm
RUN apt-get install -y npm

# install express
RUN npm install express

# working directory /home/app
WORKDIR /home/app

# copy all files from current directory to /home/app
COPY . /home/app

# expose port 3000
EXPOSE 3001

# run nodejs
CMD ["nodejs", "app.js"]