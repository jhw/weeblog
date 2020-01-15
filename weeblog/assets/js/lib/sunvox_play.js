var Sunvox={    
    load: function(slot, fname) {
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
