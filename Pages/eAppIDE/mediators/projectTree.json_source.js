include("eAppIDE.mvc.facade")
include("eAppIDE.eventNames")

include("eAppIDE.views.projectTree")
include("eAppIDE.mediators.actionsContainer")
include("eAppIDE.actionNames")

function ProjectTreeMediator() {
    this.projectTree = new ProjectTree();
    this.model = new QStandardItemModel();
    this.projectTree.setModel(this.model);

    this.projectTree.doubleClicked.connect(this, this.doubleClicked);
    this.projectTree.contextMenuPolicy = Qt.ActionsContextMenu;
//    this.projectTree.customContextMenuRequested.connect(this, this.menuRequested);

    Facade.getInstance().registerCommand(EVENTS.WORKSPACE_DATA_READY, this, this.showWorkspaceDataHandler);

    this.Logger = Logger.get("ProjectTree");
}

// Constructor function name and string MUST be equal!
ProjectTreeMediator.prototype.name = "ProjectTreeMediator";

ProjectTreeMediator.prototype.init = function() {
    var facade = Facade.getInstance();
    var actions = facade.getMediator(ActionsContainer.name);

    this.projectTree.addAction(actions.get(ACTIONS.New));
    this.projectTree.addAction(actions.get(ACTIONS.Edit));

    this.projectTree.addAction(actions.get(ACTIONS.Delete));
}


Object.defineProperties(ProjectTreeMediator.prototype, {
    "widget": {
        get: function() {
            return this.projectTree;
        }
    },
    "selectedElementId": {
        get: function() {
            var index = this.projectTree.currentIndex();
            if (!index.isValid) {
                return undefined;
            }
            var item = this.model.itemFromIndex(index);
            return getItemId(item);
        }
    }
});

var DATA_ROLE = 33  /* Qt::UserRole + 1*/;
function getItemId(item) {
    return item.data(DATA_ROLE);
}
function setItemId(item, id) {
    item.setData(id, DATA_ROLE);
}

ProjectTreeMediator.prototype.showWorkspaceDataHandler = function(data) {
    var eventName = data.eventName;
    var value = data.args[0];

    var workspace = Facade.getInstance().getModelElement(value);

    this.showWorkspaceData(workspace);
}

function addElement(id, root) {
    var facade = Facade.getInstance();

    var element = facade.getModelElement(id);
    if (!element) {
        Logger.error("ProjectTreeMediator.addElement: no element for id \"" + id + "\"");
        return;
    }

    var item = new QStandardItem(element.name);
    setItemId(item, id);
    if (element.type) {
        item.setIcon(facade.getResourceIcon(element.type));
    }

    root.appendRow(item);

    if (element.children) {
        element.children.forEach(function(child_id) {
            addElement(child_id, item);
        });
    }
}

ProjectTreeMediator.prototype.showWorkspaceData = function(root) {
    this.model.clear();
    var model_root = this.model.invisibleRootItem();

    for (var i = 0; i < root.children.length; i++) {
        addElement(root.children[i], model_root);
    }
}

ProjectTreeMediator.prototype.doubleClicked = function(index) {
    var item = this.model.itemFromIndex(index);
    if (!item) {
        return;
    }

    if (item.rowCount() > 0) {
        this.projectTree.setExpanded(index, !this.projectTree.isExpanded(index));
    } else {
        Facade.getInstance().raiseEvent(EVENTS.EDIT_RESOURCE, getItemId(item));
    }
}

ProjectTreeMediator.prototype.menuRequested = function(point) {
    var index = this.projectTree.indexAt(point);
    if (!index.isValid()) {
        this.Logger.debug("menuRequested at empty point");
        return;
    }

    var facade = Facade.getInstance();
    var actions = facade.getMediator(ActionsContainer.name);

    var elem_id = getItemId(this.model.itemFromIndex(index));
    var resource = facade.getModelElement(elem_id);

    var menu = new QMenu(this.projectTree);

    if (Resource.isContainer(resource)) {
        menu.addAction(actions.get(ACTIONS.New));
    } else {
        menu.addAction(actions.get(ACTIONS.Edit));
    }/*
    menu.addSeparator();
    menu.addAction(actions.get[ACTIONS.Rename]);
    */
    menu.addAction(actions.get(ACTIONS.Delete));

    menu.exec(this.projectTree.mapToGlobal(point));
}

ProjectTreeMediator.prototype.addResource = function(element) {
    var parent_id = element.parent;

    var parents = QStandardItem_filterRecursively(
        this.model.invisibleRootItem(),
        function(item) {
            return getItemId(item) == parent_id;
        }
    );
    assert(parents.length == 1,
        "ProjectTreeMediator.addWorkspaceItem: expect exactly one element with provided id in the model");

    addElement(element.id, parents[0]);
}

ProjectTreeMediator.prototype.removeElement = function(elem_id) {
    var candidates = QStandardItem_filterRecursively(
        this.model.invisibleRootItem(),
        function(item) {
            return getItemId(item) == elem_id;
        }
    );
    assert(candidates.length == 1,
        "ProjectTreeMediator.removeElement: expect exactly one element with provided id in the model");

    var found = candidates[0];
    found.parent().removeRow(found.row());
}


function QStandardItem_filterRecursively(item, pred) {
    var count = item.rowCount();
    var result = [];
    for (var i = 0; i < count; i++) {
        var child = item.child(i);

        if (pred(child)) {
            result.push(child);
        }
        if (child.hasChildren()) {
            Array.prototype.push.apply(
                result,
                QStandardItem_filterRecursively(child, pred)
            );
        }
    }
    return result;
}
