include("eAppIDE.mvc.facade")
include("eAppIDE.mvc.createcommand")

include("eAppIDE.views.loginDialog")

function LoginDialogMediator () {
    this.dialog = new LoginDialog();
    this.errorMessage = undefined;
}

// Constructor function name and string MUST be equal!
LoginDialogMediator.prototype.name = "LoginDialogMediator";

LoginDialogMediator.prototype.show = function() {
    var dialog = this.dialog;
    dialog.setErrorMessage(this.errorMessage);
    this.errorMessage = undefined;


    dialog.accepted.connect(null, function() {
        var login = dialog.login;
        var password = dialog.password;

        Facade.getInstance().raiseEvent(EVENTS.LOGIN_READY, {
            login: login,
            password: password
        });
    });

    dialog.show();
}