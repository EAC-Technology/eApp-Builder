include("eAppIDE.mvc.createcommand")
include("eAppIDE.mvc.facade")

include("eAppIDE.eventNames")

include("eAppIDE.mediators.workspaceSelector")

SelectWorkspaceCommand = CreateCommand(null,
    function () {
        var facade = Facade.getInstance();
        var model = facade.getModel();

        var promise = model.listWorkspaces().then(function(root_id) {
            var root = facade.getModelElement(root_id);

            var workspaces = root.children.map(
                function(wp_id) {
                    return facade.getModelElement(wp_id);
                });

            var workspaceSelector = new WorkspaceSelector();

            if (!workspaceSelector.selectWorkspace(workspaces)) {
                throw "User had not selected workspace";
            }
            return workspaceSelector.selectedWorkspace.id;
        }).then(
            function(workspace_id) {
                facade.raiseEvent(EVENTS.WORKSPACE_DATA_READY, workspace_id);
            },
            function(error) {
                Logger.error("Can't get workspace data: " + error);
            }
        ).then(undefined, function(error) {
            Logger.error("SelectWorkspaceCommand: " + error);
        });
    },
    "SelectWorkspace",
    [
        EVENTS.SELECT_WORKSPACE,
    ],
    true
);
