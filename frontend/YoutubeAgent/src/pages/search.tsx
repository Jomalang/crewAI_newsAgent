import axios from "axios";
import { useState } from "react";
import "./search.css";

const Search = () => {
  const [search, setSearch] = useState("");
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    const response = await axios.post("http://localhost:8000/ask", {
      url: search,
    });
    console.log(response.data);
    setResults(response.data.result);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
  };

  return (
    <div className="container">
      <div className="title">
        <h1>Youtube Agent</h1>
      </div>
      <div className="search-container">
        <input type="text" placeholder="Search" onChange={handleInputChange} />
        <button onClick={handleSearch}>검색</button>
      </div>

      <div className="results">
        <p>{results}</p>
      </div>
    </div>
  );
};

export default Search;
