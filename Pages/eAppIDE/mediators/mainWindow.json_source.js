include("eAppIDE.mvc.facade")
include("eAppIDE.mvc.createcommand")

include("eAppIDE.views.mainWindow")
include("eAppIDE.mediators.actionsContainer")

function MainWindowMediator () {
    this.window = new MainWindow();
    this.Logger = Logger.get("MainWindow");
    this.editorDockMapping = {};
    this.currentWindowContext = null;
}

// Constructor function name and string MUST be equal!
MainWindowMediator.prototype.name = "MainWindowMediator";

MainWindowMediator.prototype.init = function() {
    Facade.getInstance().setWindow(this.window.form);
    Facade.getInstance().registerCommand(
        EVENTS.WINDOW_CONTEXT_CHANGED,
        this,
        this.onWindowContextChangedHandler);
}

MainWindowMediator.prototype.showWindow = function() {
    var actionsContainer = Facade.getInstance().getMediator(ActionsContainer.name);

    var menus = actionsContainer.getMenuActions();
    for (var menu in menus) {
        if (menus.hasOwnProperty(menu)) {
            this.window.setMenuActions(menu, menus[menu]);
        }
    }
    var toolbars = actionsContainer.getToolbars();
    for (var toolbar in toolbars) {
        if (toolbars.hasOwnProperty(toolbar)) {
            this.window.setToolbarActions(toolbar, toolbars[toolbar]);
        }
    }
    this.window.show();
}

MainWindowMediator.prototype.getForm = function() {
    return this.window.form;
}

MainWindowMediator.prototype.setEditor = function(widget) {
    this.window.setEditor(widget);
}

MainWindowMediator.prototype.addToDock = function(args) {
    this.Logger.debug("addWidgetToDock: \"" + args.title + "\" at \"" + args.dockArea + "\"");
    var result = this.window.addWidgetToDock(
        args.dockArea,
        args.widget,
        args.title,
        args.tabify);
    if (result) {
        if (!args.editorTypes) {
            args.editorTypes = [RESOURCE_EDITORS.NoEditor];
        } else {
            result.hide();
        }

        var dockMapping = this.editorDockMapping;
        args.editorTypes.forEach(function(type) {
            if (!(type in dockMapping)) {
                dockMapping[type] = [];
            }

            dockMapping[type].push(result);
        });
    }
}

MainWindowMediator.prototype.onWindowContextChangedHandler = function(data) {
    var eventName = data.eventName;
    var newContext = data.args[0];

    this.onWindowContextChanged(newContext);
}

MainWindowMediator.prototype.onWindowContextChanged = function(newContext) {
    if (this.currentWindowContext == newContext) {
        return;
    }

    if (this.currentWindowContext != RESOURCE_EDITORS.NoEditor) {
        // Hide current context docks
        var toHide = this.editorDockMapping[this.currentWindowContext] || [];
        toHide.forEach(function(w) {
            w.hide();
        });
    }
    if (newContext != RESOURCE_EDITORS.NoEditor) {
        var toShow = this.editorDockMapping[newContext] || [];
        toShow.forEach(function(w) {
            w.show();
        });
    }
    this.currentWindowContext = newContext;
}
