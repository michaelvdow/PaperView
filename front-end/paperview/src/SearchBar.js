import React from 'react';
import './SearchBar.css';
import { connect } from 'react-redux'
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Results from './Results'
import Select from '@material-ui/core/Select';
import FormControl from '@material-ui/core/FormControl';
import MenuItem from '@material-ui/core/MenuItem';
import * as Constants from './Constants'
import * as actions from './redux/actions'


class SearchBar extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div id="searchBar">
                <div id="searchFields">
                    <FormControl id="searchFieldSelector">
                        <Select
                            value={this.props.searchType}
                            onChange={(event) => this.props.onSearchTypeChange(event.target.value)}
                            inputProps={{
                                name: 'type',
                                id: 'type',
                            }}
                            >
                            <MenuItem value={Constants.AUTHOR}>Author</MenuItem>
                            <MenuItem value={Constants.ARTICLE}>Article</MenuItem>
                        </Select>
                    </FormControl>

                    <TextField
                        id="searchFieldSearch"
                        label="Search"
                        margin="normal"
                        onChange={(event, index, value) => this.props.onTextChange(event.target.value)}
                    />

                    <Button id="searchFieldButton" variant="contained" color="primary" onClick={() => this.props.onSubmit()}>
                        Submit
                    </Button>
                </div>
            
                <Results/>
            </div>  
        );
    }
}

const mapStateToProps = (state) => {
    return {
        searchType: state.searchType
    }
}

const mapDispatchToProps = dispatch => {
    return {
        onSubmit: () => dispatch(actions.onSubmit()),
        onTextChange: (input) => dispatch(actions.onTextChange(input)),
        onSearchTypeChange: (input) => dispatch(actions.onSearchTypeChange(input))
    }
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
  )(SearchBar)
