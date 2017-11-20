include("promailResource")

include("eAppIDE.libs.promailAPI")

function PromailModel () {
}

PromailModel.prototype.init = function() {
    this.Logger = Logger.get("PromailModel");

    // Set global Resource function to this model's PromailResource
    var f = function() {
        Resource = PromailResource;
    };
    f();
}

PromailModel.prototype.login = function(login, password) {
    var promise = new Promise(function(resolve, reject) {
        var request = PromailAPI.login(login, password);
        request.finished.connect(function() {
            resolve();
        });
        request.error.connect(function(message) {
            reject(message);
        });
        request.call();
    });

    return promise;
}

PromailModel.prototype.hasWorkspaces = function() {
    return false;
};

PromailModel.prototype.getWorkspaceData = function() {
    var facade = Facade.getInstance();

    var promise = new Promise(function(resolve, reject) {
        var call = PromailAPI.listPlugins();
        call.finished.connect(this, function(plugins_list) {
            var root = {id: ROOT_ITEM_ID};

            root.children = plugins_list.map(function(plugin_data) {
                var plugin = new PromailResource(
                    plugin_data.name,
                    plugin_data.id,
                    PromailResource.TYPES.PLUGIN);
                plugin.picture = plugin_data.picture;
                plugin.description = plugin_data.description;
                plugin.author = plugin_data.author;
                plugin.parent = root.id;

                var children_ids = PromailAPI.listPluginResourcesSync(plugin.id);
                plugin.children = children_ids.map(function(name) {
                    var child_id = plugin.id + "_" + name;

                    // Generate resource data and save it as element of model
                    var child = new PromailResource(
                        name,
                        child_id,
                        PromailResource.TYPES.RESOURCE);
                    child.parent = plugin.id;
                    facade.saveModelElement(child_id, child);

                    // Return resource data id
                    return child_id;
                });
                // Save plugin data as element of model
                facade.saveModelElement(plugin.id, plugin);

                return plugin.id;
            });

            facade.saveModelElement(root.id, root);
            resolve(root);
        });
        call.error.connect(this, function(error) {
            reject(error);
        });
        call.call();
    });
    return promise;
};


PromailModel.prototype.getContent = function(resource_id) {
    var promise = new Promise(function(resolve, reject) {
        var facade = Facade.getInstance();
        var resource = facade.getModelElement(resource_id);

        assert(resource, "No resource for id \"" + resource_id + "\"");
        assert(resource.type == PromailResource.TYPES.RESOURCE,
            "Requested id is not resource: \"" + resource_id + "\"");

        var call = PromailAPI.getPluginResource(resource.parent, resource.name);
        call.finished.connect(function(data64) {
            var data = fromBase64(data64);
            resource.content = data;
            facade.saveModelElement(resource.id, resource);

            resolve(resource.id);
        });
        call.error.connect(function(error) {
            reject(error);
        });
        call.call();
    });
    return promise;
};

PromailModel.prototype.saveContent = function(resource) {
    var promise = new Promise(function(resolve, reject) {
        if (!resource.parent) {
            throw "Resource without a parent can not be saved";
        }

        var data = toBase64(resource.content);
        var call = PromailAPI.setPluginResource(resource.parent, resource.name, data);
        call.finished.connect(function() {
            Facade.getInstance().saveModelElement(resource.id, resource);

            resolve(resource.id);
        });
        call.error.connect(function() {
            reject(JSON.stringify([].slice.apply(arguments)));
        });
        call.call();
    });
    return promise;
}

PromailModel.prototype.newResource = function(resourceName, plug_id) {
    var self = this;

    return new Promise(function(resolve, reject) {
        var resource = new PromailResource(
            resourceName,
            plug_id + "_" + resourceName,
            PromailResource.TYPES.RESOURCE);
        resource.parent = plug_id;
        resource.content = "";

        var plugin = Facade.getInstance().getModelElement(plug_id);
        if (resource.id in plugin.children) {
            reject("Resource \"" + resourceName + "\" already exists");
            return;
        }

        resolve(resource);
    }).then(function(resource) {
        return self.saveContent(resource);
    }).then(function(res_id) {
        var facade = Facade.getInstance();
        // resource saving is done by saveContent
        // facade.saveModelElement(resource.id, resource);

        var plugin = facade.getModelElement(plug_id);
        plugin.children.push(res_id);
        facade.saveModelElement(plugin.id, plugin);

        return res_id;
    });
}

PromailModel.prototype.deleteResource = function(resource_id) {
    return new Promise(function(resolve, reject) {
        var facade = Facade.getInstance();

        var resource = facade.getModelElement(resource_id);

        if (resource.type == PromailResource.TYPES.PLUGIN) {
            reject("Can't delete plugin");
        }

        var call = PromailAPI.deletePluginResource(resource.parent, resource.name);
        call.finished.connect(function() {
            var parent = facade.getModelElement(resource.parent);
            var index = parent.children.indexOf(resource.id);
            if (index > -1) {
                parent.children.splice(index, 1);
            }
            facade.saveModelElement(parent.id, parent);

            facade.removeModelElement(resource.id);
            resolve(resource.id);
        });
        call.error.connect(function() {
            reject(JSON.stringify([].slice.apply(arguments)));
        });
        call.call();
    });
}
