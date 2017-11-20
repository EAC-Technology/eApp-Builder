include("controller")
include("view")

function Facade() {
    this.controller = new Controller();
    this.view = new View();
    this._cache = {};
}

Facade.getInstance = function() {
    if (!Facade.instance) {
        Facade.instance = new Facade();
    }
    return Facade.instance;
}

// MODEL

Facade.prototype.registerModel = function(model) {
    this._model = model;
}

Facade.prototype.getModel = function() {
    return this._model;
}

Facade.prototype.getModelElement = function(res_id) {
    return this._cache[res_id];
}

Facade.prototype.saveModelElement = function(resource) {
    return this._cache[resource.id] = resource;
}

Facade.prototype.saveModelElements = function(elements) {
    for (var id in elements) {
        this._cache[id] = elements[id];
    }
}

Facade.prototype.removeModelElement = function(res_id) {
    delete this._cache[res_id];
}

// CONTROLLER

Facade.prototype.registerEvent = function(eventName, eventSource) {
    this.controller.registerEvent(eventName, eventSource);
}

Facade.prototype.registerCommand = function(eventName, context, command) {
    return this.controller.registerCommand(eventName, context, command);
}

Facade.prototype.unregisterCommand = function(eventName, context, command) {
    return this.controller.unregisterCommand(eventName, context, command);
}

Facade.prototype.raiseEvent = function() {
    return this.controller.raiseEvent.apply(this.controller, [].slice.apply(arguments));
}

// VIEW

Facade.prototype.registerMediator = function(mediator) {
    return this.view.registerMediator(mediator);
}

Facade.prototype.getMediator = function(mediatorName) {
    return this.view.getMediator(mediatorName);
}

Facade.prototype.removeMediator = function(mediatorName) {
    return this.view.removeMediator(mediatorName);
}


// Window, for child/parent purposes
Facade.prototype.setWindow = function(value) {
    this._window = value;
}

Facade.prototype.getWindow = function() {
    return this._window;
}

// ResourceManager

Facade.prototype.setResourceManager = function(manager) {
    this._resourceManager = manager;
}

Facade.prototype.getResourceManager = function() {
    return this._resourceManager;
}

Facade.prototype.getResourceIcon = function(type) {
    return this._resourceManager.getIcon(type);
}
