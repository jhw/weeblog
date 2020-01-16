var Sunvox={    
    load: function(fname, slot) {
	console.log("loading "+fname+" in slot "+slot);
	var loadFromArrayBuffer=function(buf) {
	    if (buf) {
		var byteArray=new Uint8Array(buf);
		sv_open_slot(slot);
		console.log("loading data into slot "+slot);
		svloadresp=sv_load_from_memory(slot, byteArray);
		console.log("SV load resp: "+svloadresp);
	    }
	};
	var req=new XMLHttpRequest();
	req.open("GET", fname, true);
	req.responseType="arraybuffer";
	req.onload=function(e) {
	    if(this.status!=200) {
		console.log("file not found");
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
