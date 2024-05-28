const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(cors());

app.post('/complete', async (req, res) => {
    console.log("Received request with body:", req.body);

    const code = req.body.code;

    try {
        const response = await axios.post('http://localhost:5000/complete', { code });
        console.log("Received response from Flask service:", response.data);

        const completion = response.data.completion;
        res.json({ completion });
    } catch (error) {
        console.error("Error in request:", error);
        res.status(500).send(error.toString());
    }
});

app.listen(port, () => {
    console.log(`Middleware server is running on http://localhost:${port}`);
});
