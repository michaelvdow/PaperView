import * as actionTypes from './actionTypes'
import * as Constants from '../Constants'

const initialState = {
    searchInput: "",
    searchType: Constants.AUTHOR,
    searchData: [],
    panel: Constants.PANEL_SEARCH,
    detailsData: {},
    mainTab: 0,
    authorPaperTab: 0,
    isSnackBarOpen: false,
    snackBarMessage: "",
    insertArticleTitle: "",
    insertArticleAuthorName: "",
    insertArticleURL: "",
    insertArticleCitedBy: 0,
    insertArticleCitations: 0,
    insertArticleYear: 0,
    insertArticelPublisher: "",
    insertAritcleJournal: "",
    insertAuthorName: "",
    insertAuthorEmail: "",
    insertAuthorAffiliation: "",
    insertAuthorCitation: 0,
    insertAuthorH: 0,
    insertAuthorI10: 0,
    insertAuthorInterest: ""
}

function rootReducer(state=initialState, action) {
    switch(action.type) {
        case actionTypes.CHANGE_SEARCH_TYPE:
            return Object.assign({}, state, {searchType: action.input, searchData: []})
        case actionTypes.TEXT_CHANGE:
            return Object.assign({}, state, {searchInput: action.input})
        case actionTypes.ON_SEARCH_RESULT:
            return Object.assign({}, state, {searchData: action.input})
        case actionTypes.DELETE_ROW:
            return Object.assign({}, state, {searchData: [...state.searchData.filter((elem, idx) => idx != action.index)]})
        case actionTypes.SET_MAIN_TAB:
            return Object.assign({}, state, {mainTab: action.tab})
        case actionTypes.SET_AUTHOR_PAPER_TAB:
            return Object.assign({}, state, {authorPaperTab: action.tab})
        case actionTypes.ON_SNACK_BAR_CLOSE:
            if (action.reason === 'clickaway') {
                return state
            } else {
                return Object.assign({}, state, {isSnackBarOpen: false})
            }
        case actionTypes.LAUNCH_SNACK_BAR:
            return Object.assign({}, state, {isSnackBarOpen: true, snackBarMessage: action.message})
        case actionTypes.ON_INSERT_ARTICLE_TITLE:
            return Object.assign({}, state, {insertArticleTitle: action.input})
        case actionTypes.ON_INSERT_ARTICLE_AUTHOR_NAME:
            return Object.assign({}, state, {insertArticleAuthorName: action.input})
        case actionTypes.ON_INSERT_ARTICLE_URL:
            return Object.assign({}, state, {insertArticleURL: action.input})
        case actionTypes.ON_INSERT_ARTICLE_CITED_BY:
            return Object.assign({}, state, {insertArticleCitedBy: action.input})
        case actionTypes.ON_INSERT_ARTICLE_CITATIONS:
            return Object.assign({}, state, {insertArticleCitations: action.input})
        case actionTypes.ON_INSERT_ARTICLE_YEAR:
            return Object.assign({}, state, {insertArticleYear: action.input})
        case actionTypes.ON_INSERT_ARTICLE_PUBLISHER:
            return Object.assign({}, state, {insertArticelPublisher: action.input})
        case actionTypes.ON_INSERT_ARTICLE_JOURNAL:
            return Object.assign({}, state, {insertAritcleJournal: action.input})
        case actionTypes.ON_INSERT_AUTHOR_NAME:
            return Object.assign({}, state, {insertAuthorName: action.input})
        case actionTypes.ON_INSERT_AUTHOR_EMAIL:
            return Object.assign({}, state, {insertAuthorEmail: action.input})
        case actionTypes.ON_INSERT_AUTHOR_AFFILIATION:
            return Object.assign({}, state, {insertAuthorAffiliation: action.input})
        case actionTypes.ON_INSERT_AUTHOR_CITATION:
            return Object.assign({}, state, {insertAuthorCitation: action.input})
        case actionTypes.ON_INSERT_AUTHOR_H:
            return Object.assign({}, state, {insertAuthorH: action.input})
        case actionTypes.ON_INSERT_AUTHOR_I10:
            return Object.assign({}, state, {insertAuthorI10: action.input})
        case actionTypes.ON_INSERT_AUTHOR_INTEREST:
            return Object.assign({}, state, {insertAuthorInterest: action.input})
        default:
            return state
    }
}

export default rootReducer;