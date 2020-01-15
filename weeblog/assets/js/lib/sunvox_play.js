/*
  sv_play_from_beginning(0);
  sv_stop(0);
*/

var Sunvox={    
    load: function(slot, fname) {
	console.log("loading "+fname+" in slot "+slot);
	var loadFromArrayBuffer=function(buf) {
	    if (buf) {
		var byteArray=new Uint8Array(buf);
		if (sv_load_from_memory(slot, byteArray)==0) {
		    console.log("song loaded");

		} else {
		    console.log("song load error");
		}
	    }
	};
	var req=new XMLHttpRequest();
	req.open("GET", fname, true);
	req.responseType="arraybuffer";
	req.onload=function(e) {
	    if(this.status!=200) {
		console.log("file not found");
		return;
            }
            var arrayBuffer=this.response;
            loadFromArrayBuffer(arrayBuffer);
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
    sv_open_slot(0);
});
