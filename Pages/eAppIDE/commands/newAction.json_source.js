include("eAppIDE.mvc.createcommand")
include("eAppIDE.mvc.facade")

include("eAppIDE.eventNames")

NewActionCommand = CreateCommand(null,
    function () {
        var facade = Facade.getInstance();

        var ok = false;
        var newName = QInputDialog.getText(facade.getWindow(),
            qsTr("Input new element name"),
            qsTr("Element name"),
            QLineEdit.Normal,
            "",
            ok);
        if (isBlank(newName)) {
            Logger.error("Resource was not created: File must have non-empty name");
            return;
        }

        // Fetch container new resource was created at
        var projectTree = facade.getMediator(ProjectTreeMediator.name);
        var container_id = projectTree.selectedElementId;
        var parent = facade.getModelElement(container_id);

        var promise = parent.createChild(newName);
        promise.then(
            function(resource) {
                Logger.info("Resource created successfully: \"" + resource.name + "\"");
                projectTree.addResource(resource);
            },
            function(error) {
                Logger.error("Resource was not created: " + error);
            }
        ).then(undefined, function(error) {
            Logger.error("NewActionCommand: " + error);
        });
    },
    "NewAction",
    [
        EVENTS.NEW_RESOURCE,
    ],
    true
);
