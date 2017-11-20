function toBase64(data) {
    var bytes = new QByteArray(data);
    var b64 = bytes.toBase64();
    return b64.toString();
}

function fromBase64(data) {
    var b64 = new QByteArray(data);
    var bytes = QByteArray.fromBase64(b64);
    return bytes.toString();
}