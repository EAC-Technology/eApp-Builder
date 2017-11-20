include("eAppIDE.libs.builderAPI")
include("builderTypesFactory")

function BuilderModel() {
    this.objects = null;

    this._cache = {};
}

BuilderModel.prototype.init = function() {

}

BuilderModel.prototype.getModelElement = function(res_id) {
    return this._cache[res_id];
}

BuilderModel.prototype.saveModelElement = function(res_id, resource) {
    return this._cache[res_id] = resource;
}

BuilderModel.prototype.removeModelElement = function(res_id) {
    delete this._cache[res_id];
}

BuilderModel.prototype.getObjects = function() {
    if (!this.objects) {
        this.objects = BuilderAPI.getObjects();
    }
    return this.objects;
}

BuilderModel.prototype.login = function(user, pass) {
    return BuilderAPI.login(user, pass);
}

BuilderModel.prototype.hasWorkspaces = function() {
    return true;
};

BuilderModel.prototype.listWorkspaces = function() {
    return this.getObjects().then(function(objects) {
        var root = new BuilderType(ResTypes.RootElement, null, {
            id: "BuilderModelRootItemId",
        });
        root.children = [];

        for (var i = 0; i < objects.workspaces.length; i++) {
            objects.workspaces[i].parent = root.id;

            var workspace = new BTypeWorkspace(BuilderAPI, objects.workspaces[i]);
            root.children.push(workspace.id);
        }

        Facade.getInstance().saveModelElement(root);
        return root.id;
    });
}


BuilderModel.prototype.getWorkspaceData = function(workspace) {
    var self = this;

    return this.getObjects().then(function(objects) {
        var facade = Facade.getInstance();
        // Find workspace with matching guid
        var wp = JSONPath.eval(objects, "$.workspaces[?(@.guid=='" +workspace.id+ "')]")[0];

        if (!wp) {
            throw "No such workspace: \"" + workspace.name + "\"; \"" + workspace.id + "\"";
        }

        var ret = {
            name: wp.name,
            id: wp.guid,
            desription: wp.description,
            type: ResTypes.Workspace,

            children: [], // Application guids will be here
        };
        var widgetsContainer = {
            name: "Widgets",
            type: ResTypes.WidgetContainer,
            id: ret.id + "_widgets",
            parent: ret.id,
        };
        widgetsContainer.children = self.saveElementsArray(
            wp.widgets,
            widgetsContainer.id,
            ResTypes.Widget),
        ret.widgetsContainer = widgetsContainer.id;

        for (var i = 0; i < wp.applications.length; i++) {
            ret.children.push(self.saveApplication(wp.applications[i], ret.id));
        }
        ret.children.push(widgetsContainer.id);

        facade.saveModelElement(widgetsContainer.id, widgetsContainer);
        facade.saveModelElement(ret.id, ret);

        return ret;
    });
}

BuilderModel.prototype.newResource = function(resource_name, container_id) {
    var facade = Facade.getInstance();
    var container = facade.getModelElement(container_id);

    var promise = new Promise(function(resolve, reject) {
        if (container.type != ResTypes.ResourceContainer) {
            reject("Can not create new resource in container of type \"" +
                container.type + "\"");
            return;
        }

        var req_data = {
            name: resource_name,
            application_id: container.parent,
        };
        resolve(req_data);
    }).then(function(req_data) {
        return BuilderAPI.createResource(req_data);
    }).then(function(data) {
        var res_id = Object.keys(data);
        if (res_id.length != 1) {
            throw "No resource was created" ;
            return;
        }

        var resource = data[res_id[0]];
        resource.id = resource.guid;
        delete resource.guid;

        resource.parent = container.id;
        resource.type = ResTypes.Resource;
        facade.saveModelElement(resource.id, resource);

        container.children.push(resource.id);
        facade.saveModelElement(container.id, container);

        return resource.id;
    });
    return promise;
}

BuilderModel.prototype.getContent = function(elem_id) {
    var promise = new Promise(function(resolve, reject) {
        var facade = Facade.getInstance();
        var elem = facade.getModelElement(elem_id);

        var promise = elem.fetchContent(BuilderAPI);

        resolve(promise);
    });
    return promise;
}

BuilderModel.prototype.updateContent = function(resource, content) {
    var promise = resource.updateContent(BuilderAPI, content).then(function(res) {
        Facade.getInstance().saveModelElement(resource.id, res);
        return res;
    });
    return promise;
}

BuilderModel.prototype.deleteResource = function(res_id) {
    var facade = Facade.getInstance();

    var promise = new Promise(function(resolve, reject) {
        var resource = facade.getModelElement(res_id);
        if (!resource) {
            reject("Unknown resource ID");
        }

        resolve(resource.deleteSelf());
    }).then(function(guids) {
        return BuilderAPI.deleteResources(guids);
    }).then(
        function(data) {
            var result = data[res_id];

            if (!result) {
                throw "No response from server for resource \"" + res_id + "\"";
            }
            if (result != "deleted") {
                throw "Failed to delete resource \"" + res_id + "\": \"" + result + "\"";
            }

            var parent = facade.getModelElement(resource.parent);
            var index = parent.children.indexOf(resource.id);
            if (index > -1) {
                parent.children.splice(index, 1);
            }
            facade.saveModelElement(parent.id, parent);
            facade.removeModelElement(resource.id);
            return resource.id;
        }
    );
    return promise;
}
