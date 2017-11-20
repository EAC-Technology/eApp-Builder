// ==========================
//          General type
// ==========================

function BuilderType(elemType, api, data) {
    this.api = api;

    this.name = data.name;
    this.id = ('id' in data) ? data.id : data.guid;
    this.parent = data.parent;
    this.type = elemType;
}

BuilderType.prototype.isContainer = function() {
    return 'children' in this;
}

BuilderType.prototype.getEditorType = function() {
    return RESOURCE_EDITORS.NoEditor;
}

BuilderType.prototype.isEditable = function() {
    return this.getEditorType() != RESOURCE_EDITORS.NoEditor;
}

// ========================================
//              Helpers
// ========================================
function removeFromParent(parentId, selfId) {
    var facade = Facade.getInstance();
    var parent = facade.getModelElement(parentId);
    var index = parent.children.indexOf(selfId);
    if (index > -1) {
        parent.children.splice(index, 1);
    }
    facade.removeModelElement(selfId);
}

// ==========================
//          Create multiple BType objects
// ==========================
function create_objects(constructor, parent_id, api, obj_array) {
    return obj_array.map(
        function(obj_data) {
            obj_data.parent = parent_id;
            var obj = new constructor(api, obj_data);

            Facade.getInstance().saveModelElement(obj);
            return obj.id;
        });
}

include("builderTypes.widget")
include("builderTypes.types")
