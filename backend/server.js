const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

// store latest detection
let latestResult = {
  animal: "None",
  confidence: 0,
  status: "Idle",
};

// API to receive prediction from Python
app.post("/update", (req, res) => {
  latestResult = req.body;
  res.json({ message: "Updated" });
});

// API for frontend to read result
app.get("/status", (req, res) => {
  res.json(latestResult);
});

app.listen(5000, () => {
  console.log("✅ Server running on http://localhost:5000");
});
