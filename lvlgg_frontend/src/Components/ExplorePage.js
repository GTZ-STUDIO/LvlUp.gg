import React from "react";
import "../App.css";
import { Button } from "./Button";
import "./ExplorePage.css";

function ExplorePage() {
  return (
    <div className="explore-container">
      <video src="/videos/video-4.mp4" autoPlay loop muted />
      <h1>EXPLORE GAMES</h1>
      <p>filler text filler text filler text</p>
      <div className="explore-btns">
        <Button
          className="btns"
          buttonStyle="btn--outline"
          buttonSize="btn--large"
        >
          GET STARTED
        </Button>
        <Button
          className="btns"
          buttonStyle="btn--primary"
          buttonSize="btn--large"
        >
          GAME GUIDES <i className="far fa-play-circle" />
        </Button>
      </div>
    </div>
  );
}

export default ExplorePage;
