import "./UserText.css";

export function UserText(props) {
  return (
    <textarea
      className="center"
      onChange={props.predictToxicity}
      onBlur={props.predictToxicity}
      placeholder="Type here..."
    ></textarea>
  );
}
