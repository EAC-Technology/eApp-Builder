include("eAppIDE.mvc.createcommand")
include("eAppIDE.mvc.facade")

include("eAppIDE.eventNames")

DeleteActionCommand = CreateCommand(null,
    function () {
        var facade = Facade.getInstance();

        var elem_id = facade.getMediator(ProjectTreeMediator.name).selectedElementId;
        var element = facade.getModelElement(elem_id);

        var promise = Promise.resolve().then(
            function() {
                var reply = QMessageBox.question(facade.getWindow(),
                        "Delete element",
                        "Do you want to delete element '" + element.name + "'" +
                        "of type '" + element.type + "'?\n" +
                        "This action cannot be undone",
                        QMessageBox.StandardButtons(
                            QMessageBox.Yes,
                            QMessageBox.No));
                if (reply == QMessageBox.Yes) {
                    return element.deleteSelf();
                } else if (reply == QMessageBox.No) {
                    throw new Error("User cancelled the deletion");
                }
                throw new Error(
                    "QMessageBox.question reply was neither of OK or Cancel");
        }).then(
            function(element) {
                Logger.info("element removed successfully: \"" + element.name + "\"");

                var projectTree = facade.getMediator(ProjectTreeMediator.name);
                projectTree.removeElement(element.id);

                var editorsContainer = facade.getMediator(EditorsContainerMediator.name);
                if (editorsContainer.isOpen(element.id)) {
                    editorsContainer.closeEditor(element.id);
                }
                return true;
            },
            function(error) {
                Logger.error("element was not removed: " + error);
            }
        ).then(undefined, function(error) {
            Logger.error("DeleteActionCommand: " + error);
        });
    },
    "DeleteAction",
    [
        EVENTS.DELETE_RESOURCE,
    ],
    true
);
