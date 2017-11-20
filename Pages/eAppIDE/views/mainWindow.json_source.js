var Form = vdom.ui.load("ui.mainWindow");

function MainWindow(parent) {
    this.form_ = Form;

    this.menuBar = new QMenuBar(this.form);
    this.form.setMenuBar(this.menuBar);
    this.form.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea);

    this.toolBars = {};
    this.menus = {};
    this.docks = {};
}

Object.defineProperty(MainWindow.prototype, "form", {
        get: function() { return this.form_; }
});

MainWindow.prototype.init = function() {
}

MainWindow.prototype.setEditor = function(widget) {
    this.form.setCentralWidget(widget);
}

MainWindow.prototype.addWidgetToDock = function(dockArea, widget, title, tabify) {
    var newDock = new QDockWidget(title, this.form_);
    newDock.setWidget(widget);
    this.form_.addDockWidget(dockArea, newDock);

    var existingDocks = this.docks.hasOwnProperty(dockArea) ? this.docks[dockArea] : [];
    if (tabify && existingDocks.length > 0) {
        this.form_.tabifyDockWidget(existingDocks[existingDocks.length-1], newDock);
    }

    existingDocks.push(newDock);
    this.docks[dockArea] = existingDocks;
    return newDock;
}

MainWindow.prototype.show = function() {
    this.form.show();
};

MainWindow.prototype.setMenuActions = function(menuName, actions) {
    var menu = this.menus[menuName];
    if (!menu) {
        menu = this.menus[menuName] = this.menuBar.addMenu(qsTr(menuName))
    }
    for (var i = 0; i < actions.length; i++) {
        menu.addAction(actions[i]);
    }
  /*
    if (toolbarName) {
        var toolbar = this.toolBars[toolbarName];
        if (!toolbar) {
            toolbar = this.toolBars[toolbarName] = new QToolBar(qsTr(toolbarName));
            this.form.addToolBar(toolbar);
        }
        toolbar.addAction(action);
    }*/
}
MainWindow.prototype.setToolbarActions = function(barName, actions) {
    var toolbar = this.toolBars[barName];
    if (!toolbar) {
        toolbar = this.toolBars[barName] = new QToolBar(qsTr(barName));
        this.form.addToolBar(toolbar);
    }
    for (var i = 0; i < actions.length; i++) {
        toolbar.addAction(actions[i]);
    }
}
