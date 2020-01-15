var JQDemo={
    init: function(id) {
	var table=$("<table>").attr({
	    "class": "table table-bordered table-striped"
	});
	// head
	var thead=$("<thead>");
	var tr=$("<tr>");
	for (var i=0; i < 4; i++) {
	    var th=$("<th>").attr("class", "text-center");
	    $(th).text("Col "+(i+1));
	    $(tr).append(th);
	}
	$(thead).append(tr);
	$(table).append(thead);
	// body
	var tbody=$("<tbody>");
	for (var i=0; i < 8; i++) {
	    var tr=$("<tr>");
	    for (var j=0; j < 4; j++) {
		var td=$("<td>").attr("class", "text-center");
		$(td).text(Math.floor(Math.random()*1e5));
		$(tr).append(td);
	    }
	    $(tbody).append(tr);
	}
	$(table).append(tbody);
	// attach
	$(id).append(table);
    }
};

var SVSlot="sunvox-slot";
var SVButtonPlaying="btn btn-danger btn-lg";
var SVButtonStopped="btn btn-info btn-lg";

var SVDemo={
    bind: function(id, slot) {
	var button=$("<button>").attr({
	    type: "button",
	    "class": SVButtonStopped,	    
	}).css({
	    "margin-bottom": "25px"
	}).text("Play").click(function() {
	    var currentSlot=localStorage.getItem(SVSlot);
	    if (currentSlot===undefined) {
		sv_play_from_beginning(slot);
		$(id).find("button").attr("class", SVButtonPlaying).text("Stop");
		localStorage.setItem("sunvox-slot", slot);
	    } else {
		currentSlot=parseInt(currentSlot);
		if (slot===currentSlot) {
		    sv_stop(currentSlot);
		    $(id).find("button").attr("class", SVButtonStopped).text("Play");	
		    localStorage.setItem(SVSlot, undefined);
		}
	    }
	});
	$(id).append(button);
    },
    init: function(items) {
	for (var i=0; i < items.length; i++) {
	    var item=items[i];
	    Sunvox.load(i, item.filename);
	    SVDemo.bind(item.id, i);
	}
    }
};

$(document).ready(function() {
    JQDemo.init("#jquery-demo");
    SVDemo.init([
	{
	    id: "#sunvox-demo",
	    filename: "/assets/sunvox/posts/2020-01/city_dreams.sunvox"
	}
    ]);
});
