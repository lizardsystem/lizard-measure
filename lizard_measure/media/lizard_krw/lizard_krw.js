// jslint configuration
/*jslint browser: true */
/*global $, OpenLayers, window, verticalItemHeight, mainContentWidth,
show_popup, nothingFoundPopup */

function redirect_to_area(data) {
    if (data !== "" && data !== undefined) {
        window.location = data;
    }
    else {
        nothingFoundPopup();
    }
}

function homepage_area_click_handler(x, y, map) {
    $("#map_OpenLayers_ViewPort").css("cursor", "progress");
    $.get(
        "/krw/homepage_area_search/", { x: x, y: y },
        function (data) {
            $("#map_OpenLayers_ViewPort").css("cursor", "default");
            redirect_to_area(data);
        });
}
