import { call, put, all, select, takeLatest } from 'redux-saga/effects'
import * as actionTypes from './actionTypes'
import * as selectors from './selectors'
import * as actions from './actions'
import * as Constants from '../Constants'

function *submit() {
    let searchType = yield select(selectors.getSearchType)
    let searchInput = yield select(selectors.getSearchInput)

    console.log(searchInput)

    try {
        const searchField = (searchType === Constants.AUTHOR ? "name" : "title")
        const response = yield call(fetch, `${Constants.URL}/search/${searchType}?${searchField}="${searchInput}"`)
        const responseBody = response.json()
        if (responseBody.result === Constants.SUCCESS) {
            if (searchType === Constants.ARTICLE) {
                const articles = responseBody.Articles
                // Get the author name for each article
                for (var i = 0; i < articles.length; i++) {
                    const authorResponse = yield call(fetch, `${Constants.URL}/${searchType}/${articles[i].PrimaryAuthorId}"`)
                    articles[i]["authorName"] = authorResponse.Name;
                }
                yield put(actions.onSearchResult(articles))
            } else {
                yield put(actions.onSearchResult(responseBody.Authors))
            }
        } else {
            yield put(actions.launchSnackBar("Failed to find any results"))
        }
    } catch(e) {
        yield put(actions.launchSnackBar("Could not connect to server"))
    }
}

function *updateRow(action) {
    let data = yield select(selectors.getSearchData)
    let searchType = yield select(selectors.getSearchType)
    const dataIndex = data.findIndex(elem => (searchType === Constants.AUTHOR ? elem.authorId === action.oldData.authorId
        : elem.articleId === action.oldData.articleId))
    let options = {
        method: 'POST',
        body: JSON.stringify(action.newData)
    }
    const id = (searchType === Constants.AUTHOR ? action.oldData.authorId : action.oldData.articleId)
    try {
        const response = yield call(fetch, `${Constants.URL}/${searchType}/${id}`, options)
        const responseBody = response.json()
        if (responseBody.result === Constants.SUCCESS) {
            let newTableData = data.map((item, index) => {
                if (index !== dataIndex) {
                  return item
                }
            
                return {
                  ...item,
                  ...action.newData
                }
            })
            yield put(actions.onSearchResult(newTableData))
        } else {
            yield put(actions.launchSnackBar("Failed to update row"))
        }
    } catch (e) {
        console.log("Update API call failed")
        yield put(actions.launchSnackBar("Could not connect to server"))
    }
}

function *deleteRow(action) {
    let data = yield select(selectors.getSearchData)
    let searchType = yield select(selectors.getSearchType)
    const dataIndex = data.findIndex(elem => (searchType === Constants.AUTHOR ? elem.authorId === action.oldData.authorId
        : elem.articleId === action.oldData.articleId))
   
    let options = {
        method: 'DELETE'
    }
    const id = (searchType === Constants.AUTHOR ? action.oldData.authorId : action.oldData.articleId)
    try {
        const response = yield call(fetch, `${Constants.URL}/${searchType}/${id}`, options)
        const responseBody = response.json()
        if (responseBody.result === Constants.SUCCESS) {
            yield put(actions.onSearchResult(data.filter((elem, index) => index !== dataIndex)))
        } else {
            yield put(actions.launchSnackBar("Failed to delete row"))
        }
    } catch (e) {
        console.log("Delete api call failed")
        yield put(actions.launchSnackBar("Could not connect to server"))
    }
}

function *insert(action) {
    let insertType = yield select(selectors.getAuthorPaperTab)
    console.log("insert type: " + (insertType == 0 ? "article":"author"))
    if (insertType == 0) {
        // article
        let insertArticleTitle = yield select(selectors.getArticleTitle)
        let insertArticleAuthorName = yield select(selectors.getArticleAuthorName)
        let insertArticleURL = yield select(selectors.getArticleURL)
        let insertArticleCitedBy = yield select(selectors.getArticleCitedBy)
        let insertArticleCitations = yield select(selectors.getArticleCitations)
        let insertArticleYear = yield select(selectors.getArticleYear)
        let insertArticlePublisher = yield select(selectors.getArticelPublisher)
        let insertArticleJournal = yield select(selectors.getAritcleJournal)
        console.log("article title: " + insertArticleTitle)
        console.log("article author name: " + insertArticleAuthorName)
        console.log("article URL: " + insertArticleURL)
        console.log("article cited by: " + insertArticleCitedBy)
        console.log("article citations: " + insertArticleCitations)
        console.log("article year: " + insertArticleYear)
        console.log("article publisher: " + insertArticlePublisher)
        console.log("article journal: " + insertArticleJournal)
    }
    else {
        // author
    }
}

function *watchUpdateRow() {
    yield takeLatest(actionTypes.UPDATE_ROW, updateRow);
}

function *watchDelete() {
    yield takeLatest(actionTypes.ON_DELETE_CLICK, deleteRow);
}

function *watchSubmit() {
    yield takeLatest(actionTypes.SUBMIT_SEARCH, submit);
}

function *watchDeleteRow() {
    yield takeLatest(actionTypes.ON_ROW_DELETE, deleteRow);
}

function *watchInsert() {
    yield takeLatest(actionTypes.ON_INSERT_SUBMIT, insert);
}

function* rootSaga () {
    yield all([
        watchSubmit(),
        watchDelete(),
        watchUpdateRow(),
        watchDeleteRow(),
        watchInsert()
    ])
}

export default rootSaga;