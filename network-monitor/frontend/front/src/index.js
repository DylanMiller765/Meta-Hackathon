import React from "react";
import ReactDOM from "react-dom";
import App from "./App";  // Import App component
import "./index.css";  // Import global styles (optional)
import "./App.css";    // Import component-specific styles (optional)

ReactDOM.render(
  <React.StrictMode>
    <App />  {/* Render App component */}
  </React.StrictMode>,
  document.getElementById("root")
);
