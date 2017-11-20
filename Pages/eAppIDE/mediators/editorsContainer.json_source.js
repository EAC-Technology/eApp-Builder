include("eAppIDE.views.editorsContainer");
include("editorFactory");

//include("eAppIDE.eventNames")
//include("eAppIDE.model.resource")
//include("mainWindow")

function EditorsContainerMediator() {
    this.Logger = Logger.get("EditorsContainerMediator");

    this.tabWidget = new EditorsContainer();
    this.tabWidget.tabsClosable = true;
    this.tabWidget.currentChanged.connect(this, this.onTabPageChanged);
    this.tabWidget.tabCloseRequested.connect(this, this.onTabCloseRequested);
}

// Constructor function name and string MUST be equal!
EditorsContainerMediator.prototype.name = "EditorsContainerMediator";

Object.defineProperty(EditorsContainerMediator.prototype, "widget", {
    get: function(){ return this.tabWidget; }
});

EditorsContainerMediator.prototype.init = function() {
    this.initGuiComponents();
}

EditorsContainerMediator.prototype.initGuiComponents = function() {
    var window = Facade.getInstance().getMediator(MainWindowMediator.name);

    this.guiEditor = vdom.wysiwyg;
    this.guiEditor.initialize(window.getForm());
    this.guiEditor.modelChanged.connect(this, this.onXmlContentChanged);
    this.xmlView = new QTextEdit();

    var guiDocks = [
        {
            widget: this.guiEditor.widgetBox(),
            title: "Widget Box",
            dockArea: Qt.RightDockWidgetArea,
            tabify: true,
            editorTypes: [RESOURCE_EDITORS.GuiEditor],
        },
        {
            widget: this.guiEditor.objectInspector(),
            title: "Object Inspector",
            dockArea: Qt.RightDockWidgetArea,
            tabify: true,
            editorTypes: [RESOURCE_EDITORS.GuiEditor],
        },
        {
            widget: this.guiEditor.propertyEditor(),
            title: "Property Editor",
            dockArea: Qt.RightDockWidgetArea,
            tabify: true,
            editorTypes: [RESOURCE_EDITORS.GuiEditor],
        },
        {
            widget: this.xmlView,
            title: "XML View",
            dockArea: Qt.BottomDockWidgetArea,
            tabify: true,
            editorTypes: [RESOURCE_EDITORS.GuiEditor],
        }
    ];

    guiDocks.forEach(function(dockOptions) {
        window.addToDock(dockOptions);
    });
}

EditorsContainerMediator.prototype.getEditorById = function(resource_id) {
    var found = null;
    if (resource_id) {
        found = this.tabWidget.findPageByObjectName(resource_id);
    } else {
        found = this.tabWidget.currentWidget();
    }

    if (!found) {
        return null;
    }
    return EditorFactory.recoverEditor(found);
}

EditorsContainerMediator.prototype.getEditorByIndex = function(index) {
    var found = this.tabWidget.widget(index);
    if (!found) {
        return null;
    }
    return EditorFactory.recoverEditor(found);
}


EditorsContainerMediator.prototype.showEditor = function(resource) {
    var editor = this.getEditorById(resource.id);
    if (editor && editor == this.tabWidget.currentWidget()) {
        return;
    }

    if (!editor) {
        this.tabWidget.updatesEnabled = false;

        editor = EditorFactory.createEditor(this.tabWidget, resource);
        if (!editor) {
            return;
        }

        this.tabWidget.addTab(editor, resource.name);
        this.tabWidget.updatesEnabled = true;
    }

    this.tabWidget.setCurrentWidget(editor);
}

EditorsContainerMediator.prototype.activateEditor = function(resource_id) {
    var editor = this.getEditorById(resource_id);
    if (editor) {
        this.tabWidget.setCurrentWidget(editor);
    }
}

EditorsContainerMediator.prototype.setGuiDockVisibility = function(visible) {
    for (var widget in this.guiDocks) {
        if (this.guiDocks.hasOwnProperty(widget)) {
            this.guiDocks[widget].visible = visible;
        }
    }
}

EditorsContainerMediator.prototype.onXmlContentChanged = function() {
    var res = [], err = [];
    var content = this.guiEditor.getContent(res,err);
    if (err.length > 0) {
        content = err;
        this.xmlView.textColor = QColor.red;
    } else {
        this.xmlView.textColor = QColor.black;

    }
    this.xmlView.plainText = content;
}

EditorsContainerMediator.prototype.onTabPageChanged = function(index) {
    var editor = this.getEditorByIndex(index);
    var type = editor ? editor.editorType : RESOURCE_EDITORS.NoEditor;

    Facade.getInstance().raiseEvent(EVENTS.WINDOW_CONTEXT_CHANGED, type);
}

EditorsContainerMediator.prototype.onTabCloseRequested = function(index) {
    var editor = this.getEditorByIndex(index);
    if (!editor) {
        return;
    }

    Facade.getInstance().raiseEvent(EVENTS.CLOSE_EDITOR, editor.resourceId);
}

EditorsContainerMediator.prototype.getCurrentResourceId = function() {
    var editor = this.getEditorById();

    return editor.resourceId;
}

EditorsContainerMediator.prototype.getResourceContent = function(res_id) {
    var editor = this.getEditorById(res_id);

    if (!editor) {
        return null;
    }

    return editor.content;
}

EditorsContainerMediator.prototype.isOpen = function(resource_id) {
    return !!this.getEditorById(resource_id);
}

EditorsContainerMediator.prototype.hasUnsavedChanges = function(res_id) {
    var editor = this.getEditorById(res_id);
    return editor.hasUnsavedChanges();
}

EditorsContainerMediator.prototype.setHasUnsavedChanges = function(res_id, value) {
//    assert(value === true | value === false, "setHasUnsavedChanges: value MUST be boolean value");

 //   var editor = this.getEditorById(res_id);
 //   this.editorBootstrap.setDirty(editor, false);
}
/*
EditorsContainerMediator.prototype.onTabDirtynessChanged = function(res_id, newValue) {
    var editor = this.getEditorById(res_id);
    if (!editor) {
        return;
    }

    var index = this.tabWidget.indexOf(editor);

    var newTitle = this.editorBootstrap.getTitle(editor) + (newValue ? " *" : "");
    this.tabWidget.setTabText(index, newTitle);
}
*/

EditorsContainerMediator.prototype.closeEditor = function(res_id) {
    var editor = this.getEditorById(res_id);
    if (!editor) {
        return;
    }

    this.tabWidget.removeTab(this.tabWidget.indexOf(editor));
}


