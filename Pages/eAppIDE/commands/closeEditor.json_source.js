include("eAppIDE.mvc.createcommand")
include("eAppIDE.mvc.facade")
include("eAppIDE.eventNames")

include("eAppIDE.commands.saveAction");
include("eAppIDE.mediators.editorsContainer")

CloseEditorCommand = CreateCommand(null,
    function (data) {
        var eventName = data.eventName;
        var res_id = data.args[0];
        assert(res_id, "CloseEditorCommand: Empty resource ID");

        var facade = Facade.getInstance();
        var editorsContainer = facade.getMediator(EditorsContainerMediator.name);

        var STEPS = {
            proceed: "proceed",
            cancel: "cancel",
        };

        var promise = new Promise(function(resolve, reject) {
            if (!editorsContainer.hasUnsavedChanges(res_id)) {
                resolve(STEPS.proceed);
            } else {
                var resource = facade.getModelElement(res_id);

                var reply = QMessageBox.question(facade.getWindow(),
                    "Save before closing",
                    "\"" + resource.name + "\" has been modified.\n" +
                    "Do you want to save it?",
                    QMessageBox.StandardButtons(
                        QMessageBox.Save,
                        QMessageBox.Discard,
                        QMessageBox.Cancel));

                if (reply == QMessageBox.Save) {
                    SaveActionCommand({eventName: EVENTS.SAVE_FILE, args:[res_id]}).then(
                        function() {
                            resolve(STEPS.proceed);
                        }
                    ).then(undefined,
                        function(error) {
                            reject(error);
                    });

                } else if (reply == QMessageBox.Discard) {
                    resolve(STEPS.proceed);

                } else if (reply == QMessageBox.Cancel) {
                    resolve(STEPS.cansel);
                }
            }
        }).then(function(nextStep) {
            if (nextStep == STEPS.proceed) {
                editorsContainer.closeEditor(res_id);
                return true;
            } else {
                return false;
            }
        }).then(undefined, function(error) {
                Logger.error("Editor had not been closed: " + error);
        });
        return promise;
    },
    "CloseEditor",
    [ EVENTS.CLOSE_EDITOR ],
    true /* register now */
);
