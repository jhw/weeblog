var Sunvox={    
    loadSlot: function(item, button) {
	console.log("loading "+item.filename+" in slot "+item.slot);
	var loadFromArrayBuffer=function(buf) {
	    if (buf) {
		var byteArray=new Uint8Array(buf);
		sv_open_slot(item.slot);
		var sv=sv_load_from_memory(item.slot, byteArray);
		if (sv===0) {
		    $(button).text("Play").attr("class", "btn btn-primary btn-lg");
		    console.log("loaded "+item.filename+" in slot "+item.slot);
		} else {
		    console.log("error loading "+item.filename+" in slot "+item.slot);
		}
	    }
	};
	var req=new XMLHttpRequest();
	req.open("GET", item.filename, true);
	req.responseType="arraybuffer";
	req.onload=function(e) {
	    if(this.status!=200) {
		console.log(item.filename+" not found");
            } else {
		var arrayBuffer=this.response;
		loadFromArrayBuffer(arrayBuffer);
	    }
	};
	req.send(null);
    },
    bindButton: function(item) {
	var button=$("<button>").attr({
	    type: "button",
	    class: "btn btn-info btn-lg"
	}).text("Load").click(function() {
	    var text=$(this).text();
	    if (text==="Load") {
		Sunvox.loadSlot(item, this);
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
	    Sunvox.bindButton(item);
	}
    }
};

svlib.then(function(Module) {
    console.log("SunVoxLib loading is complete");
    var ver=sv_init(0, 44100, 2, 0); 
    if(ver >= 0) {
        var major=( ver >> 16 ) & 255;
        var minor1=( ver >> 8 ) & 255;
        var minor2=( ver ) & 255;
        console.log("SunVox lib version: "+major+" "+minor1+" "+minor2);
	console.log("init ok");
    } else {
	console.log("init error");
	return;
    }
});
