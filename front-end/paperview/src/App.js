import React from 'react';
import { connect } from 'react-redux'
import AppBar from '@material-ui/core/AppBar'
import Tabs from '@material-ui/core/Tabs'
import Tab from '@material-ui/core/Tab'
import Typography from '@material-ui/core/Typography'
import Box from '@material-ui/core/Box'
import SearchBar from './SearchBar.js'
import InsertForm from './Insert.js'
import Snackbar from '@material-ui/core/Snackbar';
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';

import './App.css';
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
          <SearchBar/>
        </TabPanel>
        <TabPanel value={this.props.tab} index={1}>
         <InsertForm/>
        </TabPanel>
        <Snackbar
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
          open={this.props.isSnackBarOpen}
          autoHideDuration={4000}
          onClose={(event, reason) => this.props.onSnackBarClose(reason)}
          message={<span id="message-id">{this.props.snackBarMessage}</span>}
          action={[
            <IconButton
              key="close"
              aria-label="close"
              color="inherit"
              onClick={() => this.props.onSnackBarClose("idk")}
            >
              <CloseIcon />
            </IconButton>,
          ]}
      />
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
      tab: selectors.getMainTab(state),
      isSnackBarOpen: selectors.isSnackBarOpen(state),
      snackBarMessage: selectors.getSnackBarMessage(state)
  }
}

const mapDispatchToProps = dispatch => {
  return {
    setTab: (value) => dispatch(actions.setMainTab(value)),
    onSnackBarClose: (reason) => dispatch(actions.onSnackBarClose(reason)),
  }
}


export default connect(
  mapStateToProps,
  mapDispatchToProps
)(App)

