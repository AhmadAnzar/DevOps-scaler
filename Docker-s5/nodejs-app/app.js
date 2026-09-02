const http = require("http");

const port = 3000;

const server = http.createServer((request, response) => {
    response.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    response.end(`<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Node.js Docker App</title></head>
<body><h1>Hello World from Node.js + Docker!</h1></body>
</html>`);
});

server.listen(port, "0.0.0.0", () => {
    console.log(`Node.js app listening on port ${port}`);
});
