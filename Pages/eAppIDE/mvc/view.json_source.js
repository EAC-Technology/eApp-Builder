function View() {
    this.mediators = {};
}

View.prototype.registerMediator = function(mediator) {
    if (this.mediators[mediator.name]) {
        return false;
    }
    this.mediators[mediator.name] = mediator;
}

View.prototype.getMediator = function(mediatorName) {
    return this.mediators[mediatorName];
}

View.prototype.removeMediator = function(mediatorName) {
    var ret = this.mediators[mediatorName];
    delete this.mediators[mediatorName];

    return ret;
}