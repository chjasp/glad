import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [videoId, setVideoId] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("/api/transcribe", { video_id: videoId});
      alert("Transcription job started.");
    } catch (error) {
      console.error("Error starting transcription job: ", error);
      alert("An error occured while starting the transcription job.")
    }
  };

  return (
    <div>
      <h1>Gulch</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={videoId}
          onChange={(e) => setVideoId(e.target.value)}>
        </input>
        <button type="submit">Transcribe</button>
      </form>
    </div>
  )

}

export default App;