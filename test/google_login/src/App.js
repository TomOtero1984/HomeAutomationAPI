import logo from './logo.svg';
import { useEffect, useState } from 'react';
import jwt_decode from "jwt-decode";
import './App.css';

function App() {
  const [user, setUser] = useState({})

  function handleCallbackResponse(response) { 
    console.log("Encoded JWT ID token: " + response.credential);
    var userObject = jwt_decode(response.credential);
    console.log(userObject);
    setUser(userObject)
  }

  useEffect(() => {
    /* global google */
    google.accounts.id.initialize({
      client_id: "401964866605-rordq63u2emnt8avs0gag0pakri4mh2c.apps.googleusercontent.com",
      callback: handleCallbackResponse
    });

    google.accounts.id.renderButton(
      document.getElementById("signInDiv"),
      { theme: "outline", size: "large"}
    )
  }, []);

  return (
    <div className="App">
      <div id="signInDiv"></div>
    </div>
  );
}

export default App;
