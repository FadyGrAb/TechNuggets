import "./App.css";
import { UserText } from "./components/UserText";
import { ModeratorNotifications } from "./components/ModeratorNotifications";

import { useState } from "react";

function App() {
  // const [userText, setUserText] = useState("");
  const [textToxicity, setTextToxicity] = useState([]);

  const predictToxicity = (event) => {
    // setUserText(event.target.value);
    setTextToxicity(["toxic", "insult"]);
  };

  return (
    <div>
      <h1 className="title">Start Typing ... </h1>
      <UserText predictToxicity={predictToxicity}></UserText>
      <ModeratorNotifications
        textToxicity={textToxicity}
      ></ModeratorNotifications>
    </div>
  );
}

export default App;
