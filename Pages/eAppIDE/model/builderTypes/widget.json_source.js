
// ==========================
//          Widget
// ==========================

function BTypeWidget (api, data) {
    BuilderType.apply(this, [ResTypes.Widget, api, data]);

    this.e2vdom = null;
    this.vdomxml = null;
    this.attributes = [];
}
BTypeWidget.prototype = Object.create(BuilderType.prototype);
Object.defineProperties(BTypeWidget.prototype, {
    content: {
        get: function() { return this.vdomxml; },
        set: function(value) { this.vdomxml = value; }
    },
});

BTypeWidget.prototype.getEditorType = function() {
    return RESOURCE_EDITORS.GuiEditor;
}

BTypeWidget.createElementFromContainer = function(container, newName) {
    var facade = Facade.getInstance();

    // widget is placed inside BTypeContainer which resides in BTypeWorkspace
    // workspace ID is container.parent
    var promise = container.api.createWidget(newName, container.parent).then(function(result) {
        var resource = new BTypeWidget(container.api, result);
        resource.parent = container.id;

        container.children.push(resource.id);
        facade.saveModelElement(resource);
        return resource;
    });
    return promise;
}

BTypeWidget.prototype.readContent = function() {
    if (this.vdomxml) {
        return Promise.resolve(this);
    }

    var self = this;
    var promise = this.api.readWidget(self.id).then(
        function(source) {
            self.processXMLContent(source);
            return self;
        }
    );
    return promise;
}

BTypeWidget.prototype.saveContent = function(content) {
    if (content == this.vdomxml) {
        return Promise.resolve(this);
    }

    var self = this;
    var promise = Promise.resolve().then(function() {
        return self.buildXML({vdomxml: content});
    }).then(function(newXml) {
        self.newXml = newXml;
        return self.api.saveWidget(self.id, self.newXml);
    }).then(function(savedContent) {
        self.newXml = undefined;
        self.processXMLContent(savedContent);
        return self;
    });
    return promise;
}

BTypeWidget.prototype.deleteSelf = function() {
    var self = this;
    var promise = self.api.deleteWidget(self.id).then(function() {
        removeFromParent(self.parent, self.id);
        return self;
    });
    return promise;
}

BTypeWidget.prototype.processXMLContent = function(source) {
    this.originalSource = source;
    var reader = new QXmlStreamReader(source);

    reader.readNextStartElement();
    while (!reader.atEnd()) {
        var name = reader.name().toLowerCase();

        switch (name) {
            case "widget":
            case "attributes":
                break;
            case "attribute":
                this.attributes.push(reader.attributes());
                break;
            case "vdomxml":
                this.vdomxml = reader.readElementText(QXmlStreamReader.IncludeChildElements);
                break;
            case "e2vdom":
                this.e2vdom = reader.readElementText(QXmlStreamReader.IncludeChildElements);
                break;
            default:
                Logger.debug("processXMLContent: unknown XML tag " + reader.name());
        };

        reader.readNextStartElement();
    }
}

BTypeWidget.prototype.buildXML = function(newData) {
    var to_write = {};
    var self = this;
    function merge(attr) {
        to_write[attr] = attr in newData? newData[attr] : self[attr];
    }
    merge("attributes");
    merge("vdomxml");
    merge("e2vdom");

    var bytes = new QByteArray();
    var writer = new QXmlStreamWriter(bytes);
    writer.setAutoFormatting(true);

    writer.writeStartElement("WIDGET");

    if (to_write["attributes"].length > 0) {
        writer.writeStartElement("Attributes");
        for (var i = 0; i < to_write["attributes"].length; i++) {
            writer.writeStartElement("Attribute");
            writer.writeAttributes(to_write["attributes"][i]);
            writer.writeEndElement();
        }
        writer.writeEndElement();
    }

    if (to_write["vdomxml"]) {
        writer.writeStartElement("VDOMXML");
        writer.writeCDATA(to_write["vdomxml"]);
        writer.writeEndElement();
    }
    if (to_write["e2vdom"]) {
        writer.writeStartElement("E2VDOM");
        writer.writeCDATA(to_write["e2vdom"]);
        writer.writeEndElement();
    }

    writer.writeEndElement();
    writer.writeEndDocument();

    var textStream = new QTextStream(bytes);
    textStream.setCodec("utf-8");
    var result = textStream.readAll();
    return result;
}

