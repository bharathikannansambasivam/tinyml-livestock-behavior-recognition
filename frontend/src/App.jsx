import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState({
    animal: "Loading...",
    confidence: 0,
    status: "Waiting",
  });

  useEffect(() => {
    const interval = setInterval(() => {
      axios
        .get("http://localhost:5000/status")
        .then((res) => setData(res.data))
        .catch(() => {});
    }, 500); // refresh every 0.5 sec

    return () => clearInterval(interval);
  }, []);

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        fontFamily: "Arial",
      }}
    >
      <div
        style={{
          padding: "40px",
          borderRadius: "12px",
          boxShadow: "0 0 20px rgba(0,0,0,0.2)",
          textAlign: "center",
        }}
      >
        <h1>🐄 Livestock Monitoring Dashboard</h1>

        <h2>Animal: {data.animal}</h2>
        <h2>Confidence: {data.confidence}%</h2>
        <h2>Status: {data.status}</h2>
      </div>
    </div>
  );
}

export default App;
