import logo from "./logo.svg";
import React, { Component } from "react";
import "./App.css";
const api = "http://localhost:8000/api";
const origin = "http://localhost:3000";

function k() {
  return "52cdcc726dabfbe7356dc273f2f5a238f6d40c10";
}

async function getPortfolio() {
  const portfolio = await fetch(`${api}/portfolio`, {
    method: "GET",
    headers: {
      Authorization: `Token ${k()}`,
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .catch((error) => console.log(error));
  console.log(portfolio);
  return portfolio;
}

function Portfolio() {
  const portfolio = getPortfolio();
  return <div>Portfolio</div>;
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code> src / App.js </code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <Portfolio></Portfolio>
    </div>
  );
}

export default App;
