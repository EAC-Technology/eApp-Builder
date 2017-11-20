function assert(condition, message) {
    if (!condition) {
        Logger.error(message);
        throw new Error(message);
    }
}
