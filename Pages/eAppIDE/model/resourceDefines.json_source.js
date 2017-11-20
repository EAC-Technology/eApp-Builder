include("eAppIDE.actionNames")

RESOURCE_EDITORS = {
    NoEditor: "NoEditor",
    GuiEditor: "Wysiwig",
    TextEditor: "Text",
};

ResTypes = {
    RootElement: "RootElement",
    Workspace: "Workspace",
    Application: "Application",
    Widget: "Widget",
    WidgetContainer: "WidgetContainer",
    View: "View",
    ViewContainer: "ViewContainer",
    Resource: "Resource",
    ResourceContainer: "ResourceContainer",
};

ResIcons = {};
ResIcons[ResTypes.Application]      = "cb4d01af-36f7-418d-94d8-e8a0546e5877";
ResIcons[ResTypes.View]             = "5ae599b4-95c1-4f13-a817-5d4fe38cf9e9";
ResIcons[ResTypes.ViewContainer]    = "aad0d263-0f83-46b7-884e-c3c67370f237";
ResIcons[ResTypes.Resource]         = "e358c62a-2c70-400b-b100-553ee481618f";
ResIcons[ResTypes.ResourceContainer]= "35418ae0-cc2f-44bd-8dc9-a7995c22d7d6";
ResIcons[ResTypes.Widget]           = "e2c4dc59-d3ed-4dd3-b955-e44ccc7576aa";
ResIcons[ResTypes.WidgetContainer]  = "828fc32c-c275-47e5-ba89-04d956ec0221";
ResIcons[ACTIONS.Save]              = "5add2a09-471e-4529-8b54-3377cefe29c2";
ResIcons[ACTIONS.Quit]              = "42f5c57b-d45f-44ee-b7a3-db3d657538ed";
