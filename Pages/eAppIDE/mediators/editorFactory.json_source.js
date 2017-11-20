include("eAppIDE.model.resourceDefines");

// ==============================================
// General Editor
function Editor(parent, resource, editorType) {
    QWidget.call(this, parent);
    this.resourceId = resource.id;

    var layout = new QVBoxLayout();
    layout.margin = 0;
    layout.spacing = 0;
    this.setLayout(layout);

    this.editorType = editorType;
    this.title = resource.name;
}

Editor.prototype = new QWidget();

Object.defineProperties(Editor.prototype, {
    "editorType": {
        get: function() { return this.property("editorType"); },
        set: function(value) { this.setProperty("editorType", value); },
    },
    "resourceId": {
        get: function() { return this.objectName; },
        set: function(value) { this.objectName = value; },
    },
    "title": {
        get: function() { return this.property("originalTitle"); },
        set: function(value) { this.setProperty("originalTitle", value); },
    },
    "editor": {
        get: function() { return this.layout().itemAt(0).widget(); },
        set: function(newEditor) {
            var layout = this.layout();

            if (layout.count() > 0) {
                layout.takeAt(0);
            }
            layout.addWidget(newEditor, 0, 0);
        },
    },
});


// ==============================================
// Text Editor

function EditorText(parent, resource) {
    Editor.apply(this, [parent, resource, RESOURCE_EDITORS.TextEditor]);

    this.editor = new QTextEdit(this);

    this.originalContent = resource.content;
    this.content = resource.content;
}
EditorText.prototype = Object.create(Editor.prototype);

Object.defineProperties(EditorText.prototype, {
    "content": {
        get: function() { return this.editor.plainText; },
        set: function(value) { this.editor.plainText = value; },
    },
    "originalContent": {
        get: function() { return this.property("originalContent"); },
        set: function(value) { this.setProperty("originalContent", value); },
    },
});

EditorText.prototype.hasUnsavedChanges = function() {
    return this.content != this.originalContent;
}

// ==============================================
// Gui Editor

function EditorGui(parent, resource) {
    Editor.apply(this, [parent, resource, RESOURCE_EDITORS.GuiEditor]);

    this.originalContent = resource.content;
    this.contentBackup = resource.content;
    this.alreadyShown = false;
}

EditorGui.prototype = Object.create(Editor.prototype);

Object.defineProperties(EditorGui.prototype, {
    "content": {
        get: function() { return vdom.wysiwyg.getContent(); },
        set: function(value) {
            if (!vdom.wysiwyg.setContent(value)) {
                Logger.error("Unable to show provided data as VdomXML. Showing first 40 symbols: '" +
                    value.substr(0, 40) + "'");
            }
        },
    },
    "contentBackup": {
        get: function() { return this.property("contentBackup"); },
        set: function(value) { this.setProperty("contentBackup", value); },
    },
    "originalContent": {
        get: function() { return this.property("originalContent"); },
        set: function(value) { this.setProperty("originalContent", value); },
    },
});

EditorGui.prototype.showEvent = function(evData) {
    this.alreadyShown = true;

    if (this.layout().count() == 0) {
        this.content = this.contentBackup;
        this.layout().addWidget(vdom.wysiwyg.form(), 0, 0);
    }
};
EditorGui.prototype.hideEvent = function(evData) {
    if (!this.alreadyShown) {
        return;
    }

    this.contentBackup = this.content;
};

EditorGui.prototype.hasUnsavedChanges = function() {
    return this.content != this.originalContent;
}

// ==============================================
// Factory

function EditorFactory() {
}

EditorFactory.Types = {};

EditorFactory.Types[RESOURCE_EDITORS.TextEditor] = EditorText;
EditorFactory.Types[RESOURCE_EDITORS.GuiEditor] = EditorGui;

EditorFactory.createEditor = function(parent, resource, editorType) {
    if (!editorType) {
        editorType = resource.getEditorType();
    }

    var constructor = EditorFactory.Types[editorType];
    if (!constructor) {
        Logger.error("EditorFactory.createEditor: unknown editor type \"" + editorType + "\"");
        return null;
    }

    var ret = new constructor(parent, resource);

    return ret;
}

EditorFactory.getEditorType = function(editor) {
    return editor.property("editorType");
}

// That fuckup is necessary as QtScript loses every property defined using JS constructs
// and accepts only data types in object.setProperty()
//
// Every time widget is recovered from Qt system (like object.layout().itemAt() or tab.widget()
// anything that was set using JS prototypes or defineProperties is lost.

EditorFactory.recoverEditor = function(editor) {
    var type = EditorFactory.getEditorType(editor);
    var editorConstructor = EditorFactory.Types[type];

    if (!editorConstructor) {
        throw new TypeError("No known constructor for editor \"" + editor +
            "\" of type \"" + type + "\"");
    }

    editor.__proto__ = editorConstructor.prototype;
    return editor;
}

