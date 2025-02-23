const express = require("express");
const fileUpload = require("express-fileupload");
const cors = require("cors");
const bluebutton = require("bluebutton");

const app = express();
app.use(cors());
app.use(fileUpload());

// API endpoint to handle CCD file upload
app.post("/parse_ccd", (req, res) => {
    if (!req.files || !req.files.ccd) {
        return res.status(400).json({ error: "No file uploaded" });
    }

    const ccdFile = req.files.ccd.data.toString("utf8");
    const parsedData = bluebutton(ccdFile);

    // Debug: Log entire parsed output
    console.log("Parsed CCD Data:", JSON.stringify(parsedData.data, null, 2));

    // Try extracting from different places
    const diagnoses = parsedData.data.conditions || parsedData.data.problems || parsedData.data.diagnoses || [];

    res.json({
        patient: parsedData.data.demographics || {},
        allergies: parsedData.data.allergies || [],
        medications: parsedData.data.medications || [],
        diagnoses: diagnoses
    });
});

// Start the server
const PORT = 5000;
app.listen(PORT, () => console.log(` Server running on port ${PORT}`));
