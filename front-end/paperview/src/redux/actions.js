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

export const updateRow = (oldData, newData) => {
    return {
        type: actions.UPDATE_ROW,
        oldData: oldData,
        newData: newData
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

export const onRowDelete = (data) => {
    return {
        type: actions.ON_ROW_DELETE,
        oldData: data
    }
}

export const onSnackBarClose = (reason) => {
    return {
        type: actions.ON_SNACK_BAR_CLOSE,
        reason: reason
    }
}

export const launchSnackBar = (message) => {
    return {
        type: actions.LAUNCH_SNACK_BAR,
        message: message
    }
}