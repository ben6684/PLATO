
function search_KW(KW)
{
	var url="/search/";
	new Ajax.Updater('INFOS', url, {method:'get',parameters: {id:id} })	;
}
function search()
{
	var v=$('search_text').getValue();
	var url="/search/";
	var ajaxRequest = new Ajax.Request(
		url,{
			method : 'get',
			parameters: {search:v},
		});
}
function plop()
{
	return $('search_text').getValue();
}