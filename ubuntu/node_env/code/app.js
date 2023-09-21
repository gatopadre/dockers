const express = require('express');
const app = express();
const port = 3001; // Puerto en el que se ejecutará la aplicación

// Ruta de ejemplo para la página principal
app.get('/', (req, res) => {
    res.send('¡Hola, gente desde Express.js!');
});