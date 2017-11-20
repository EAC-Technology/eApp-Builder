function ProjectTree(parent) {
    QTreeView.call(this, parent);

    this.setStyleSheet("background-color: white;");
    this.headerHidden = true;
    this.editTriggers = EDIT_TRIGGERS;
    this.expandsOnDoubleClick = false;

}

var EDIT_TRIGGERS = 8 /* EditKeyPressed */ /* +2 DoubleClicked */;

ProjectTree.prototype = new QTreeView();