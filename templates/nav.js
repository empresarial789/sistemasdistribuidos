// JavaScript Version
const buttonMenu = document.querySelector('#nav-mobile');
const navMenu = document.querySelector('.nav-menu');
const formularioAccess = '<form onSubmit="event.preventDefault();"><div><label for="username" style="display:inline-block; width: 100px;">Username</label><input id="username" type="text" name="username" /></div><div><label for="password" style="display:inline-block; width: 100px;">Password</label><input id="password" type="text" name="password" /></div><div id="statusLogin"></div><br/><button onclick="login()">Login</button></form >';
//const formularioAccessx = '<form action = "" method = "post" ><div><label for="username" style="display:inline-block; width: 100px;">Username</label><input id="username" type="text" name="username" /></div><div><label for="password" style="display:inline-block; width: 100px;">Password</label><input id="password" type="text" name="password" /></div><div><label for="rol" style="display:inline-block; width: 100px;">Rol</label><select id="rol" name="rol" ><option value="1">Admin</option><option value="2">Gestor</option><option value="3">Agente</option></select></div><br/><input type="submit" value="Save" /></form >';
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
var divMensajeStatus = document.getElementById('divMensajeStatus');
function op(api,id,clase) {

    //reseteo el panel de contenido
	Generales.mostrarPanelDerYOcultarClase(id,clase)
    divMensajeStatus.innerHTML = '';

    //dependiendo de la api hago una cosa u otra
    switch (api) {
        case API.endpoint1:
            divMensajeStatus.innerHTML = 'HTTPS';            
            fetch(api)
                .then(response => {
                    /*if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }*/
                    return response.json();
                })
                .then(data => {
                    var contenido = document.getElementById('contenido1');
                    contenido.innerHTML = data.message;
                })
                .catch(error => {
                    // Handle errors
                    //console.error('Fetch Error :-S', error);
                });
            break;
        case API.endpoint2:
            divMensajeStatus.innerHTML = 'Access Control';
            var contenido = document.getElementById('contenido2');
            contenido.innerHTML = formularioAccess;
            break;
        case API.endpoint3:
            console.log("Tengo un gato");
            break;
        case API.endpoint4:
            console.log("Tengo una serpiente");
            break;
        case API.endpoint5:
            console.log("Tengo un loro");
            break;
        default:
            console.log("No tengo mascota");
            break;
    }

	//AQUI PONER AJAx,JQUERY o mejor FETCH .... para las llamadas asincronas a las apis*******************************************
	
    //llamo a la api y retorno los resultados,,,,, este es solo un ejemplo con jquery
    /*$.ajax({
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
   			

        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            //console.log("error en moodle url:", XMLHttpRequest, textStatus, errorThrown);
			
			//PONER el MENSAJE a mostrar en caso de error en el html**************************************
			
		}               
                        
    });*/
					
        
}    

function login() {
    var contenido = document.getElementById('statusLogin');
    contenido.innerHTML = '';
    
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let headers = new Headers();
    headers.set('Authorization', 'Basic ' + btoa(username + ":" + password));
    headers.set('X-Requested-With', 'XMLHttpRequest');

    fetch(API.endpoint2,{method:'GET',
        headers: headers, /*credentials: 'user:passwd'*/  credentials: 'include' })
        .then(response => {
            /*if (!response.ok) {
                throw new Error('Network response was not ok');
            }*/
            return response.json();
        })
        .then(data => {
            var contenido = document.getElementById('statusLogin');
            contenido.innerHTML = data.message;
        })
        .catch(error => {
            var contenido = document.getElementById('statusLogin');
            contenido.innerHTML = "Usuario invalido";
        }); 


}






