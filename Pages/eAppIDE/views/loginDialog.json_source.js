var LoginDialogForm = vdom.ui.load("ui.loginDialog");

function LoginDialog(parent) {
    this.form_ = LoginDialogForm;
    this.form_.setParent(parent);

    this.form_.modal = true;
    this.form_.password.echoMode = QLineEdit.PasswordEchoOnEdit;
    this.errorMessage = null;
}

Object.defineProperties(LoginDialog.prototype, {
    login: {
        get: function() { return this.form_.login.text; },
        set: function(value) { this.form_.login.text = value; }
    },
    password: {
        get: function() { return this.form_.password.text; },
        set: function(value) { this.form_.password.text = value; }
    },
    isAccepted: {
        get: function() { return this.form_.result() == 1; }
    }
});

LoginDialog.prototype.showSynchronously = function() {
    if (this.errorMessage) {
        this.form_.errorMessage.text = this.errorMessage;
        this.form_.errorMessage.visible = true;
    } else {
        this.form_.errorMessage.visible = false;
    }

    this.form_.exec();
    return this.isAccepted;
}

LoginDialog.prototype.setErrorMessage = function(message) {
    this.errorMessage = message;
}