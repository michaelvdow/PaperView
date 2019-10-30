import * as actions from './actionTypes'

export const onSubmit = () => {
    return {
        type: actions.SUBMIT_SEARCH
    }
}

export const onTextChange = (input) => {
    return {
        type: actions.TEXT_CHANGE,
        input: input
    }
}

export const onSearchTypeChange = (input) => {
    return {
        type: actions.CHANGE_SEARCH_TYPE,
        input: input
    }
}

export const onSearchResult = (input) => {
    return {
        type: actions.ON_SEARCH_RESULT,
        input: input
    }
}

export const onDetailsClick = (id) => {
    return {
        type: actions.ON_DETAILS_CLICK,
        id: id
    }
}

export const onDeleteClick = (id) => {
    return {
        type: actions.ON_DELETE_CLICK,
        id: id
    }
}

export const deleteRow = (index) => {
    return {
        type: actions.DELETE_ROW,
        index: index
    }
}

export const setDetailsData = (data) => {
    return {
        type: actions.SET_DETAILS_DATA,
        data: data
    }
}

export const setPanel = (panel) => {
    return {
        type: actions.SET_PANEL,
        panel: panel
    }
}

export const updateRow = (data) => {
    return {
        type: actions.UPDATE_ROW,
        data: data
    }
}

export const setMainTab = (data) => {
    return {
        type: actions.SET_MAIN_TAB,
        tab: data
    }
}

export const setAuthorPaperTab = (data) => {
    return {
        type: actions.SET_AUTHOR_PAPER_TAB,
        tab: data
    }
}