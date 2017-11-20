include("eAppIDE.mvc.createcommand")
include("eAppIDE.mvc.facade")
include("eAppIDE.eventNames")
include("eAppIDE.model.resourceDefines")

include("eAppIDE.mediators.mainWindow")
include("eAppIDE.mediators.projectTree")
include("eAppIDE.mediators.editorsContainer")
include("eAppIDE.mediators.actionsContainer")
include("eAppIDE.mediators.loggerWindow")
include("eAppIDE.mediators.resourceManager")

StartupCommand = CreateCommand(null,
    function () {
        registerHandlers();
        var mainWindow = registerViews();
        mainWindow.showWindow();

        Facade.getInstance().raiseEvent(EVENTS.LOGIN_START);
    },
    "Startup",
    [ EVENTS.APP_STARTED ],
    true /* register now */
);

function registerHandlers() {
    // work is done through CreateCommand mostly
}

function registerViews() {
    var facade = Facade.getInstance();

    var mainWindow = new MainWindowMediator();
    facade.registerMediator(mainWindow);

    var resourceManager = new ResourceManager(ResIcons);
    facade.setResourceManager(resourceManager);

    var loggerWindowMediator = new LoggerWindowMediator();
    facade.registerMediator(loggerWindowMediator);

    var projectTree = new ProjectTreeMediator();
    facade.registerMediator(projectTree);

    var editorsContainer = new EditorsContainerMediator();
    facade.registerMediator(editorsContainer);

    var actionsContainer = new ActionsContainer();
    facade.registerMediator(actionsContainer);

    mainWindow.init();
    loggerWindowMediator.init(mainWindow);
    actionsContainer.init(mainWindow.window);
    projectTree.init();
    mainWindow.addToDock({
        dockArea: Qt.LeftDockWidgetArea,
        widget: projectTree.widget,
        title: "Project Tree",
        tabify: false
    });
    editorsContainer.init();
    mainWindow.setEditor(editorsContainer.widget);

    return mainWindow;
}
