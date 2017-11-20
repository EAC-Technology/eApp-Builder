include("signalconnector")

function Controller() {
    this.connectors = {};
}

Controller.prototype.getConnector = function(eventName) {
    var connector = this.connectors[eventName];

    if (!connector) {
        connector = this.connectors[eventName] = new SignalConnector(eventName);
    }

    return connector;
}

Controller.prototype.registerEvent = function(eventName, eventSource) {
    assert(eventName && eventSource, "Empty eventName or eventSource");
    this.getConnector(eventName).registerEvent(eventSource);
}

Controller.prototype.raiseEvent = function() {
    var args = [].slice.call(arguments);
    var eventName = args[0];

    assert(eventName, "Empty event name");
    args.splice(0, 1);

    var connector = this.getConnector(eventName);
    assert(connector, "No registered command for event name \"" + eventName + "\"");
    return connector.handler.apply(connector, args);
}

Controller.prototype.registerCommand = function(eventName, context, command) {
    assert(eventName && command, "Empty eventName or command");
    return this.getConnector(eventName).addCommand(context, command);
}

Controller.prototype.unregisterCommand = function(eventName, context, command) {
    throw "unregisterCommand is not implemented yet";

/*    if (!eventName || !command) {
        var error = "Empty eventName or command";
        print(error);
        throw error;
    }
    return this.getConnector(eventName).removeCommand(context, command);*/
}