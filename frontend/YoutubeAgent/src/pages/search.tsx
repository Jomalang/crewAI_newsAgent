import axios from "axios";
import { useState } from "react";
import "./search.css";
import loading from "../assets/gif/loading.gif";

const Search = () => {
  const [search, setSearch] = useState("");
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/ask", {
        url: search,
      });
      console.log(response.data);
      setResults(response.data.result);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
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
        {isLoading ? (
          <div className="loading">
            <img src={loading} alt="loading..." />
          </div>
        ) : (
          <p>{results}</p>
        )}
      </div>
    </div>
  );
};

export default Search;
