include("eAppIDE.views.loggerWindow")

function LoggerWindowMediator(window) {
    this.loggerWindow = undefined;
}

LoggerWindowMediator.name = "LoggerWindowMediator";

LoggerWindowMediator.prototype.init = function(window) {
    this.loggerWindow = new LoggerWindow(window.getForm());

    var loggerWindow = this.loggerWindow;
    function logHandler(messages, context) {
        var name = context.name ? context.name.substring(0, 13) + ":\t" : "\t";
        var message = "";
        for (var i=0; i < messages.length; i++) {
            message = context.level.name + "\t" + name + messages[i];
            print(message);
            loggerWindow.appendMessage(message);
        }
        window.getForm().statusBar().showMessage(message, 5000);
    }
    Logger.setHandler(logHandler);

    window.addToDock({
        widget: this.loggerWindow,
        title: "Log",
        dockArea: Qt.BottomDockWidgetArea,
        tabify: true
    });
}
