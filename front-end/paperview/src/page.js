import React from 'react';
import './page.css';
import { connect } from 'react-redux'
import Graph from 'react-graph-vis'

import * as Constants from './Constants'
import * as selectors from './redux/selectors'
import * as actions from './redux/actions'

/*
function AuthorDetailedForm(props) {
    return (
        <div id = "AuthorDetailedForm">
            <p "name: = " + this.props.
        </div>



    )
}
*/

class NeoGraph extends React.Component {
  constructor(props) {
    super(props);
    this.options = {
        layout: {
            hierarchical: false
        },
        edges: {
            color: "#000000"
        },
        height: "600px",
        width: "600px"
    };
    this.events = {
        select: function(event) {
        var { nodes, edges } = event;
        console.log("Selected nodes:");
        console.log(nodes);
        console.log("Selected edges:");
        console.log(edges);
        }
    };
  }

  render() {
    return (
        <Graph graph={this.props.graph} options={this.options} events={this.events} />
        
    ); 
  }
}


const mapStateToProps = (state) => {
    return {
        tab: selectors.getMainTab(state),
        graph: selectors.getGraph(state)
    }
}

const mapDispatchToProps = dispatch => {
    return {
    }
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(NeoGraph)
