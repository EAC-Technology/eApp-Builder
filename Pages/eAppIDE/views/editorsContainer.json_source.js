function EditorsContainer(parent) {
    QTabWidget.call(this, parent);
}

EditorsContainer.prototype = new QTabWidget();

EditorsContainer.prototype.findPageByObjectName = function(objectName) {
    for (var i = 0; i < this.count; i++) {
        if (this.widget(i).objectName == objectName) {
            return this.widget(i);
        }
    }
    return null;
}
