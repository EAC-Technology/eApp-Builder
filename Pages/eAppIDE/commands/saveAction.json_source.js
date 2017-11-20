include("eAppIDE.mvc.createcommand")
include("eAppIDE.mvc.facade")

include("eAppIDE.eventNames")

SaveActionCommand = CreateCommand(null,
    function (data) {
        var eventName = data.eventName;
        var res_id = data.args[0];

        var facade = Facade.getInstance();
        var editorsContainer = facade.getMediator(EditorsContainerMediator.name);

        if (!res_id) {
            res_id = editorsContainer.getCurrentResourceId();
        }
        assert(res_id, "No Resource ready for saving");

        var content = editorsContainer.getResourceContent(res_id);
        var resource = facade.getModelElement(res_id);

        var promise = resource.saveContent(content);
        return promise.then(
            function(res) {
                Logger.info("Resource saved successfully: \"" + res_id + "\"");
                editorsContainer.setHasUnsavedChanges(res_id, false);
                facade.raiseEvent(EVENTS.SAVE_RESOURCE_DATA_SUCCESS, res_id);
                return res_id;
            }
        ).then(undefined,
            function(error) {
                Logger.error("Resource had not been saved: " + error);
                return null;
            }
        );
    },
    "SaveAction",
    [
        EVENTS.SAVE_FILE,
//        EVENTS.SAVE_ALL_FILES,
    ],
    true
);
