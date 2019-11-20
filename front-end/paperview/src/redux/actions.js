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

export const onInsertArticleTitleChange = (input) => {
    return {
        type: actions.ON_INSERT_ARTICLE_TITLE,
        input: input
    }
}

export const onInsertArticleAuthorNameChange = (input) => {
    return {
        type: actions.ON_INSERT_ARTICLE_AUTHOR_NAME,
        input: input
    }
}

export const onInsertArticleURLChange = (input) => {
    return {
        type: actions.ON_INSERT_ARTICLE_URL,
        input: input
    }
}

export const onInsertArticleCitedByChange = (input) => {
    return {
        type: actions.ON_INSERT_ARTICLE_CITED_BY,
        input: input
    }
}

export const onInsertArticleCitationsChange = (input) => {
    return {
        type: actions.ON_INSERT_ARTICLE_CITATIONS,
        input: input
    }
}

export const onInsertArticleYearChange = (input) => {
    return {
        type: actions.ON_INSERT_ARTICLE_YEAR,
        input: input
    }
}

export const onInsertArticlePublisherChange = (input) => {
    return {
        type: actions.ON_INSERT_ARTICLE_PUBLISHER,
        input: input
    }
}

export const onInsertArticleJournalChange = (input) => {
    return {
        type: actions.ON_INSERT_ARTICLE_JOURNAL,
        input: input
    }
}

export const onInsertAuthorNameChange = (input) => {
    return {
        type: actions.ON_INSERT_AUTHOR_NAME,
        input: input
    }
}

export const onInsertAuthorEmailChange = (input) => {
    return {
        type: actions.ON_INSERT_AUTHOR_EMAIL,
        input: input
    }
}

export const onInsertAuthorAffilicationChange = (input) => {
    return {
        type: actions.ON_INSERT_AUTHOR_AFFILIATION,
        input: input
    }
}

export const onInsertAuthorCitationChange = (input) => {
    return {
        type: actions.ON_INSERT_AUTHOR_CITATION,
        input: input
    }
}

export const onInsertAuthorHChange = (input) => {
    return {
        type: actions.ON_INSERT_AUTHOR_H,
        input: input
    }
}

export const onInsertAuthorI10Change = (input) => {
    return {
        type: actions.ON_INSERT_AUTHOR_I10,
        input: input
    }
}

export const onInsertAuthorInterestChange = (input) => {
    return {
        type: actions.ON_INSERT_AUTHOR_INTEREST,
        input: input
    }
}

export const onInsertSubmit = (input) => {
    return {
        type: actions.ON_INSERT_SUBMIT
    }
}
