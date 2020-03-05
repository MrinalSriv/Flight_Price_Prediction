
//document.getElementById("submit_button").disabled = false;

function show_loading(){
    console.log("Show Loading")
    console.log(document.getElementById("upload_box"))
    if(document.getElementById("upload_box").value != "") {
   			// you have a file
   			document.getElementById('loading').show();
	}else{
		console.log("No FIle")
	}

}