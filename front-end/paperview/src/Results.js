import React from 'react';
import './Results.css';
import Button from '@material-ui/core/Button';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import * as selectors from './redux/selectors'
import * as actions from './redux/actions'
import * as Constants from './Constants'
import { connect } from 'react-redux'


class Results extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="Results">
                <Paper id="resultsTable">
                    <Table>
                        <TableHead>
                        <TableRow>
                            <TableCell>{this.props.searchType === Constants.AUTHOR ? "Author" : "Article"} Name</TableCell>
                            <TableCell align="right">Details</TableCell>
                            <TableCell align="right">Remove</TableCell>
                        </TableRow>
                        </TableHead>
                        <TableBody>
                        {this.props.data.map(row => (
                            <TableRow key={row.name}>
                                <TableCell component="th" scope="row">
                                    {row.name}
                                </TableCell>

                                <TableCell align="right">
                                    <Button onClick={() => this.props.onDetailsClick(this.props.searchType === Constants.AUTHOR ? row.authorId : row.articleId)}
                                    variant="contained"
                                    color="primary">
                                        Details
                                    </Button>
                                </TableCell>

                                <TableCell align="right">
                                    <Button onClick={() => this.props.onDeleteClick(this.props.searchType === Constants.AUTHOR ? row.authorId : row.articleId)}
                                    variant="contained" 
                                    color="secondary">
                                        Delete
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                        </TableBody>
                    </Table>
                </Paper>
                
            </div>  
        );
    }
}

const mapStateToProps = (state) => {
    return {
        searchType: selectors.getSearchType(state),
        data: selectors.getSearchData(state)
    }
}

const mapDispatchToProps = dispatch => {
    return {
        onDetailsClick: (id) => dispatch(actions.onDetailsClick(id)),
        onDeleteClick: (id) => dispatch(actions.onDeleteClick(id))
    }
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
  )(Results)
