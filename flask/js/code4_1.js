/* Google Maps APIサンプル */

function initialize() {
  if (GBrowserIsCompatible()) {
    var map = new GMap2(document.getElementById("map_canvas"));
    map.setCenter(new GLatLng(38.074987,138.441467), 11);
    map.addControl(new GMapTypeControl());
  }
}
