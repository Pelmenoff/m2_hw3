1. docker build -t web_app
2. docker run -it -p 3000:3000 -p 5000:5000 -v [PATH TO FOLDER]:/app/web/storage web_app