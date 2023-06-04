import "./App.css";
import { UserText } from "./components/UserText";
import { ModeratorNotifications } from "./components/ModeratorNotifications";

import { useState } from "react";
import { useEffect } from "react";

import * as toxicityClassifier from "@tensorflow-models/toxicity";

function App() {
  const [textToxicity, setTextToxicity] = useState([]);
  const [model, setModel] = useState(null);

  const predictToxicity = async (event) => {
    const predictions = await model.classify([event.target.value]);
    setTextToxicity(
      // Sets the "textToxicity" array
      // to the predictions after some filtering and mapping.
      // (console.log) the predictions to see
      // from where this came from.
      predictions
        .filter((item) => item.results[0].match === true)
        .map((item) => item.label)
    );
  };

  useEffect(() => {
    async function loadModel() {
      // "threshold" The the confidence interval for the classier.
      // Higher values = the model is more confident about its prediction.
      const threshold = 0.6;
      const toxicityModel = await toxicityClassifier.load(threshold);
      setModel(toxicityModel);
    }
    if (model === null) {
      // Only load the model if its current value is null
      loadModel();
    }
  }, [textToxicity, model]); // Watch the values for those and execute when changed.

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
