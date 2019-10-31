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
    snackBarMessage: ""
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
        default:
            return state
    }
}

export default rootReducer;