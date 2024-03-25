import React, { useState } from "react";
import axios from "axios";
import { useHistory } from "react-router-dom";
import "./SearchBar.css";

function SearchBar() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedGame, setSelectedGame] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [searchedBlog, setSearchedBlog] = useState(null);
  const history = useHistory();


  const handleChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleGameChange = (event) => {
    setSelectedGame(event.target.value);
  };


  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const params = {
        title: searchTerm,
        game: selectedGame,
      };
  
      const filteredParams = Object.fromEntries(
        Object.entries(params).filter(([_, value]) => value !== "")
      );
  
      const response = await axios.get("/blog/get_blog/", {
        baseURL: "http://localhost:8000", 
        params: filteredParams,
      });
      setSearchResults(response.data.blogs);
      if (response.data.blogs.length > 0) {
        setSearchedBlog(response.data.blogs[0]);
      } else {
        setSearchedBlog(null);
      }
    } catch (error) {
      console.error("Error searching:", error);
    }
  };

  const handleBlogClick = (blogId) => {
    history.push(`/blog/${blogId}`);
  };

  const handleInputBlur = () => {
    setSearchResults([]);
  };

  return (
    <div className="search-container">
      <form className="search-bar" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Search..."
          value={searchTerm}
          onChange={handleChange}
          onBlur={handleInputBlur}
          className="search-input"
        />
        <select value={selectedGame} onChange={handleGameChange}>
          <option value="">Select Game</option>
          <option value="EldenRing">Elden Ring</option>
          <option value="Dota2">Dota 2</option>
          <option value="LeagueOfLegends">League of Legends</option>
          <option value="BaldursGate3">Baldurs Gate 3</option>
          <option value="CSGO">CSGO</option>
        </select>
        <button type="submit" className="search-button">
          Search
        </button>
      </form>
      {searchedBlog && (
        <div className="searched-blog" onClick={() => handleBlogClick(searchedBlog.id)}>
        </div>
      )}
      <div className="search-results">
        {searchResults.map((blog) => (
          <div
            key={blog.id}
            className="search-result"
            onClick={() => handleBlogClick(blog.id)}
          >
            <h3>{blog.title}</h3>
            <p>{blog.game}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SearchBar;