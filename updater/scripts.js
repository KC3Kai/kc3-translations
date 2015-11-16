(function(){
	
	var EN_JSON = {};
	var XX_JSON = {};
	var NEW_JSON = {};
	var i;
	
	$(document).on("ready", function(){
		
		$("#lang_submit").on("click", function(){
			EN_JSON = JSON.parse($.ajax({
				async: false,
				url: "https://raw.githubusercontent.com/KC3Kai/kc3-translations/master/data/en/terms.json",
			}).responseText);
			
			for(i in EN_JSON){
				EN_JSON[i] = "*****"+EN_JSON[i];
			}
			
			XX_JSON = JSON.parse($.ajax({
				async: false,
				url: "https://raw.githubusercontent.com/KC3Kai/kc3-translations/master/data/"+$("#lang_code").val()+"/terms.json",
			}).responseText);
			
			NEW_JSON = $.extend(true, EN_JSON, XX_JSON);
			
			$("#newjson").val( JSON.stringify(NEW_JSON, null, "\t") );
			$("#newjson").css("background", "#dfd");
		});
		
		$(document).on("keyup", function(e){
			var NEWTL = $("#newjson").val();
			if(NEWTL==="") return true;
			try {
				JSON.parse(NEWTL);
				$("#newjson").css("background", "#dfd");
			}catch(ex){
				$("#newjson").css("background", "#fdd");
			}
		});
		
	});
	
})();
