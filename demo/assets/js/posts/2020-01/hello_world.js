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

var SVButtonPlaying="btn btn-danger btn-lg";
var SVButtonStopped="btn btn-info   btn-lg";

var SVDemo={
    isPlaying: function(id) {
	return $(id).find("button").attr("class")==SVButtonPlaying;
    },
    renderPlaying: function(id) {
	$(id).find("button").attr("class", SVButtonPlaying).text("Stop");
    },
    renderStopped: function(id) {
	$(id).find("button").attr("class", SVButtonStopped).text("Play");
    },
    renderAllStopped: function() {
	$.each($(":button"), function(i, button) {
	    var id="#"+$(button).parent().attr("id");
	    if (SVDemo.isPlaying(id)) {
		SVDemo.renderStopped(id);
	    }
	});
    },
    bind: function(id, slot) {
	var button=$("<button>").attr({
	    type: "button",
	    "class": SVButtonStopped,	    
	}).css({
	    "margin-bottom": "25px"
	}).text("Play").click(function() {
	    if (!SVDemo.isPlaying(id)) {
		sv_stop(slot);
		SVDemo.renderAllStopped();
		SVDemo.renderPlaying(id);
		sv_play_from_beginning(slot);
	    } else {
		SVDemo.renderStopped(id);
		sv_stop(slot);
	    }
	});
	$(id).append(button);
    }
};

$(document).ready(function() {
    JQDemo.init("#jquery-demo");
    SVDemo.init("#sunvox-demo",
		"/assets/sunvox/posts/2020-01/city_dreams.sunvox");
});
