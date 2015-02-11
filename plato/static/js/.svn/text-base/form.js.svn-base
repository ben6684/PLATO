
function n_algo()
{
	var url = "/add_publi/";
	var ajaxRequest = new Ajax.Request(
		url,
		{	method : 'get',
			parameters: {n_algo:'1'},
			onComplete : DisplayResponse
		});	
	function DisplayResponse (xhr){
		$('add_algo').style.display= "table-row-group";
		$('add_algo').innerHTML = xhr.responseText;
	}	
}

function publi_code(ntool)
{
	if(!ntool){
		ntool = -1;
	}
	var url = "/add_app/publi_code/";
	var ajaxRequest = new Ajax.Request(
		url,
		{	method : 'get',
			parameters: {publi:ntool},
			onComplete : DisplayResponse
		});	
	function DisplayResponse (xhr){
		$('publicode').style.display= "table-row-group";
		$('publicode').innerHTML = xhr.responseText;
	}
	
}

function demo_code(ntool)
{
	if(!ntool){
		ntool = -1;
	}
	var url = "/add_app/demo_code/";
	var ajaxRequest = new Ajax.Request(
		url,
		{	method : 'get',
			parameters: {demo:ntool},
			onComplete : DisplayResponse
		});	
	function DisplayResponse (xhr){
		$('democode').style.display= "table-row-group";
		$('democode').innerHTML = xhr.responseText;
	}
	
}


function ensfile_code(ntool)
{
	if(!ntool){
		ntool = -1;
	}
	var url = "/add_app/ensfile_code/";
	var ajaxRequest = new Ajax.Request(
		url,
		{	method : 'get',
			parameters: {ensfile:ntool},
			onComplete : DisplayResponse
		});	
	function DisplayResponse (xhr){
		$('ensfilecode').style.display= "table-row-group";
		$('ensfilecode').innerHTML = xhr.responseText;
	}
	
}

function ensfile_publi(npubli)
{
	if(!npubli){
		npubli = -1;
	}
	var url = "/add_publi/ensfile_publi/";
	var ajaxRequest = new Ajax.Request(
		url,
		{	method : 'get',
			parameters: {ensfile:npubli},
			onComplete : DisplayResponse
		});	
	function DisplayResponse (xhr){
		$('ensfilepubli').style.display= "table-row-group";
		$('ensfilepubli').innerHTML = xhr.responseText;
	}
	
}

function add_author_to_list(text,li)
{
	//ici on peut faire appelle a une focntion qui va chercherr les auteurs ? 
	// et remplit un div editable ! (un peu comme django-selectable)
	$('author').innerHTML = li.innerHTML;
}

function new_article(id_page,id)
{
	r=confirm("are you sure you want to delete the article linked to this publication ?");
	if(r==true)
	{
		var url = "/add_publi/del_article/"+id_page;
		var ajaxRequest = new Ajax.Request(
			url,
			{	method : 'get',
				parameters: {id:id},
				onComplete : DisplayResponse
			});	
		function DisplayResponse (xhr){
			$('change_article').innerHTML= "<input type='file' name='form_page-article' id='id_form_page-article' />";
		}
	}
}
function new_prez(id_page,id)
{
	r=confirm("are you sure you want to delete the presentation linked to this publication ?");
	if(r==true)
	{
		var url = "/add_publi/del_prez/"+id_page;
		var ajaxRequest = new Ajax.Request(
			url,
			{	method : 'get',
				parameters: {id:id},
				onComplete : DisplayResponse
			});	
		function DisplayResponse (xhr){
			$('change_prez').innerHTML= "<input type='file' name='form_page-prez' id='id_form_page-prez' />";
		}
	}
}
function new_files(id_page,id)
{	
	r=confirm("are you sure you want to delete the file linked to this publication ?");
	if(r==true)
	{
		var url = "/add_publi/del_file/"+id_page;
		var ajaxRequest = new Ajax.Request(
			url,
			{	method : 'get',
				parameters: {id:id},
				onComplete : DisplayResponse
			});	
		function DisplayResponse (xhr){
			$("change_file_"+id).innerHTML = "";
		}
	}
}
function new_files_algo(id)
{	
	r=confirm("are you sure you want to delete the files linked to this source code?");
	if(r==true)
	{
		var url = "/add_app/del_file/";
		var ajaxRequest = new Ajax.Request(
			url,
			{	method : 'get',
				parameters: {id:id},
				onComplete : DisplayResponse
			});	
		function DisplayResponse (xhr){
			$("change_files_"+id).innerHTML = "";
		}
	}
}
function new_files_demo(id)
{	
	r=confirm("are you sure you want to delete the example linked to this demo?");
	if(r==true)
	{
		var url = "/demo/del/";
		var ajaxRequest = new Ajax.Request(
			url,
			{	method : 'get',
				parameters: {id:id},
				onComplete : DisplayResponse
			});	
		function DisplayResponse (xhr){
			$("change_files_"+id).innerHTML = xhr.responseText;
		}
	}
}


////////////////////////NEW FUNCTION FOR NEW DATABASE /////

function show_ensfile(id)
{
	var url = "/add_data/add_files/";
	var ajaxRequest = new Ajax.Request(
		url,
		{	method : 'get',
			parameters: {tef:id},
			onComplete : DisplayResponse
		});	
	function DisplayResponse (xhr){
		$('ensfile').style.display= "table-row-group";
		$('ensfile').innerHTML = xhr.responseText;
	}	
}

function show_complementary(id)
{
	var url = "/add_data/more/";
	var ajaxRequest = new Ajax.Request(
		url,
		{	method : 'get',
			parameters: {type:id},
			onComplete : DisplayResponse
		});	
	function DisplayResponse (xhr){
		$('more').style.display= "table-row-group";
		$('more').innerHTML = xhr.responseText;
	}	
}

function show_all_f(id)
{
	var url = "/add_data/add_new_files/";
	var ajaxRequest = new Ajax.Request(
		url,
		{	method : 'get',
			parameters: {allf:id},
			onComplete : DisplayResponse
		});	
	function DisplayResponse (xhr){
		$('allf').style.display= "table-row-group";
		$('allf').innerHTML = xhr.responseText;
	}	
}


///////// Try to show image before upload for legende /////////


///// SOME INTERESTING LINE NOT USED /////////
	// $$('div.prev_img')[0].insert(i)//objectUrl+'<br>'
	// $$('div.prev_img')[0].insert(fileList.length)//objectUrl+'<br>'
	//$('test').insert('<img src="' + objectUrl + '" />');
    // get rid of the blob
    //window.URL.revokeObjectURL(fileList[i]);


function previmg(input){
	var fileList = input.files;
	var anyWindow = window.URL || window.webkitURL;
	$('img_preview').innerHTML="";
    for(var i = 0; i < fileList.length; i++){
		var total_type = fileList[i].type;
		var type = total_type.split("/")[0]
		if (type=="image"){
			//get a blob to play with
			var objectUrl = anyWindow.createObjectURL(fileList[i]);
			// for the next line to work, you need something class="preview-area" in your html
			$('img_preview').insert('<tr><td></td><td>'+fileList[i].name +'<img height="50px" src="' + objectUrl + '" /><input id="id_legende_'+i+'" maxlength="2000" type="text" name="legende_'+i+'" size="20"></td></tr>')
		}
		else
		{
			$('img_preview').insert('<tr><td></td><td>'+fileList[i].name +'<input id="id_legende_'+i+'" maxlength="2000" type="text" name="legende_'+i+'" size="20"></td></tr>')
		}
	}
	
	window.URL.revokeObjectURL(fileList)
}


function previmg_demo(input,id){
	var fileList = input.files;
	var anyWindow = window.URL || window.webkitURL;
	$('img_preview'+id).innerHTML="";
    for(var i = 0; i < fileList.length; i++){
		var total_type = fileList[i].type;
		var type = total_type.split("/")[0]
		if (type=="image"){
			//get a blob to play with
			var objectUrl = anyWindow.createObjectURL(fileList[i]);
			// for the next line to work, you need something class="preview-area" in your html
			$('img_preview'+id).insert('<img height="150px" src="' + objectUrl + '" />')
		}
		else
		{
			$('img_preview'+id).insert(fileList[i].name)
		}
	}
	
	window.URL.revokeObjectURL(fileList)
}
