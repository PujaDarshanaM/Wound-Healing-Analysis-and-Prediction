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

    let parsedData;
    try {
        parsedData = bluebutton(ccdFile);
    } catch (err) {
        return res.status(500).json({ error: "CCD parsing failed", details: err.message });
    }

    if (!parsedData || !parsedData.data) {
        return res.status(500).json({ error: "Parsed data is undefined. File may not be a valid CCD." });
    }

    // Debug print
    console.log("✅ Parsed CCD Data:", JSON.stringify(parsedData.data, null, 2));

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
