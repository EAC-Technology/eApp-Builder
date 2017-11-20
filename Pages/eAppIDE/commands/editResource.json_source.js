include("eAppIDE.mvc.createcommand")
include("eAppIDE.mvc.facade")
include("eAppIDE.eventNames")

EditResourceCommand = CreateCommand(null,
    function () {
        var facade = Facade.getInstance();

        var elem_id = facade.getMediator(ProjectTreeMediator.name).selectedElementId;
        var resource = facade.getModelElement(elem_id);
        assert(resource, "Command: EditResource for empty resource");

        if (!resource.isEditable()) {
            Logger.warn("Command: EditResource for NOT editable resource \"" + resource.name + "\" " +
                "of type '" + resource.type + "'");
            return;
        }

        var editorsContainer = facade.getMediator(EditorsContainerMediator.name);
        if (editorsContainer.isOpen(elem_id)) {
            Logger.info("Command: EditResource found existing editor for resource \"" + resource.name + "\"");
            editorsContainer.activateEditor(elem_id);
            return;
        }

        Logger.info("EditResource: fetching editable resource \"" + resource.name + "\"");
        var promise = resource.readContent();
        promise.then(
            function(resource) {
                editorsContainer.showEditor(resource);
            },
            function(error) {
                Logger.error("Can't get content for resource \"" + resource.name + "\": " + error);
            }
        ).then(undefined, function(error) {
            Logger.error("EditResourceCommand: " + error);
        });
    },
    "EditResource",
    [ EVENTS.EDIT_RESOURCE ],
    true /* register now */
);
