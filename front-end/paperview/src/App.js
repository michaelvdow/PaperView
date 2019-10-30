import React from 'react';
import { connect } from 'react-redux'
import AppBar from '@material-ui/core/AppBar'
import Tabs from '@material-ui/core/Tabs'
import Tab from '@material-ui/core/Tab'
import Typography from '@material-ui/core/Typography'
import Box from '@material-ui/core/Box'

import SearchBar from './SearchBar.js'
import Details from './Details.js'
import InsertForm from './Insert.js'
import './App.css';
import * as Constants from './Constants'
import * as selectors from './redux/selectors'
import * as actions from './redux/actions'

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <Typography
      component="div"
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      <Box p={3}>{children}</Box>
    </Typography>
  );
}

class App extends React.Component {
  render() {
    return (
      <div className="App">
        <AppBar position="static">
          <Tabs value={this.props.tab} onChange={(event, newValue) => this.props.setTab(newValue)}>
            <Tab label="Search" />
            <Tab label="Insert" />
          </Tabs>
        </AppBar>
        <TabPanel value={this.props.tab} index={0}>
          {this.props.panel === Constants.PANEL_SEARCH ? <SearchBar/> : null}
          {this.props.panel === Constants.PANEL_DETAILS ? <Details/> : null}
        </TabPanel>
        <TabPanel value={this.props.tab} index={1}>
         <InsertForm/>
        </TabPanel>
      </div>
    );
  }
}

// Just to test the functionality of insert (using PANEL_SEARCH, will change)
// class App extends React.Component {
//   render() {
//     return (
//       <div className="App">
//         {this.props.panel === Constants.PANEL_SEARCH ? <InsertForm/> : null}
//       </div>
//     );
//   }
// }


const mapStateToProps = (state) => {
  return {
      panel: selectors.getPanel(state),
      tab: selectors.getMainTab(state)
  }
}

const mapDispatchToProps = dispatch => {
  return {
    setTab: (value) => dispatch(actions.setMainTab(value)),
  }
}


export default connect(
  mapStateToProps,
  mapDispatchToProps
)(App)

