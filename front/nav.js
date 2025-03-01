// JavaScript Version
const buttonMenu = document.querySelector('#nav-mobile');
const navMenu = document.querySelector('.nav-menu');

buttonMenu.addEventListener('click', (e) => {
  e.currentTarget.classList.toggle('nav-open');
  navMenu.classList.toggle('open-menu');
});

// jQuery Version
// $(function() {
//     var btn_movil = $(‘#nav-mobile’),
//     menu = $(‘#menu’).find(‘ul’);

//     // Al dar click agregar/quitar clases que permiten el despliegue del menú
//     btn_movil.on(‘click’, function (e) {
//         e.preventDefault();
//         var el = $(this);
//         el.toggleClass(‘nav-active’);
//         menu.toggleClass(‘open-menu’);
//     });
// });


//operacion a realizar , llamado a la API
function op(api,id,clase) {

    //reseteo el panel de contenido
	Generales.mostrarPanelDerYOcultarClase(id,clase)
	
	//AQUI PONER AJAx,JQUERY o mejor FETCH .... para las llamadas asincronas a las apis*******************************************
	
    //llamo a la api y retorno los resultados,,,,, este es solo un ejemplo con jquery
    $.ajax({
		//url: 'http://localhost:43414/moodle/login/index.php?XDEBUG_SESSION_START=php2',
        url: api,
       // headers: { 'Authorization': "Bearer " + "mi autorizacino" },
        type: "GET",
        data: { "username": "mi usuario", "password": "", 'Authorization': 'miautorizacion' },
        async: true,
       // dataType: "html",
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        success: function (respuestaJson) {
            //porner el mensaje a mostrar en caso de exito en el html*****************************
   			alert(respuestaJson);

        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            //console.log("error en moodle url:", XMLHttpRequest, textStatus, errorThrown);
			
			//PONER el MENSAJE a mostrar en caso de error en el html**************************************
			alert(textStatus);
		}               
                        
    });
					
        
}    





