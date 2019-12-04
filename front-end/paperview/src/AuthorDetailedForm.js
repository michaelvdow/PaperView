import React from 'react';
import './page.css';
import { connect } from 'react-redux'
import Graph from 'react-graph-vis'
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import MaterialTable from "material-table";

import * as Constants from './Constants'
import * as selectors from './redux/selectors'
import * as actions from './redux/actions'

class AuthorDetailedForm extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
      
      console.log(this.props.detailData)
    return (
        <div id="AuthorDetailedForm">
            {this.props.detailData.AuthorId ? <Paper style={{overflow: 'auto'}}>
                <Typography variant="h5" component="h3">
                    {this.props.detailData.Name}
                </Typography>
                <Typography component="p">
                    Affiliation: {this.props.detailData.Affiliation}
                </Typography>
                <Typography component="p">
                    Citations: {this.props.detailData.CitedBy}
                </Typography>
                <Typography component="p">
                    H-Index: {this.props.detailData.HIndex}
                </Typography>
                <Typography component="p">
                    I10-Index{this.props.detailData.I10Index}
                </Typography>
                <Paper class="graphPaper">
                    <Table aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell>Interests</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {this.props.detailData.Interests ? this.props.detailData.Interests.map(row => (
                                <TableRow key={row}>
                                <TableCell component="th" scope="row">
                                    {row}
                                </TableCell>
                                </TableRow>
                            )) : null}
                        </TableBody>
                    </Table>
                </Paper>
                
                <Paper class="graphPaper">
                    <MaterialTable
                            options={{
                                search: false
                            }}
                            columns={
                                [
                                    { title: "Article Title", field: "Title", editable: 'never' }
                                ]
                            }
                            data={
                                this.props.detailData.Articles ? this.props.detailData.Articles : []
                            }
                            title="Articles"
                        />
                </Paper>
            </Paper>
            :
            <Paper style={{overflow: 'auto'}}>
                <Typography variant="h5" component="h3">
                    {this.props.detailData.Title}
                </Typography>
                <Typography component="p">
                    {this.props.detailData.Year ? "Primary Author:" + this.props.detailData.PrimaryAuthorName : null}
                </Typography>
                <Typography component="p">
                    {this.props.detailData.Year ? "Year:" + this.props.detailData.Year : null}
                </Typography>
                <Typography component="p">
                    {this.props.detailData.Year ? "Cited By:" + this.props.detailData.CitedBy : null}
                </Typography>
                <Typography component="p">
                    {this.props.detailData.Year ? "Citations:" + this.props.detailData.Citations : null}
                </Typography>

                <Paper class="graphPaper">
                    <MaterialTable
                            options={{
                                search: false
                            }}
                            columns={
                                [
                                    { title: "Names", field: "Name", editable: 'never' }
                                ]
                            }
                            data={
                                this.props.detailData.Authors ? this.props.detailData.Authors : []
                            }
                            title="Authors"
                        />
                </Paper>
            </Paper>
            }
            
        </div>
    ); 
  }
}


const mapStateToProps = (state) => {
    return {
        detailData: selectors.getDetailedData(state),
    }
}

const mapDispatchToProps = dispatch => {
    return {
    }
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(AuthorDetailedForm)
