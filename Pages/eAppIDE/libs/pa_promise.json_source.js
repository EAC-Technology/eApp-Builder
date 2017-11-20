var POLYFILL_TIMERS = [];

function createTimer(callback, timeout, singleShot) {
    var timer = new QTimer();
    timer.interval = timeout;
    timer.singleShot = singleShot;
    timer.timeout.connect(null, callback);
    timer.start();
    POLYFILL_TIMERS.push(timer);
    return POLYFILL_TIMERS.length-1;
}


function setTimeout(callback, time_ms) {
    return createTimer(callback, time_ms, true);
}

function setInterval(callback, delay) {
    return createTimer(callback, delay, false);
}
