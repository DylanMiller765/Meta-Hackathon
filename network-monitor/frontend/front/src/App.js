import React, { useState } from "react";
import "./App.css";  // Import styles for this component

function App() {
  const [ip, setIp] = useState(""); // State for storing IP input

  // Handle IP address change in the input field
  const handleIpChange = (event) => {
    setIp(event.target.value);
  };

  // Handle form submission
  const handleSubmit = (event) => {
    event.preventDefault();
    alert("IP Address Submitted: " + ip);
  };

  return (
    <div className="App">
      <h1>Enter IP Address</h1>
      <form onSubmit={handleSubmit}>
        <label>
          IP Address:
          <input
            type="text"
            value={ip}
            onChange={handleIpChange}  // Update state on change
            placeholder="Enter IP"
          />
        </label>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default App;
