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


function makePaperInsertForm() {
    return (
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


function a11yProps(index) {
    return {
        id: `simple-tab-${index}`,
        'aria-controls': `simple-tabpanel-${index}`,
    };
}

class InsertForm extends React.Component {
    constructor(props) {
        super(props);
        this.value = 0;
    }

    handleChange(){}

    render() {
        return (
            <div>
                <AppBar position="static">
                    <Tabs value={this.value} onChange={this.handleChange}>
                        <Tab label="Insert Paper" {...a11yProps(0)} />
                        <Tab label="Insert Scholar" {...a11yProps(1)} />
                    </Tabs>
                </AppBar>
                <TabPanel value={this.value} index={0}>
                    {makePaperInsertForm()}
                </TabPanel>
                <TabPanel value={this.value} index={1}>
                    Item Two
                </TabPanel>
            </div>
        );
    }
}


const mapStateToProps = (state) => {
    return {

    }
}

const mapDispatchToProps = dispatch => {
    return {

    }
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
  )(InsertForm)
