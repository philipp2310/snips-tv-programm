flash_in = true;
flash_val = 40;
is_listening = false;

function start_listening(){
	is_listening = true;
	listening();
}

function listening(){
	if (is_listening == false){
		flash_in = false;
	}
	var list = document.getElementById("listening");
	if (flash_in){
		flash_val++;
		list.style.boxShadow  = "inset 0 0 "+flash_val+"VW 0VW #17D4FE";
		
		if(flash_val >= 40){
			flash_in = false;
		}
	} else {
		flash_val--;
		list.style.boxShadow  = "inset 0 0 "+flash_val+"VW 0VW #17D4FE";
		if(flash_val <= 0){
			flash_in = true;
			if(is_listening == false){
				return;
			}
		}
	}
    setTimeout(listening, 50);
    
}
