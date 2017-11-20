// ==========================
//          Workspace
// ==========================
function BTypeWorkspace(api, wp_data) {
    BuilderType.apply(this, [ResTypes.Workspace, api, wp_data]);
    this.description = wp_data.description;

    var facade = Facade.getInstance();

    this.children = create_objects(
        BTypeApplication,
        this.id,
        api,
        wp_data.applications);

    var widgetsContainer = new BTypeContainer(
        api,
        ResTypes.Widget,
        {
            name: "Widgets",
            parent: this.id,
        });
    this.children.push(widgetsContainer.id);
    widgetsContainer.children = create_objects(
        BTypeWidget,
        widgetsContainer.id,
        api,
        wp_data.widgets);

    facade.saveModelElement(widgetsContainer);
    facade.saveModelElement(this);
}
BTypeWorkspace.prototype = Object.create(BuilderType.prototype);


// ==========================
//          Application
// ==========================

function BTypeApplication(api, app_data) {
    BuilderType.apply(this, [ResTypes.Application, api, app_data]);
    this.author = app_data.author;
    this.children = [];
    this.api = api;

    var views = new BTypeContainer(
        api,
        ResTypes.View,
        {
            name: "Views",
            parent: this.id,
        });
    views.children = create_objects(
        BTypeView,
        views.id,
        api,
        app_data.views);
    facade.saveModelElement(views);
    this.children.push(views.id);

    var resources = new BTypeContainer(
        api,
        ResTypes.Resource,
        {
            name: "Resources",
            parent: this.id,
        });
    resources.children = create_objects(
        BTypeResource,
        resources.id,
        api,
        app_data.resources);
    facade.saveModelElement(resources);
    this.children.push(resources.id);
}
BTypeApplication.prototype = Object.create(BuilderType.prototype);


// ==========================
//          General Container
// ==========================

function BTypeContainer (api, elemType, data) {
    if (! ("id" in data)) {
        data["id"] = data.parent + "_" + data.name;
    }

    BuilderType.apply(this, [elemType, api, data]);
    this.children = [];
}
BTypeContainer.prototype = Object.create(BuilderType.prototype);

BTypeContainer.prototype.createChild = function(name) {
    if (this.type == ResTypes.Resource) {
        return BTypeResource.createElementFromContainer(this, name);
    } else if (this.type == ResTypes.Widget) {
        return BTypeWidget.createElementFromContainer(this, name);
    }

    throw Error("Creating children of type '" + this.type + "' is not implemented");
}


// ==========================
//          View
// ==========================

function BTypeView (api, data) {
    BuilderType.apply(this, [ResTypes.View, api, data]);
}
BTypeView.prototype = Object.create(BuilderType.prototype);


// ==========================
//          Resource
// ==========================

function BTypeResource (api, data) {
    BuilderType.apply(this, [ResTypes.Resource, api, data]);
}
BTypeResource.prototype = Object.create(BuilderType.prototype);

BTypeResource.createElementFromContainer = function(container, newName) {
    var facade = Facade.getInstance();
    var promise = container.api.createResource(newName, container.parent).then(function(result) {
        var resource = new BTypeResource(container.api, result);
        resource.parent = container.id;

        container.children.push(resource.id);
        facade.saveModelElement(resource);
        return resource;
    });
    return promise;
}


BTypeResource.prototype.getEditorType = function() {
    if (this.name.endsWith(".xml") || this.name.endsWith(".vxml")) {
        return RESOURCE_EDITORS.GuiEditor;
    }

    return RESOURCE_EDITORS.TextEditor;
}
BTypeResource.prototype.isContainer = function() {
    return false;
}

BTypeResource.prototype.readContent = function() {
    if (typeof this.content !== 'undefined') {
        return Promise.resolve(this);
    }

    var self = this;
    var promise = this.api.readResource(self.id).then(
        function(content) {
            self.content = content;
            return self;
        }
    );
    return promise;
}

BTypeResource.prototype.saveContent = function(content) {
    if (content == this.content) {
        return Promise.resolve(this);
    }

    var self = this;
    var promise = self.api.saveResource(self.id, content).then(function() {
        self.content = content;
        return self;
    });
    return promise;
}

BTypeResource.prototype.deleteSelf = function() {
    var self = this;
    var promise = self.api.deleteResource(self.id).then(function() {
        removeFromParent(self.parent, self.id);
        return self;
    });
    return promise;
}
