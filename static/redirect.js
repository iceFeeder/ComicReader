var vol=1;
var page=1;

function s_click(obj) {
    var num = 0;
    for (var i = 0; i < obj.options.length; i++) {
        if (obj.options[i].selected == true) {
            if (obj.name == "vol") {
                vol = obj.options[obj.selectedIndex].value
            } else if(obj.name == "page") {
                page = obj.options[obj.selectedIndex].value
            }
            break
        }
    }
}

function jump() {
    url = "/" + vol + "/" + page
    window.open(url)
}