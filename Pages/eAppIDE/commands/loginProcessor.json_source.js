include("eAppIDE.mvc.createcommand")
include("eAppIDE.mvc.facade")
include("eAppIDE.eventNames")

include("eAppIDE.views.loginDialog")

LoginProcessorCommand = CreateCommand(null,
    function (data) {
        var eventName = data.eventName;
        var errMsg = data.args[0];
        var facade = Facade.getInstance();

        if (eventName == EVENTS.LOGIN_SUCCESS) {
            facade.raiseEvent(EVENTS.SELECT_WORKSPACE);
            return;
        }

        var dialog = new LoginDialog();

        if (errMsg) {
            dialog.setErrorMessage("Login unsuccessful: \n" + errMsg);
        }

//        if (dialog.showSynchronously()) {
//            var promise = facade.getModel().login(dialog.login, dialog.password);
            var promise = facade.getModel().login("root", "root");
            promise.then(
                function() {
                    // Just to make sure we are notifying the app about success.
                    facade.raiseEvent(EVENTS.LOGIN_SUCCESS);
                },
                function(error) {
                    // Run this again, recursively.
                    facade.raiseEvent(EVENTS.LOGIN_ERROR, error);
                }
            ).then(undefined, function(error) {
                Logger.error("LoginProcessorCommand: " + error);
            });
//        }
    },
    "LoginProcessor",
    [
        EVENTS.LOGIN_START,
        EVENTS.LOGIN_SUCCESS,
        EVENTS.LOGIN_ERROR,
    ],
    true /* register now */
);
