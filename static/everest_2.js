
//document.getElementById("submit_button").disabled = false;

function show_loading(){
    //console.log("Show Loading")
    //console.log(document.getElementById("upload_box").files.length)
    if (document.getElementById("upload_box")){
    	if(document.getElementById("upload_box").value != "") {
	   			// you have a file
	   			//document.getElementById('loading').show(); style.display='block'
	   			document.getElementById('loading').style.display='block';
	   			console.log("Showing _loading")
		}else{
			//console.log("No File")
		}	
    }
    else{
    	//console.log(":No file")
    }
    

}