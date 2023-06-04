import "./ModeratorNotifications.css";

export function ModeratorNotifications(props) {
  let impression;
  switch (props.textToxicity.length) {
    case 1:
      impression = "🤔";
      break;
    case 2:
      impression = "🤨";
      break;
    case 3:
      impression = "😯";
      break;
    case 4:
      impression = "😠";
      break;
    case 5:
      impression = "😡";
      break;
    case 6:
      impression = "🤬";
      break;
    default:
      impression = "";
  }

  const toxicityItems = props.textToxicity.map((item, key) => (
    <div key={key} className="toxicity-item">
      {item}
    </div>
  ));
  return (
    <div className="notifications-wrapper">
      {impression}
      {toxicityItems}
    </div>
  );
}
