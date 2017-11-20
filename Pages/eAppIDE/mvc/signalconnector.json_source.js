function SignalConnector(eventName) {
    this.commands = [];
    this.eventName = eventName;
}

SignalConnector.prototype.handler = function() {
    var data = {
        eventName: this.eventName,
        args: [].slice.call(arguments)
    };

    this.commands.forEach(function(cmd) {
        var name = (cmd.obj && "name" in cmd.obj) ? cmd.obj.name :
                        ("cbname" in cmd.func) ? cmd.func.cbname : cmd.func.name;
        Logger.get("Controller").debug("Invoke event \"" + data.eventName + "\" on \"" + name + "\"");

        cmd.func.apply(cmd.obj, [data]);
    });
}

SignalConnector.prototype.registerEvent = function(eventSource) {
    eventSource.connect(this, this.handler);
}

SignalConnector.prototype.commandIndex = function(context, func) {
    var i = this.commands.length - 1;
    for (; i >= 0; i--) {
        if (this.commands[i].obj === context && this.commands[i].func === func) {
            break;
        }
    }

    return i;
}

SignalConnector.prototype.addCommand = function(context, func) {
    if (this.commandIndex(context, func) != -1) {
        return false;
    }
    this.commands.push({
        obj: context,
        func: func
    });
    return true;
}

SignalConnector.prototype.removeCommand = function(context, func) {
    var index = this.commandIndex(context, func);

    if (index == -1) {
        return false;
    }
    this.commands.splice(index, 1);
    return true;
}