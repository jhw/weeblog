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

var SVDemo={
    bindButton: function(item) {
	var button=$("<button>").attr({
	    type: "button",
	    class: "btn btn-info btn-lg"
	}).text("Load").click(function() {
	    var text=$(this).text();
	    if (text==="Load") {
		Sunvox.load(item.filename, item.slot);
		$(this).text("Play").attr("class", "btn btn-primary btn-lg");
	    } else if (text==="Play") {
		sv_play_from_beginning(item.slot);
		$(this).text("Stop").attr("class", "btn btn-warning btn-lg");
	    } else if (text=="Stop") {
		sv_stop(item.slot);
		$(this).text("Play").attr("class", "btn btn-primary btn-lg");
	    };
	});
	$(item.id).append(button);
    },    
    initButtons: function(items) {
	for (var i=0; i < items.length; i++) {
	    var item=items[i];
	    item.slot=i;
	    SVDemo.bindButton(item);
	}
    }
};

$(document).ready(function() {
    JQDemo.init("#jquery-demo");
    SVDemo.initButtons([{
	id: "#sunvox-demo",
	filename: "/assets/sunvox/posts/2020-01/city_dreams.sunvox"	
    }], "btn-info btn-lg");
});
