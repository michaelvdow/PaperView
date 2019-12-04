import React from 'react';
import './page.css';
import { connect } from 'react-redux'
import Graph from 'react-graph-vis'

import * as Constants from './Constants'
import * as selectors from './redux/selectors'
import * as actions from './redux/actions'


function AuthorDetailedForm(props) {
    console.log(props.data);
    return (
        <div id = "AuthorDetailedForm">
            <p Hi />
        </div>
    );
}

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
        width: "600px",
        "physics": {
            "barnesHut": {
                "springConstant": 0.05,
                "avoidOverlap": 0.3
            }
        },
        nodes:{
            shape: 'ellipse',
            widthConstraint: {
                maximum: 150   
            }
        },
        margin: 1
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
        <div>
            {AuthorDetailedForm(this.props)}
            <Graph graph={this.props.graph} options={this.options} events={this.events} />
        </div>
    ); 
  }
}


const mapStateToProps = (state) => {
    return {
        tab: selectors.getMainTab(state),
        graph: selectors.getGraph(state),
        data: selectors.getDetailedData(state)
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
