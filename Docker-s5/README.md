# Docker Fundamentals

**Name:** Anzar, 24BCS10289

## 1. Node.js
```bash
docker build -t hello-node ./nodejs-app
docker run -d --name hello-node -p 3000:3000 hello-node
curl http://localhost:3000
```

![Node.js output](node-output.png)

## 2. Python

```bash
docker build -t hello-python ./python-app
docker run -d --name hello-python -p 8000:8000 hello-python
curl http://localhost:8000
```

![Python output](python-output.png)

## 3. Java

```bash
docker build -t hello-java ./java-app
docker run -d --name hello-java -p 8080:8080 hello-java
curl http://localhost:8080
```

![Java output](java-output.png)

## 4. Apache HTTP Server

```bash
docker build -t hello-apache ./apache-app
docker run -d --name hello-apache -p 8081:80 hello-apache
curl http://localhost:8081
```

![Apache output](apache-output.png)

## 5. React

```bash
docker build -t hello-react ./React-app
docker run -d --name hello-react -p 8082:80 hello-react
curl http://localhost:8082
```

![React output](react-output.png)

## 6. Nginx

```bash
docker build -t hello-nginx ./nginx-app
docker run -d --name hello-nginx -p 8083:80 hello-nginx
curl http://localhost:8083
```

![Nginx output](nginx-output.png)

## ALL TOGETHER: 

```bash
docker ps --filter "name=hello-"
```
