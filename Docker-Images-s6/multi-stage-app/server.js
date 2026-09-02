const express = require("express");

const app = express();
const port = 3000;

app.get("/", (request, response) => {
    response.send("<h1>Hello World from Docker multi-stage build</h1>");
});

app.listen(port, "0.0.0.0", () => {
    console.log(`Application listening on port ${port}`);
});
