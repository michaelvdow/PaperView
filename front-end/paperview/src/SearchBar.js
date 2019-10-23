import React from 'react';
import './SearchBar.css';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';

class SearchBar extends React.Component {
    constructor(props) {
        super(props);
        this.onSubmit = this.onSubmit.bind(this);
        this.handleOnChange = this.handleOnChange.bind(this);
        this.state = {input: ""};
    }

    // Call api and get data, then display it
    onSubmit(e) {
        let input = this.state.input;
        console.log(input)
    }

    handleOnChange(e) {
        this.setState({input: e.target.value})
    }

    render() {
        return (
            <div className="SearchBar">
                <TextField
                    id="searchField"
                    label="Search"
                    className="searchField"
                    margin="normal"
                    onChange={this.handleOnChange}
                />
                <Button id="submitButton" onClick={this.onSubmit}>
                    Submit
                </Button>
            </div>  
        );
    }
}

export default SearchBar;
