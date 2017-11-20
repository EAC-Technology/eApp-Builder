function ServerRPC() {

}

ServerRPC.api = vdom.application.object("5073ff75-da99-44fb-a5d7-e44e5ab28598");

vdom.applicationService.sessionRestored.connect( function(host,login) {
    ServerRPC.api = vdom.application.object( '5073ff75-da99-44fb-a5d7-e44e5ab28598' )
});


//
// Sync call
//
ServerRPC.syncCall = function( name, data ) {
    //Agent.print( 'ServerAPI call: ' + name + '\n' )
    var reply = this.api.serverActionCall(name, data);
    reply.waitForFinished();
    var ret =  reply.result;
    delete reply;
    return ret;
}


//
// Async Call
//
ServerRPC.asyncCall = function( name, data ) {
    function AsyncCaller( name, data ) {
        // save action name and data
        this.action = name
        this.data = data

        // signal that call has finished
        this.finished = signal()

        this.timer = new QTimer()
        this.timer.singleShot = true
        this.timer.timeout.connect( this, function() {
            this.timer.stop()
            var response = ServerRPC.syncCall( this.action, this.data )
            this.finished.emit( response )
        })

        // call action asynchroniously
        this.call = function() {
            this.timer.start( 10, true )
        }
    }

    return new AsyncCaller( name, data )
}