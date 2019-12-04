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
        width: "700px",
        "physics": {
            "barnesHut": {
              "springConstant": 0.1,
              "avoidOverlap": 0.2
            }
          },
        nodes:{
            shape: 'ellipse',
            widthConstraint: {
                maximum: 150   
            }
        },
        edges: {
            width: 1
        },
        "physics": {
            "barnesHut": {
              "springConstant": 0,
              "avoidOverlap": 0.2
            }
          }
    };
  }

  render() {
    return (
        <div id="detailPage">
            <AuthorDetailForm/>

            <div id="graph">
                <Graph graph={this.props.graph} options={this.options} events={this.events} />
            </div>
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
        onSelectNode: (event) => dispatch(actions.onSelectNode(event))
    }
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(NeoGraph)
