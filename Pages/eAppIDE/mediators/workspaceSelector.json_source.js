function WorkspaceSelector(parent) {
    this.parent = parent;

    this.selectedWorkspace = null;
}

WorkspaceSelector.prototype.selectWorkspace = function(workspaces) {
    this.selectedWorkspace = null;
    var wp_list = [];
    var wp_names = [];

    for (var id in Object.keys(workspaces)) {
        wp_list.push(workspaces[id]);
        wp_names.push(workspaces[id].name);
    }
    var result = QInputDialog.getItem(
        this.parent,
        "Select workspace",
        "Workspaces",
        wp_names,
        0,
        false,
        Qt.Dialog
    );

    if (result !== null) {
        var index = wp_names.indexOf(result);
        this.selectedWorkspace = wp_list[index];
        return true;
    }
    return false;
}
