function Show_more(id)
{
	var url="/audio/musical/";
	new Ajax.Updater('div_more'+id, url, {method:'get',parameters: {id_mma:id} })
}
function Show_more_usr_obj(id)
{	
	var url="/users/object/more/";
	new Ajax.Updater('div_more'+id, url, {method:'get',parameters: {id:id} })
}
function Show_files(id)
{
	var url="/image/satimages/";
	new Ajax.Updater('div_more'+id, url, {method:'get',parameters: {multid:id} })
}

function Show_files2(id,cpt)
{
	if(cpt==1)
	{
		var url="/image/more/";
		new Ajax.Updater('div_more'+id, url, {method:'get',parameters: {id_mma:id} })
		$('button_show_files2_'+id).style.display= "None";
		$('button_unshow_files2_'+id).style.display= "block";
	}
	else
	{
		$('div_more'+id).innerHTML = "";
		$('button_show_files2_'+id).style.display= "block";
		$('button_unshow_files2_'+id).style.display= "None";
	}
}

function Show_codes(id,cpt)
{
	if(cpt ==1)
	{
		var url="/app/more/";
		var ajaxRequest = new Ajax.Request(
			url,{
				method : 'get',
				parameters: {id_algo:id},
				onComplete : DisplayResponse
			});
		function DisplayResponse(xhr){
			$('button_show_codes_'+id).style.display= "None";
			$('button_unshow_codes_'+id).style.display= "block";
			$('div_more'+id).innerHTML = xhr.responseText;
		}
	}
	else
	{
		$('button_show_codes_'+id).style.display= "block";
		$('button_unshow_codes_'+id).style.display= "none";
		$('div_more'+id).innerHTML = "";
	}	
}

function Change_order(val,url)
{
	var ajaxRequest = new Ajax.Request(
		url,{
			method : 'get',
			parameters: {id_ord:val},
			onSuccess : DisplayResponse
		});
	function DisplayResponse(xhr){
		$('content').innerHTML = xhr.responseText;
	}
	//new Ajax.Updater('content', url, {	method : 'get',parameters: {id_ord:val} })
}


function user_infos(log,id)
{
	var url="/navbar/user/"+log;
	new Ajax.Updater('INFOS', url, {method:'get',parameters: {id:id} })	;
}
function group_infos(id_gpe,id)
{
	var url="/navbar/group/"+id_gpe;
	new Ajax.Updater('INFOS', url, {method:'get',parameters: {id:id} })	;
}

function m_media(id_ens)
{
	var url="/util/upd/ef/";
	new Ajax.Updater('formodif'+id_ens, url, {method:'get',parameters: {id_ens:id_ens} })	;
}
function m_file(id_file)
{
	var url="/util/upd/m/"+id_file;
	new Ajax.Updater('file_modif_'+id_file, url, {method:'get',parameters: {id_file:id_file} })	;
}

function upd_biblio(log)
{
	var url="/util/upd/biblio/"+log;
	new Ajax.Updater('raiponce', url, {method:'get'});
}
function check_dates()
{
	var url="/util/check_dates/";
	new Ajax.Updater('raiponce', url, {method:'get'});
}