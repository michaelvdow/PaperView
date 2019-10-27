import { call, put, all, select, takeLatest } from 'redux-saga/effects'
import * as actionTypes from './actionTypes'
import * as selectors from './selectors'
import * as actions from './actions'
import * as Constants from '../Constants'

function *submit() {
    let searchType = yield select(selectors.getSearchType)
    let searchInput = yield select(selectors.getSearchInput)

    // const response = call(fetch, `localhost:something/search/${searchType}?input=${searchInput}`)
    // const responseBody = response.json()
    // Test data:
    const responseBody = [{authorId: 10, name: "Michael Dow"}, {authorId: 12, name: "Dow"}]
    yield put(actions.onSearchResult(responseBody))
}

function *deleteRow(action) {
    let options = {
        method: 'DELETE'
    }
    let url = "URL"
    // const response = yield call(fetch, url, options)
    // if (response.json().status == 200) {
        var data = yield select(selectors.getSearchData)
        console.log(data)
        var searchType = yield select(selectors.getSearchType)
        let index = data.findIndex((elem) => (searchType === Constants.AUTHOR ? elem.authorId : elem.articleId) === action.id)
        yield put(actions.deleteRow(index))
    // }
}

function *onDetailsClick(id) {
    // let options = {
    //     method: 'GET'
    // }
    // let url = "URL"
    // const response = yield call(fetch, url, options)
    const responseBody = {authorId: 10, name: "Michael Dow", affiliation: "UIUC", citedBy: 102, email: "mvdow2", hindex: 3, i10index: 12}
    yield put(actions.setDetailsData(responseBody))
}

function *updateRow(action) {
    // let options = {
    //     method: 'POST'
    // }
    // let url = "URL"
    // const response = yield call(fetch, url, options)
    yield put(actions.setDetailsData(action.data))
}

function *watchUpdateRow() {
    yield takeLatest(actionTypes.UPDATE_ROW, updateRow);
}

function *watchDelete() {
    yield takeLatest(actionTypes.ON_DELETE_CLICK, deleteRow);
}

function *watchDetails() {
    yield takeLatest(actionTypes.ON_DETAILS_CLICK, onDetailsClick);
}

function *watchSubmit() {
    yield takeLatest(actionTypes.SUBMIT_SEARCH, submit);
}

function* rootSaga () {
    yield all([
        watchSubmit(),
        watchDetails(),
        watchDelete(),
        watchUpdateRow()
    ])
}

export default rootSaga;