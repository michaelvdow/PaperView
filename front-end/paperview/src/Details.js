import React from 'react';
import MaterialTable from "material-table";
import Paper from "@material-ui/core/Paper";
import * as selectors from './redux/selectors'
import * as actions from './redux/actions'
import * as Constants from './Constants'
import { connect } from 'react-redux'


class Details extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="Details" style={{ maxWidth: "90%", marginLeft: "5%", marginTop: "30px"}}>
                <Paper>
                    <MaterialTable
                        options={{
                            search: false
                        }}
                        columns={
                            this.props.searchType === Constants.AUTHOR ? 
                            [
                                { title: "Author ID", field: "authorId", type: "numeric", editable: 'never' },
                                { title: "Author Name", field: "name" },
                                { title: "Affiliation", field: "affiliation" },
                                { title: "Cited By", field: "citedBy", type: "numeric" },
                                { title: "Email", field: "email" },
                                { title: "H-Index", field: "hindex", type: "numeric" },
                                { title: "I10-Index", field: "i10index", type: "numeric" }
                            ]:
                            [//ArticleId, PrimaryAuthorId, CitedBy, Citations, Title, Year, Url, Publisher, Journal
                                { title: "Article ID", field: "articleId", type: "numeric", editable: 'never' },
                                { title: "Title", field: "title" },
                                { title: "Primary Author ID", field: "primaryAuthorId", type: "numeric" },
                                { title: "Cited By", field: "citedBy", type: "numeric" },
                                { title: "Citations", field: "citations", type: "numeric" },
                                { title: "Year", field: "year", type: "numeric" },
                                { title: "Publisher", field: "publisher" },
                                { title: "Journal", field: "journal" },
                                { title: "URL", field: "url" }
                            ]
                        }
                        data={[
                            this.props.detailsData
                        ]}
                        title={this.props.searchType === Constants.AUTHOR ? "Author Details" : "Article Details"}
                        editable={{
                            onRowUpdate: (newData, oldData) =>
                              new Promise((resolve, reject) => {
                                setTimeout(() => {
                                    {
                                        this.props.updateRow(newData)
                                    }
                                  resolve()
                                }, 200)
                              })
                          }}
                          actions={[
                            {
                              icon: "arrow_back",
                              tooltip: 'Back',
                              isFreeAction: true,
                              onClick: () => this.props.setPanel(Constants.PANEL_SEARCH)
                            }
                          ]}
                    />
                </Paper>
            </div>  
        );
    }
}

const mapStateToProps = (state) => {
    return {
        searchType: selectors.getSearchType(state),
        detailsData: selectors.getDetailsData(state)
    }
}

const mapDispatchToProps = dispatch => {
    return {
        setPanel: (panel) => dispatch(actions.setPanel(panel)),
        updateRow: (data) => dispatch(actions.updateRow(data))
    }
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
  )(Details)
