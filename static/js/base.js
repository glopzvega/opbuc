var getUrlVars = function () {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

let monedaFormatter = function(value){
	let params = {style: 'currency', currency: 'MXN'};
	return Number(value).toLocaleString('es-MX', params);
}