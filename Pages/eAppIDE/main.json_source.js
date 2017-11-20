var importExtension = vdom.script.importExtension;
var include = vdom.script.include;

importExtension("qt.core");
importExtension("qt.gui");
importExtension("qt.signal");
importExtension("qt.webkit");
importExtension("qt.xml");


// ### working around bug in QMenu.prototype.addAction
QMenu.prototype.addAction = QWidget.prototype.addAction;
QToolBar.prototype.addAction = QWidget.prototype.addAction;


importExtension("vdom.core");
importExtension("vdom.gui");
importExtension("vdom.desktop")

include("defines")
qApp.applicationName = APP_NAME;
qApp.applicationVersion = APP_VERSION;
qApp.organizationName = APP_ORG;

include("libs.logger")
Logger.setLevel( Logger.DEBUG );

// First include some libs in definitive order
include("libs.pa_promise")
include("libs.promise")

include("libs.*")
include("mvc.facade")
include("commands.*") // Registers Startup command
include("eventNames")
include("model.promailModel")
include("model.builderModel")

facade = Facade.getInstance();
var model = new BuilderModel();
//var model = new PromailModel();
model.init()
facade.registerModel(model);

facade.raiseEvent(EVENTS.APP_STARTED);

QCoreApplication.exec();
