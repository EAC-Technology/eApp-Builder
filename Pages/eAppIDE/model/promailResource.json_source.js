include("resourceDefines")

function PromailResource(name, id, type) {
    this.name = name;
    this.id = id;
    this.type = type;

    this.children = null;
    this.parent = null;
    this.content = null;
}

PromailResource.TYPES = {
    PLUGIN: "plugin",
    RESOURCE: "resource"
}

// Is necessary as saving Resource object in Qt::Variant removes type information
PromailResource.getEditorType = function(resource) {
    if (resource.type == PromailResource.TYPES.PLUGIN) {
        return RESOURCE_EDITORS.NoEditor;
    }

    if (resource.name.endsWith(".xml") || resource.name.endsWith(".vxml")) {
        return RESOURCE_EDITORS.GuiEditor;
    }

    if(resource.name.endsWith(".js") || resource.name.endsWith(".css")) {
        return RESOURCE_EDITORS.TextEditor;
    }

    return RESOURCE_EDITORS.NoEditor;
}

PromailResource.isEditable = function(resource) {
    return PromailResource.getEditorType(resource) != RESOURCE_EDITORS.NoEditor;
}

PromailResource.isContainer = function(resource) {
    return resource.type == Resource.TYPES.PLUGIN;
}
