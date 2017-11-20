function LoggerWindow(parent) {
    QPlainTextEdit.call(this, parent);
    this.readOnly = true;
}

LoggerWindow.prototype = new QPlainTextEdit();

LoggerWindow.prototype.appendMessage = function(message) {
    this.appendPlainText(message);
    this.verticalScrollBar().value = this.verticalScrollBar().maximum;
}