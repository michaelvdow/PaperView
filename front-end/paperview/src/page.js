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
    this.graph = {
        nodes: [
            { id: "1", label: "Node 1", color: "#e04141" , authorID: 1},
            { id: 2, label: "Node 2", color: "#e09c41" , authorID: 1},
            { id: 3, label: "Node 3", color: "#e0df41" },
            { id: 4, label: "Node 4", color: "#7be041" },
            { id: 5, label: "Node 5", color: "#41e0c9" }
        ],
        edges: [{ from: "1", to: 2 , isCitation: true, color:"#e09c41" }, { from: "1", to: 3 }, { from: 2, to: 4 }, { from: 2, to: 5 }]
    };
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
        <Graph graph={this.graph} options={this.options} events={this.events} />
        
    ); 
  }
}


const mapStateToProps = (state) => {
    return {
        tab: selectors.getMainTab(state)
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
