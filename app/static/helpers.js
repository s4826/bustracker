const dirs = ["Outbound", "Inbound"]

function addEventListeners() {
    let routeElement = getRouteElement();
    if (routeElement != null)
        routeElement.onchange = () => {selectRoute(routeElement.value)};

    let dirElement = getDirElement();
    if (dirElement != null)
        dirElement.onchange = () => {selectDir(dirElement.value)};
}

function selectRoute(route) {
    if (route != "")
        window.location.assign(window.origin + `/routes/${route}`);
}

function selectDir(dir) {
    let pathElems = window.location.pathname.split("/");
    if (dir != "") {
        if (dirs.includes(pathElems[pathElems.length - 1])) {
            let path = pathElems.slice(1, pathElems.length - 1).join("/")
            window.location.assign(window.origin + `/${path}/${dir}`);
        }
        else
            window.location.assign(window.location + `/${dir}`);
    }
}

function populateSelections() {
    let routeElement = getRouteElement();
    let pathElems = window.location.pathname.split("/");
    if (pathElems.length == 3) {
        routeElement.value = pathElems[pathElems.length - 1];
    } else if (pathElems.length == 4) {
        routeElement.value = pathElems[pathElems.length - 2];
        let dirElement = getDirElement();
        dirElement.value = pathElems[pathElems.length - 1];
    }
}

function getRouteElement() {
    return document.getElementById("route_list");
}

function getDirElement() {
    return document.getElementById("dir_list");
}
