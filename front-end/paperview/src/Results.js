import React from 'react';
import MaterialTable from "material-table";
import Paper from "@material-ui/core/Paper";
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
            <div className="Results" style={{ maxWidth: "90%", marginLeft: "5%", marginTop: "30px"}}>
                <Paper>
                    <MaterialTable
                        options={{
                            search: false
                        }}
                        columns={
                            this.props.searchType === Constants.ARTICLE ?
                            [
                                { title: "Article ID", field: "ArticleId", type: "numeric", editable: 'never' },
                                { title: "Title", field: "Title" },
                                // { title: "Author Name", field: "authorName" },
                                { title: "Primary Author ID", field: "PrimaryAuthorId", type: "numeric" },
                                { title: "Cited By", field: "CitedBy", type: "numeric" },
                                { title: "Citations", field: "Citations", type: "numeric" },
                                { title: "Year", field: "Year", type: "numeric" },
                                { title: "Publisher", field: "Publisher" },
                                { title: "Journal", field: "Journal" },
                                { title: "URL", field: "Url" }
                            ]:
                            [
                                { title: "Author ID", field: "AuthorId", type: "numeric", editable: 'never' },
                                { title: "Author Name", field: "Name" },
                                { title: "Affiliation", field: "Affiliation" },
                                { title: "Cited By", field: "CitedBy", type: "numeric" },
                                { title: "H-Index", field: "HIndex", type: "numeric" },
                                { title: "I10-Index", field: "I10Index", type: "numeric" },
                            ]
                        }
                        data={
                            this.props.detailsData
                        }
                        title={this.props.searchType === Constants.AUTHOR ? "Author Details" : 
                            (this.props.searchType === Constants.ARTICLE ? "Article Details" : "Expert Details")}
                        actions = {[
                            {
                                icon: 'filter',
                                tooltip: 'Goto detailed page',
                                onClick: (event, rowData) => {
                                    this.props.searchType === Constants.ARTICLE ? 
                                    this.props.onGotoDetailedPage(Constants.ARTICLE, rowData.ArticleId) : 
                                    this.props.onGotoDetailedPage(Constants.AUTHOR, rowData.AuthorId)}
                            }
                        ]}
                        editable={{
                            onRowUpdate: (newData, oldData) =>
                              new Promise((resolve, reject) => {
                                setTimeout(() => {
                                    {
                                        this.props.updateRow(oldData, newData)
                                    }
                                  resolve()
                                }, 200)
                              }),
                              onRowDelete: oldData =>
                                new Promise((resolve, reject) => {
                                setTimeout(() => {
                                    {
                                        this.props.onRowDelete(oldData)
                                    }
                                    resolve()
                                }, 1000)
                                })
                            }}
                            onRowSace
                    />
                </Paper>
            </div>  
        );
    }
}

const mapStateToProps = (state) => {
    return {
        searchType: selectors.getSearchType(state),
        detailsData: selectors.getSearchData(state)
    }
}

const mapDispatchToProps = dispatch => {
    return {
        updateRow: (oldData, newData) => dispatch(actions.updateRow(oldData, newData)),
        onRowDelete: (oldData) => dispatch(actions.onRowDelete(oldData)),
        onGotoDetailedPage: (type, id) => dispatch(actions.onGotoDetailPage(type, id))
    }
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
  )(Results)
