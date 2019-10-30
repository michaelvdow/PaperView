import React from 'react';
import './Insert.css';
import { connect } from 'react-redux'
import AppBar from '@material-ui/core/AppBar';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';

import * as Constants from './Constants'
import * as selectors from './redux/selectors'
import * as actions from './redux/actions'


function makeAuthorInsertForm() {
    return (
        <React.Fragment>
            <Grid container spacing={3} id="InsertForm">
                <Grid item xs={12}>
                    <TextField
                        required
                        id="name"
                        name="name"
                        label="Name"
                        autoComplete="name"
                        fullWidth
                    />
                </Grid>
                <Grid item xs={12}>
                    <TextField
                        required
                        id="email"
                        name="email"
                        label="Email"
                        autoComplete="email"
                        fullWidth
                    />
                </Grid>
                <Grid item xs={12}>
                    <TextField
                        required
                        id="affiliation"
                        name="affiliation"
                        label="Affiliation"
                        autoComplete="affiliation"
                        fullWidth
                    />
                </Grid>
                <Grid item xs={12} sm={6}>
                    <TextField
                        id="citationNumber"
                        name="citationNumber"
                        label="Citation number"
                        autoComplete="citationNumber"
                        fullWidth
                    />
                </Grid>
                <Grid item xs={12} sm={3}>
                    <TextField
                        id="hIndex"
                        name="hIndex"
                        label="H-Index"
                        autoComplete="hIndex"
                        fullWidth
                    />
                </Grid>
                <Grid item xs={12} sm={3}>
                    <TextField
                        id="i10Index"
                        name="i10Index"
                        label="I10-Index"
                        autoComplete="i10Index"
                        fullWidth
                    />
                </Grid>
            </Grid>
        </React.Fragment>
    );
}

function makePaperInsertForm() {
    return (
        <div id = "paperInsertFields">
            <React.Fragment>
                <Grid container spacing={3} id="InsertForm">
                    <Grid item xs={12}>
                        <TextField
                            required
                            id="title"
                            name="title"
                            label="Title"
                            autoComplete="title"
                            fullWidth
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            required
                            id="authorName"
                            name="authorName"
                            label="Author name"
                            autoComplete="authorName"
                            fullWidth
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            required
                            id="url"
                            name="url"
                            label="Url"
                            autoComplete="url"
                            fullWidth
                        />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <TextField
                            id="citationNumber"
                            name="citationNumber"
                            label="Citation number"
                            autoComplete="citationNumber"
                            fullWidth
                        />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <TextField
                            required
                            id="year"
                            name="year"
                            label="Year"
                            autoComplete="year"
                            fullWidth
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            id="journalName"
                            name="journalName"
                            label="Journal name"
                            autoComplete="journalName"
                            fullWidth
                        />
                    </Grid>
                </Grid>
            </React.Fragment>
        </div>
    );
}

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


class InsertForm extends React.Component {
    constructor(props) {
        super(props);
    }

    handleChange(){}

    render() {
        return (
            <div>
                <AppBar position="static" color = "inherit">
                    <Tabs value={this.props.tab} onChange={(event, newValue) => this.props.setTab(newValue)} centered indicatorColor="primary" textColor="primary">
                        <Tab label="Insert Paper" />
                        <Tab label="Insert Scholar" />
                    </Tabs>
                </AppBar>
                <TabPanel value={this.props.tab} index={0}>
                    {makePaperInsertForm()}
                </TabPanel>
                <TabPanel value={this.props.tab} index={1}>
                    {makeAuthorInsertForm()}
                </TabPanel>
            </div>
        );
    }
}


const mapStateToProps = (state) => {
    return {
        panel: selectors.getPanel(state),
        tab: selectors.getAuthorPaperTab(state)
    }
}

const mapDispatchToProps = dispatch => {
    return {
        setTab: (value) => dispatch(actions.setAuthorPaperTab(value))
    }
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
  )(InsertForm)
