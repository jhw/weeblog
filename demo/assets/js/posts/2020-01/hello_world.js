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
    initButton: function(id, slot) {
	var button=$("<button>").attr({
	    type: "button",
	    class: "btn btn-info btn-lg"
	}).text("Load").click(function() {
	    var text=$(this).text();
	    if (text==="Load") {
		$(this).text("Play");
	    } else if (text==="Play") {
		$(this).text("Stop");
	    } else if (text=="Stop") {
		$(this).text("Play");
	    };
	});
	$(id).append(button);
    },    
    init: function() {
	SVDemo.initButton({
	    id: "#sunvox-demo",
	    filename: "",	    
	    slot: 0
	});
    }
};

$(document).ready(function() {
    JQDemo.init("#jquery-demo");
    SVDemo.init();
});
