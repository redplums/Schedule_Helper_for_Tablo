// Display modified time for file scheduled.csv
document.querySelector("button.refresh").onclick = function () {
// Call python function
eel.refresh()(function(p){					
	// Update to display in browser
		document.querySelector(".refresh").outerHTML += "&nbsp" + p;
})
}


// Read config.txt file and display items
document.querySelector("button.Tablo_IP").onclick = function () {
// Call python function
eel.Tablo_IP()(function(reader){					
	// Update to display in browser
		document.querySelector(".Tablo_IP").outerHTML += "&nbsp" + reader;
})}

// Change Tablo IP Address in config.txt file
document.querySelector("button.change_IP").onclick = function () {var q = prompt("Enter IP Address for Tablo", "");
// Call python function
	document.querySelector(".keywords").innerHTML = "";
      document.querySelector(".keywords").innerHTML = "<p><li>Added: " + q + " for IP Address</li></p>";
	document.querySelector(".keywords").innerHTML = "<p><li>Added: " + q + " for IP Address</li></p>";
	eel.change_IP(q); location.reload()}



// Read keyword_search.csv file and display items
document.querySelector("button.view").onclick = function () {
// Call python function
document.querySelector(".keywords").innerHTML = "";
eel.keywords()(function(string){					
	for(var i=1; i <string.length; i++){
	// Update the div with a random number returned by python
		document.querySelector(".keywords").innerHTML += "<p>" + "&nbsp<button id='delete" + [i] + "' onclick='demoA()'>-</button>&nbsp" + string[i] + "</p>";
}
})
}


// Add new item to keyword_search.csv file
var add_new;
document.querySelector("button.add").onclick = function () {var y = prompt("Add Keyword", "");
// Call python function
	document.querySelector(".keywords").innerHTML = "";
	document.querySelector(".keywords").innerHTML += "<li>Choose type of programs for: " + y + 
		"</li>" + "<br><input type='radio' name='SHfT' id='series' value='series'>TV Series" + 
		"<br><input type='radio' name='SHfT' id='movie' value='movie'>Movies" + 
		"<br><input type='radio' name='SHfT' id='sports' value='sports'>Sports" + 
		"<br><input type='radio' name='SHfT' id='all' value='all'>All the above" + 
		"<br><button class='checkButton'> Submit </button><br><p></p>";
		    	document.querySelector("button.checkButton").onclick = function () {var k = document.querySelector('input[name="SHfT"]:checked');
      document.querySelector(".keywords").innerHTML = "<p><li>Added: " + y + " for category [" + k.value + "]</li></p>";
	eel.add_item(y, k.value);}
}

// Delete item from keyword_search.csv file after confirmation
var text;
function demoA () { var z = confirm("Continue with deletion?"); 
	if (z == true){
		document.querySelector(".keywords").innerHTML += "<li>" + event.target.id + "</li>";
		text = String([event.target.id]);
		text = text.slice(6);
		document.querySelector(".keywords").innerHTML += "<li>" + text + "</li>";
		document.querySelector(".keywords").innerHTML = "";
		eel.delete_item(text)(function(del_item){
			document.querySelector(".keywords").innerHTML += "<li>" + "Deleted: "+ del_item + "</li><br></br>";		
		})
} 	else {
		document.querySelector(".keywords").innerHTML += "<li>" + "OK" + "</li>";
	
}}

// Display rows in scheduled.csv to see what last search set to schedule
document.querySelector("button.sch_rec").onclick = function () {
// Call python function
document.querySelector(".keywords").innerHTML = "";
eel.scheduled()(function(string){					
	for(var i=1; i <string.length; i++){
	// Update the div with a random number returned by python
		document.querySelector(".keywords").innerHTML += "<p>" + string[i] + "</p>";
}
})
}

// Onclick of the button
document.querySelector("button.days").onclick = function () { document.querySelector(".keywords").innerHTML += "<li>Choose number of days to search schedule: </li>" + 
		"<input type='radio' name='SHfT' id='1' value='1'>1" + 
		"<br><input type='radio' name='SHfT' id='2' value='2'>2" + 
		"<br><input type='radio' name='SHfT' id='4' value='4'>4" + 
		"<br><input type='radio' name='SHfT' id='6' value='6'>6" + 
		"<br><input type='radio' name='SHfT' id='8' value='8'>8" +
		"<br><input type='radio' name='SHfT' id='10' value='10'>10" +
		"<br><input type='radio' name='SHfT' id='14' value='14'>14" +   
		"<br><button class='checkButton'> Submit </button><br><p></p>";
		    	document.querySelector("button.checkButton").onclick = function () {var n = document.querySelector('input[name="SHfT"]:checked');
      document.querySelector(".keywords").innerHTML = "<p><li>Number of Days to Search: " + n.value + "</li></p>";
	eel.num(n.value)};
//(function(string){for(var i=1; i <string.length; i++){					
//		})
//}	else {
//		document.querySelector(".keywords").innerHTML += "<li>" + "OK" + "</li>";
}

// Onclick of the button
document.querySelector("button.search").onclick = function () { var a = confirm("This may take several minutes");
// Call python function
	if (a == true){
		document.querySelector(".keywords").innerHTML = "";
		eel.search(); location.reload()
//(function(string){for(var i=1; i <string.length; i++){					
//		})
}	else {
		document.querySelector(".keywords").innerHTML += "<li>" + "OK" + "</li>";
}}

// Onclick of the button
document.querySelector("button.windows_sched").onclick = function () { var a = confirm("This will setup a task in MS Scheduler to run the program daily"); var t = prompt("What hour to run? [0-23]");
// Call python function
	if (a == true){
		document.querySelector(".keywords").innerHTML = "";
		eel.windows_sched(t); location.reload()
}	else {
		document.querySelector(".keywords").innerHTML += "<li>" + "OK" + "</li>";
}}


