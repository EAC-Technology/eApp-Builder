function ResourceManager(resources) {
    for (var res in resources) {
        vdom.resourceManager.addResource(res, resources[res]);
    }
    vdom.resourceManager.update();
}

ResourceManager.prototype.name = "ResourceManager";

ResourceManager.prototype.getIcon = function(aliasOrGuid) {
    return vdom.resourceManager.resource(aliasOrGuid).toIcon();
}
