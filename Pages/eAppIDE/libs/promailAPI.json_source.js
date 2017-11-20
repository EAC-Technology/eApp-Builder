include("serverRPC")

function PromailAPI() {

}

PromailAPI.pack = function( args ) {
    return JSON.stringify( args )
}

PromailAPI.unpack = function( text ) {
    try {
        return JSON.parse( text )
    }
    catch(er) {
        return [ 'error', 'parse error' ]
    }

    return SimpleXML.loads( text )
}

//
// Process server response
//
PromailAPI.processResponse = function( response ) {
    if (typeof response === 'undefined') {
        var error = "Response must not be 'undefined'";
        print(error);
        throw error;
    }

    // convert xml to objects
    var result = this.unpack( response )

    // get status and result of response
    var status = 'error'
    var answer = ''
    if (result) {
        status = result[0]
        answer = result[1]
    }

    if (status == 'success')
        return answer

    // else - proccess server's error
    var message = result[2] || answer;

    // print error message to debug console
    if( status == 'error' ) {
        print( '*** API Error' );
        throw message
    }

    return null;
}



//
// call of server action.
//
PromailAPI.call = function( action, args ) {
    // prepare data
    var data = this.pack( args )

    // call action
    var response = ServerRPC.syncCall( action, data )

    return this.processResponse( response )
}



PromailAPI.asyncCall = function( action, args ) {
    //
    // create special async closue for ServerAPI calls
    //
    function AsyncServerAPI( name, xml ) {
        // save action name for signals
        this.name = name

        // create async caller
        this.caller = ServerRPC.asyncCall( name, xml )


        // signal that call finished
        this.finished = signal()
        // signal that error
        this.error = signal()


        // start async caller
        this.call = function() {
            this.caller.call()
        }


        // slot for caller finished signal
        this.caller.finished.connect( this, function( response ) {
            var result = null
            try {
                result = PromailAPI.processResponse( response )
            }
            catch( error ) {
                PromailAPI.debugPrint( this.name, error )
                this.error.emit(error)
                return;
            }

            this.finished.emit( result )
        })
    }


    // prepare xml
    var xml_data = this.pack( args )
    return new AsyncServerAPI( action, xml_data )
}


//
// debug print if error in server api action
//
PromailAPI.debugPrint = function( actionName, error ) {
    print( '+--------------------------------------------' )
    print( '| error in action: ' + actionName.toUpperCase() )
    print( '+--------------------------------------------' )
    print( error )
    print()
}

//
// safe call that catch exceptions
//
PromailAPI._safeCall = function( actionName, args ) {
    var response = null
    try {
        response = this.call( actionName, args )
    }
    catch( error ) {
        this.debugPrint( actionName, error )
        return null
    }

    return response
}


PromailAPI.listPlugins = function() {
    return this.asyncCall("list_plugins");
}

PromailAPI.login = function(login, password) {
    return this.asyncCall("login", {
        login: login,
        password: password
    });
}

PromailAPI.listPluginResourcesSync = function(id) {
    return this._safeCall("list_plugin_resources", {
        guid: id
    });
}

PromailAPI.getPluginResource = function(plugin, resourceName) {
    return this.asyncCall("get_plugin_resource", {
        plugin_id: plugin,
        name: resourceName
    });
}

PromailAPI.setPluginResource = function(plugin, resourceName, data) {
    return this.asyncCall("set_plugin_resource", {
        plugin_id: plugin,
        name: resourceName,
        source: data
    });
}

PromailAPI.deletePluginResource = function(plugin, resourceName) {
    return this.asyncCall("delete_plugin_resource", {
        plugin_id: plugin,
        name: resourceName
    });
}