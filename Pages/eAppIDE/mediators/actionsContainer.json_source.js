include("eAppIDE.actionNames");

function ActionsContainer () {
    this.actions = {};
    this.Logger = Logger.get("ActionsContainer");
}

// Constructor function name and string MUST be equal!
ActionsContainer.prototype.name = "ActionsContainer";

ActionsContainer.prototype.init = function(window) {
    var facade = Facade.getInstance();
    var window = facade.getWindow();

    function newAction(text, event) {
        var ret = new QAction(text, window);
        if (event) {
            facade.registerEvent(event, ret.triggered);
        }
        return ret;
    }

    this.actions[ACTIONS.Quit] = newAction(qsTr("&Quit"), EVENTS.QUIT_TRIGGERED);
    this.actions[ACTIONS.Quit].icon = facade.getResourceIcon(ACTIONS.Quit);

    this.actions[ACTIONS.Login] = newAction(qsTr("&Login"), EVENTS.LOGIN_START);
    this.actions[ACTIONS.OpenWorkspace] = newAction(qsTr("&Open Workspace"), EVENTS.SELECT_WORKSPACE);

    this.actions[ACTIONS.ReloadWorkspace] = newAction(qsTr("&Reload Workspace"));
    this.actions[ACTIONS.ReloadWorkspace].triggered.connect(this, function() {
        this.Logger.error("Not implemented");
    });

    this.actions[ACTIONS.Save] = newAction(qsTr("&Save"), EVENTS.SAVE_FILE);
    this.actions[ACTIONS.Save].icon = facade.getResourceIcon(ACTIONS.Save);

    this.actions[ACTIONS.SaveAll] = newAction(qsTr("Save &All"), EVENTS.SAVE_ALL_FILES);

    this.actions[ACTIONS.New] = newAction(qsTr("&New"), EVENTS.NEW_RESOURCE);
    this.actions[ACTIONS.Edit] = newAction(qsTr("&Edit"), EVENTS.EDIT_RESOURCE);
    this.actions[ACTIONS.Delete] = newAction(qsTr("&Delete"), EVENTS.DELETE_RESOURCE);
}

ActionsContainer.prototype.getMenuActions = function() {
    var ret = {};
    ret["&Main"] = [
        this.actions[ACTIONS.OpenWorkspace],
        this.actions[ACTIONS.ReloadWorkspace],
        this.actions[ACTIONS.Quit],
    ];
    ret["&File"] = [
        this.actions[ACTIONS.Save],
        this.actions[ACTIONS.SaveAll],
    ];
    return ret;
}

ActionsContainer.prototype.getToolbars = function() {
    var ret = {};
    ret["General"] = [
        this.actions[ACTIONS.Quit]
    ];
    ret["Workspace"] = [
        this.actions[ACTIONS.Login],
        this.actions[ACTIONS.OpenWorkspace],
        this.actions[ACTIONS.ReloadWorkspace],
    ];
    ret["File"] = [
        this.actions[ACTIONS.Save],
        this.actions[ACTIONS.SaveAll],
    ];
    return ret;
}

ActionsContainer.prototype.get = function(actionName) {
    assert(ACTIONS.hasOwnProperty(actionName), "Action \"" + actionName + "\" is not listed in ACTIONS");
    assert(this.actions.hasOwnProperty(actionName), "Action \"" + actionName + "\" is not listed in ActionsContainer");

    return this.actions[actionName];
}
