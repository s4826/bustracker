function timer() {
    let arrivalElems = document.getElementsByClassName("arrival-time");
    let arrivalTimes = Array.from(arrivalElems).map(x => x.getAttribute("data-time") - 1);
    for (i = 0; i < arrivalElems.length; i++) {
        if (arrivalTimes[i] < 0)
            arrivalElems[i].parentNode.removeChild(arrivalElems[i])
        else {
            arrivalElems[i].innerHTML = mapToClockTime(arrivalTimes[i]);
            arrivalElems[i].setAttribute("data-time", arrivalTimes[i]);
        }
    }

    setTimeout(timer, 1000);
}

function mapToClockTime(time) {
    h = Math.floor(time / 3600);
    m = Math.floor((time - h*3600) / 60);
    s = time - h*3600 - m*60;

    let t = [];
    if (h)
        t = [h, m, s];
    else if (m)
        t = [m, s];
    else
        t = [s];

    return t.map(x => ("00" + x).slice(-2)).join(":");
}
