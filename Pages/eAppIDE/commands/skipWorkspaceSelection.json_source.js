include("eAppIDE.mvc.createcommand")
include("eAppIDE.mvc.facade")
include("eAppIDE.eventNames")

include("eAppIDE.mediators.workspaceSelector")

SkipWorkspaceSelectionCommand = CreateCommand(null,
    function () {
        var facade = Facade.getInstance();
        var selector = facade.removeMediator(WorkspaceSelectorMediator.name);
        selector.cancel();

        Facade.getInstance().raiseEvent(EVENTS.NEED_WORKSPACE_DATA);
    },
    "SkipWorkspaceSelection",
    [ EVENTS.SKIP_WORKSPACE ],
    true /* register now */
);