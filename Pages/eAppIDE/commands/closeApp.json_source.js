include("eAppIDE.mvc.createcommand")
include("eAppIDE.mvc.facade")
include("eAppIDE.eventNames")

CloseAppCommand = CreateCommand(null,
    function () {
        qApp.quit();
    },
    "CloseApp",
    [ EVENTS.QUIT_TRIGGERED ],
    true /* register now */
);