include("promailAPI")

function BuilderAPI() {
}
BuilderAPI.pingers = [];

BuilderAPI.login = function(login, password) {
    var ret = new Promise(function(resolve, reject) {
        var request = PromailAPI.asyncCall("login", {
            login: login,
            password: password
        });
        request.finished.connect(function(data) {
            resolve(data);
        });
        request.error.connect(function(message) {
            reject(message);
        });
        request.call();
    });
    ret.then(function() {
        var pinger = setInterval(function() {
                var caller = PromailAPI.asyncCall("ping", {});
                caller.call();
            },
            PING_INTERVAL_SEC * 1000);
        BuilderAPI.pingers.push(pinger);
    });

    return ret;
}


BuilderAPI.getObjects = function() {
    var ret = new Promise(function(resolve, reject) {
        var request = PromailAPI.asyncCall("get_objects", {});
        request.finished.connect(function(data) {
            resolve(data);
        });
        request.error.connect(function(message) {
            reject(message);
        });
        request.call();
    });
    return ret;
}

// ============================
// General data accessor
// ============================

BuilderAPI.accessData = function(dataName, action, input) {
    var ret = new Promise(function(resolve, reject) {
        var request = PromailAPI.asyncCall(dataName, {
            action: action,
            data: input,
        });

        request.finished.connect(function(data) {
            resolve(data);
        });

        request.error.connect(function(message) {
            reject(message);
        });
        request.call();
    });
    return ret;
}

// ============================
// General data CRUD operations
// ============================

BuilderAPI.readData = function(dataName, guid) {
    return BuilderAPI.accessData(dataName, "read", [guid]).then(function(data) {
        var result = data[guid];
        if (!result) {
            throw new Error("Unable to fetch " + dataName + " '" + guid + "'");
        }
        return result;
    });
}

BuilderAPI.createData = function(dataName, request) {
    return BuilderAPI.accessData(dataName, "create", request).then(function(data) {
        var keys = Object.keys(data);
        if (keys.length == 0) {
            throw new Error("API returned no data");
        }
        return data[keys[0]];
    });
}

BuilderAPI.saveData = function(dataName, guid, data) {
    var request = {};
    request[guid] = data;

    return BuilderAPI.accessData(dataName, "update", request).then(function(result) {
        if (!result[guid]) {
            throw new Error("Unable to update " + dataName + " '" + guid + "'");
        }
        return result[guid];
    });
}

BuilderAPI.deleteData = function(dataName, guid) {
    return BuilderAPI.accessData(dataName, "delete", [guid]).then(function(result) {
        if (!result[guid]) {
            throw new Error("Unable to delete " + dataName + " '" + guid + "'");
        }
        return result[guid];
    });
}

// ============================
//         Resource
// ============================

BuilderAPI.readResource = function(guid) {
    return BuilderAPI.readData("eapp_resource", guid).then(function(result) {
        return result.b64content ? fromBase64(result.b64content) : "";
    });
}

BuilderAPI.createResource = function(name, app_id) {
    return BuilderAPI.createData("eapp_resource", {
        'name': name,
        'application_id': app_id,
    });
}

BuilderAPI.saveResource = function(guid, content) {
    return BuilderAPI.saveData("eapp_resource", guid, {
            'b64content': toBase64(content),
    });
}

BuilderAPI.deleteResource = function(guid) {
    return BuilderAPI.deleteData("eapp_resource", guid).then(function(status) {
        if (status != "deleted") {
            throw new Error("Unable to delete resource '" + guid + "': " + status);
        }
        return status;
    });
}


// ============================
//         Widget
// ============================



BuilderAPI.readWidget = function(guid) {
    return BuilderAPI.readData("eapp_widget", guid).then(function(result) {
        return result.b64source ? fromBase64(result.b64source) : "";
    });
}

BuilderAPI.createWidget = function(name, wp_id) {
    return BuilderAPI.createData("eapp_widget", {
        'name': name,
        'workspace_id': wp_id,
    });
}

BuilderAPI.saveWidget = function(guid, content) {
    return BuilderAPI.saveData("eapp_widget", guid, {
            'b64source': toBase64(content),
    }).then(function(result) {
        return result.b64source ? fromBase64(result.b64source) : "";
    });
}

BuilderAPI.deleteWidget = function(guid) {
    return BuilderAPI.deleteData("eapp_widget", guid).then(function(status) {
        if (status != "deleted") {
            throw new Error("Unable to delete widget '" + guid + "': " + status);
        }
        return status;
    });
}
