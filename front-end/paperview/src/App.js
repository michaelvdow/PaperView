import React from 'react';
import { connect } from 'react-redux'
import SearchBar from './SearchBar.js'
import Details from './Details.js'
import InsertForm from './Insert.js'
import './App.css';
import * as Constants from './Constants'
import * as selectors from './redux/selectors'

/*
class App extends React.Component {
  render() {
    return (
      <div className="App">
        {this.props.panel === Constants.PANEL_SEARCH ? <SearchBar/> : null}
        {this.props.panel === Constants.PANEL_DETAILS ? <Details/> : null}
      </div>
    );
  }
}
*/

// Just to test the functionality of insert (using PANEL_SEARCH, will change)
class App extends React.Component {
  render() {
    return (
      <div className="App">
        {this.props.panel === Constants.PANEL_SEARCH ? <InsertForm/> : null}
      </div>
    );
  }
}


const mapStateToProps = (state) => {
  return {
      panel: selectors.getPanel(state)
  }
}

const mapDispatchToProps = dispatch => {
  return {}
}


export default connect(
  mapStateToProps,
  mapDispatchToProps
)(App)

