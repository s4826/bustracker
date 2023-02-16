const dirs = ['outbound', 'inbound']

function addEventListeners() {
    let routeElement = getRouteElement();
    if (routeElement != null)
        routeElement.onchange = () => {selectRoute(routeElement.value)};

    let dirElement = getDirElement();
    if (dirElement != null)
        dirElement.onchange = () => {selectDir(dirElement.value)};

    let stopElement = getStopElement();
    if (stopElement != null)
        stopElement.onchange = () => {selectStop(stopElement.value)};
}

function selectRoute(route) {
    if (route != '')
        window.location.assign(buildPath(route));
}

function selectDir(dir) {
    let pathElems = window.location.pathname.split('/');
    if (dir != '') {
        let routeIdx = pathElems.indexOf('routes') + 1;
        window.location.assign(buildPath(pathElems[routeIdx], dir));
    }
}

function selectStop(stop) {
    let route = getRouteElement().value;
    let direction = getDirElement().value;
    if (stop != '') {
        window.location.assign(buildPath(route, direction, stop))
    }
}

function populateSelections() {
    let pathElems = window.location.pathname.split('/');

    let startIdx = pathElems.indexOf('routes');
    let fieldCandidates = [null, null, null];

    if (startIdx++ != -1) {
        let fieldIdx = 0;
        while (fieldIdx < fieldCandidates.length && startIdx < pathElems.length) {
            fieldCandidates[fieldIdx] = pathElems[startIdx];
            fieldIdx++;
            startIdx++;
        }
    }

    if (fieldCandidates[0] != null) {
        getRouteElement().value = fieldCandidates[0];
        if (fieldCandidates[1] != null) {
            getDirElement().value = fieldCandidates[1];
            if (fieldCandidates[2] != null)
                getStopElement().value = fieldCandidates[2];
        }
    }
}


function getRouteElement() {
    return document.getElementById('route_list');
}

function getDirElement() {
    return document.getElementById('dir_list');
}

function getStopElement() {
    return document.getElementById('stop_list');
}

function buildPath(route = -1, direction = '', stop = -1) {
    let path = '';
    if (route == -1)
        return window.origin;
    else if (direction == '')
        return window.origin + `/routes/${route}`;
    else if (stop == -1)
        path = [route, direction].join('/');
    else
        path = [route, direction, stop].join('/');
    return window.origin + `/routes/${path}`;
} 

function delete_flash(flash) {
    $(flash).parent().remove()
}
