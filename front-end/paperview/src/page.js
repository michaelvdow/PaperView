import React from 'react';
import './page.css';
import { connect } from 'react-redux'
import Graph from 'react-graph-vis'
import AuthorDetailForm from './AuthorDetailedForm'

import * as Constants from './Constants'
import * as selectors from './redux/selectors'
import * as actions from './redux/actions'

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
        width: "800px",
        "physics": {
            "barnesHut": {
                "avoidOverlap": 0.5,
                damping: 0.2,
                springConstant: 0.01
            }
        },
        nodes:{
            shape: 'ellipse',
            widthConstraint: {
                maximum: 150   
            }
        }
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
        <div id="detailPage">
            <AuthorDetailForm/>
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
