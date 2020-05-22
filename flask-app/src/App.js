import React from 'react';
import logo from './logo.svg';
import './App.css';
import Main from './Main'
import MainAdvanced from './MainAdvanced'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Router>
        <ul>
          <li>
            <Link to="/basic">basic</Link>
          </li>
          <li>
            <Link to="/advanced">advanced</Link>
          </li>
        </ul>
        <Switch>
          <Route path="/basic" exact component={Main}>
          </Route>
          <Route path="/advanced" exact component={MainAdvanced}>
          </Route>
        </Switch>



      </Router>

    </div>
  );
}

export default App;
