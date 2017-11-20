include("facade")

function CreateCommand(context, callback, name, eventList, doRegister) {
    callback.cbname = name;
    callback.events = eventList;

    if (doRegister) {
        callback.events.forEach(function(eventName) {
            Facade.getInstance().registerCommand(eventName, context, callback);
        });
    }

    return callback;
}