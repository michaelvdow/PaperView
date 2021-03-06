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


function AuthorInsertForm(props) {
    return (
        <div id = "authorInsertFields">
            <Grid container spacing={3} id="InsertForm">
                <Grid item xs={12}>
                    <TextField
                        required
                        id="name"
                        name="name"
                        label="Name"
                        autoComplete="name"
                        fullWidth
                        onChange={(event, index, value) => props.onInsertAuthorNameChange(event.target.value)}
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
                        onChange={(event, index, value) => props.onInsertAuthorAffilicationChange(event.target.value)}
                    />
                </Grid>
                <Grid item xs={12} sm={6}>
                    <TextField
                        id="citationNumber"
                        name="citationNumber"
                        label="Citation number"
                        autoComplete="citationNumber"
                        fullWidth
                        onChange={(event, index, value) => props.onInsertAuthorCitationChange(event.target.value)}
                    />
                </Grid>
                <Grid item xs={12} sm={3}>
                    <TextField
                        id="hIndex"
                        name="hIndex"
                        label="H-Index"
                        autoComplete="hIndex"
                        fullWidth
                        onChange={(event, index, value) => props.onInsertAuthorHChange(event.target.value)}
                    />
                </Grid>
                <Grid item xs={12} sm={3}>
                    <TextField
                        id="i10Index"
                        name="i10Index"
                        label="I10-Index"
                        autoComplete="i10Index"
                        fullWidth
                        onChange={(event, index, value) => props.onInsertAuthorI10Change(event.target.value)}
                    />
                </Grid>
                <Grid item xs={12} sm={12}>
                    <TextField
                        id="interest"
                        name="interest"
                        label="Interest"
                        autoComplete="interest"
                        fullWidth
                        onChange={(event, index, value) => props.onInsertAuthorInterestChange(event.target.value)}
                    />
                </Grid>
            </Grid>
        </div>
    );
}

function PaperInsertForm(props) {
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
                            onChange={(event, index, value) => props.onInsertArticleTitleChange(event.target.value)}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            required
                            id="primaryAuthorName"
                            name="primaryAuthorName"
                            label="Primary author name"
                            autoComplete="authorName"
                            fullWidth
                            onChange={(event, index, value) => props.onInsertArticleAuthorNameChange(event.target.value)}
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
                            onChange={(event, index, value) => props.onInsertArticleURLChange(event.target.value)}
                        />
                    </Grid>
                    <Grid item xs={12} sm={4}>
                        <TextField
                            required
                            id="citedBy"
                            name="citedBy"
                            label="Cited by"
                            autoComplete="citedBy"
                            fullWidth
                            onChange={(event, index, value) => props.onInsertArticleCitedByChange(event.target.value)}
                        />
                    </Grid>
                    <Grid item xs={12} sm={4}>
                        <TextField
                            required
                            id="citations"
                            name="citations"
                            label="Citations"
                            autoComplete="citations"
                            fullWidth
                            onChange={(event, index, value) => props.onInsertArticleCitationsChange(event.target.value)}
                        />
                    </Grid>
                    <Grid item xs={12} sm={4}>
                        <TextField
                            required
                            id="year"
                            name="year"
                            label="Year"
                            autoComplete="year"
                            fullWidth
                            onChange={(event, index, value) => props.onInsertArticleYearChange(event.target.value)}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            required
                            id="publisher"
                            name="publisher"
                            label="Publisher"
                            autoComplete="publisher"
                            fullWidth
                            onChange={(event, index, value) => props.onInsertArticlePublisherChange(event.target.value)}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            required
                            id="journalName"
                            name="journalName"
                            label="Journal name"
                            autoComplete="journalName"
                            fullWidth
                            onChange={(event, index, value) => props.onInsertArticleJournalChange(event.target.value)}
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

    render() {
        return (
            <div id = "insertFields">
                <AppBar position="static" color = "inherit" id = "appBar">
                    <Tabs value={this.props.tab} onChange={(event, newValue) => this.props.setTab(newValue)} centered indicatorColor="primary" textColor="primary">
                        <Tab label="Insert Paper" />
                        <Tab label="Insert Scholar" />
                    </Tabs>
                </AppBar>
                <TabPanel value={this.props.tab} index={0} >
                    {PaperInsertForm(this.props)}
                </TabPanel>
                <TabPanel value={this.props.tab} index={1}>
                    {AuthorInsertForm(this.props)}
                </TabPanel>
                <Button id="submitButton" variant="contained" color="primary" onClick={() => this.props.onInsertSubmit()}>
                    Submit
                </Button>
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
        onInsertSubmit: () => dispatch(actions.onInsertSubmit()),
        setTab: (value) => dispatch(actions.setAuthorPaperTab(value)),
        onInsertAuthorNameChange: (input) => dispatch(actions.onInsertAuthorNameChange(input)),
        onInsertAuthorEmailChange: (input) => dispatch(actions.onInsertAuthorEmailChange(input)),
        onInsertAuthorAffilicationChange: (input) => dispatch(actions.onInsertAuthorAffilicationChange(input)),
        onInsertAuthorCitationChange: (input) => dispatch(actions.onInsertAuthorCitationChange(input)),
        onInsertAuthorHChange: (input) => dispatch(actions.onInsertAuthorHChange(input)),
        onInsertAuthorI10Change: (input) => dispatch(actions.onInsertAuthorI10Change(input)),
        onInsertAuthorInterestChange: (input) => dispatch(actions.onInsertAuthorInterestChange(input)),
        onInsertArticleTitleChange: (input) => dispatch(actions.onInsertArticleTitleChange(input)),
        onInsertArticleAuthorNameChange: (input) => dispatch(actions.onInsertArticleAuthorNameChange(input)),
        onInsertArticleURLChange: (input) => dispatch(actions.onInsertArticleURLChange(input)),
        onInsertArticleCitedByChange: (input) => dispatch(actions.onInsertArticleCitedByChange(input)),
        onInsertArticleCitationsChange: (input) => dispatch(actions.onInsertArticleCitationsChange(input)),
        onInsertArticleYearChange: (input) => dispatch(actions.onInsertArticleYearChange(input)),
        onInsertArticlePublisherChange: (input) => dispatch(actions.onInsertArticlePublisherChange(input)),
        onInsertArticleJournalChange: (input) => dispatch(actions.onInsertArticleJournalChange(input))
    }
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
  )(InsertForm)
