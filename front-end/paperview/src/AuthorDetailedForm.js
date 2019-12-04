import React from 'react';
import './page.css';
import { connect } from 'react-redux'
import Graph from 'react-graph-vis'
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';

import * as Constants from './Constants'
import * as selectors from './redux/selectors'
import * as actions from './redux/actions'

class AuthorDetailedForm extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
        <div id="AuthorDetailedForm">
            <Paper>
                <Typography variant="h5" component="h3">
                    {this.props.detailData.Name}
                </Typography>
                <Typography component="p">
                    {this.props.detailData.Affiliation}
                </Typography>
            </Paper>
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
