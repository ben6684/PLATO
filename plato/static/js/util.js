
function plop(id){alert("plop"+id);}

function KC()
{
	if ( window.addEventListener ) {
		var kkeys = [], konami = "38,38,40,40,37,39,37,39,66,65";
		window.addEventListener("keydown", function(e){
			kkeys.push( e.keyCode );
			if ( kkeys.toString().indexOf( konami ) >= 0 ) {
				/*ici mettre ce que l'on veux !*/
				alert('PLATO is watching you');
				window.location = "http://137.194.132.6:8000/wiki/petitpas/";
			}
		}, true);
	}
}
function showIm(f,name_demo):
{
	var url="/demos/"+name_demo;
	new Ajax.Updater('show_selection_input', url, {method:'get',parameters: {filename:f} })
}

