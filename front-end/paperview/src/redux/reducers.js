import * as actionTypes from './actionTypes'
import * as Constants from '../Constants'

const initialState = {
    searchInput: "",
    searchType: Constants.AUTHOR,
    searchData: [],
    panel: Constants.PANEL_SEARCH,
    detailsData: {},
    mainTab: 0,
    authorPaperTab: 0
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
        case actionTypes.SET_DETAILS_DATA:
            return Object.assign({}, state, {detailsData: action.data, panel: Constants.PANEL_DETAILS})
        case actionTypes.SET_PANEL:
            return Object.assign({}, state, {panel: action.panel})
        case actionTypes.SET_MAIN_TAB:
            return Object.assign({}, state, {mainTab: action.tab})
        case actionTypes.SET_AUTHOR_PAPER_TAB:
            return Object.assign({}, state, {authorPaperTab: action.tab})
        default:
            return state
    }
}

export default rootReducer;