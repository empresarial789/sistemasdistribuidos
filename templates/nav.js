// JavaScript Version
const buttonMenu = document.querySelector('#nav-mobile');
const navMenu = document.querySelector('.nav-menu');
const formularioAccess = '<form onSubmit="event.preventDefault();"><div><label for="username" style="display:inline-block; width: 100px;">Username</label><input id="username" type="text" name="username" /></div><div><label for="password" style="display:inline-block; width: 100px;">Password</label><input id="password" type="text" name="password" /></div><div id="statusLogin"></div><br/><button onclick="loginBasic()">Login</button></form >';
const formularioAccessAPIKEY = '<form onSubmit="event.preventDefault();"><div><label for="username2" style="display:inline-block; width: 100px;">Username</label><input id="username2" type="text" name="username2" /></div><div><label for="password2" style="display:inline-block; width: 100px;">Password</label><input id="password2" type="text" name="password2" /></div><div id="statusLogin2"></div><br/><button onclick="registerAPIKEY()">Registro</button><button onclick="getAPIKEY()">GetAPIKEY</button><button onclick="recursoAPIKEYprotegido()">AccesoARecurso</button></form >';
const formularioAccessJWT = '<form onSubmit="event.preventDefault();"><div><label for="username3" style="display:inline-block; width: 100px;">Username</label><input id="username3" type="text" name="username3" /></div><div><label for="password3" style="display:inline-block; width: 100px;">Password</label><input id="password3" type="text" name="password3" /></div><div id="statusLogin3"></div><br/><button onclick="getTOKENJWT()">Login</button><button onclick="recursoJWTprotegido()">AccesoARecurso</button></form >';


//const formularioAccessx = '<form action = "" method = "post" ><div><label for="username" style="display:inline-block; width: 100px;">Username</label><input id="username" type="text" name="username" /></div><div><label for="password" style="display:inline-block; width: 100px;">Password</label><input id="password" type="text" name="password" /></div><div><label for="rol" style="display:inline-block; width: 100px;">Rol</label><select id="rol" name="rol" ><option value="1">Admin</option><option value="2">Gestor</option><option value="3">Agente</option></select></div><br/><input type="submit" value="Save" /></form >';
var API_KEY;
var TOKEN_JWT;

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
            divMensajeStatus.innerHTML = 'API KEY';
            var contenido = document.getElementById('contenido3');
            contenido.innerHTML = formularioAccessAPIKEY;
            break;
        case API.endpoint4:
            divMensajeStatus.innerHTML = 'JWT TOKEN';
            var contenido = document.getElementById('contenido4');
            contenido.innerHTML = formularioAccessJWT;
            break;
        case API.endpoint5:
            console.log("Tengo un loro");
            break;
        default:
            console.log("No tengo mascota");
            break;
    }
			
        
}    

function loginBasic() {
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
            contenido.innerHTML = error.message;
        }); 


}
function registerAPIKEY() {
    var contenido = document.getElementById('statusLogin2');
    contenido.innerHTML = '';

    let username = document.getElementById("username2").value;
    let password = document.getElementById("password2").value;
    let headers = new Headers();
    headers.set('usuario', username);
    headers.set('password', password);
    headers.set('Content-Type', 'application/json');

    fetch(API.endpoint3, {
        method: 'POST',
        headers: headers 
    })
        .then(response => {
            /*if (!response.ok) {
                throw new Error('Network response was not ok');
            }*/
            return response.json();
        })
        .then(data => {
            var contenido = document.getElementById('statusLogin2');
            contenido.innerHTML = data.message;
            
        })
        .catch(error => {
            var contenido = document.getElementById('statusLogin2');
            contenido.innerHTML = error.message;
        });


}

function getAPIKEY() {
    var contenido = document.getElementById('statusLogin2');
    contenido.innerHTML = '';

    let username = document.getElementById("username2").value;
    let password = document.getElementById("password2").value;
    let headers = new Headers();
    headers.set('usuario', username);
    headers.set('password', password); 
    headers.set('Content-Type', 'application/json');

    fetch(API.endpoint31, {
        method: 'POST',
        headers: headers
    })
        .then(response => {
            /*if (!response.ok) {
                throw new Error('Network response was not ok');
            }*/
            return response.json();
        })
        .then(data => {
            var contenido = document.getElementById('statusLogin2');
            contenido.innerHTML = data.message;
            API_KEY = data.api_key;
        })
        .catch(error => {
            var contenido = document.getElementById('statusLogin2');
            contenido.innerHTML = error.message;
        });


}

function recursoAPIKEYprotegido() {
    var contenido = document.getElementById('statusLogin2');
    contenido.innerHTML = '';

    let username = document.getElementById("username2").value;
    let password = document.getElementById("password2").value;
    let headers = new Headers();
    headers.set('usuario', username);
    headers.set('password', password);
    headers.set('Content-Type', 'application/json');
    headers.set('X-API-KEY', API_KEY);

    fetch(API.endpoint32, {
        method: 'GET',
        headers: headers
    })
        .then(response => {
            /*if (!response.ok) {
                throw new Error('Network response was not ok');
            }*/
            return response.json();
        })
        .then(data => {
            var contenido = document.getElementById('statusLogin2');
            contenido.innerHTML = data.message;
        })
        .catch(error => {
            var contenido = document.getElementById('statusLogin2');
            contenido.innerHTML = error.message;
        });


}


//login jwt
function getTOKENJWT() {
    var contenido = document.getElementById('statusLogin3');
    contenido.innerHTML = '';

    let username = document.getElementById("username3").value;
    let password = document.getElementById("password3").value;
    let headers = new Headers();
    headers.set('usuario', username);
    headers.set('password', password);
    headers.set('Content-Type', 'application/json');
    
    fetch(API.endpoint4, {
        method: 'POST',
        headers: headers
    })
        .then(response => {
            /*if (!response.ok) {
                throw new Error('Network response was not ok');
            }*/
            return response.json();
        })
        .then(data => {
            var contenido = document.getElementById('statusLogin3');
            contenido.innerHTML = data.message;
            TOKEN_JWT = data.access_token;
        })
        .catch(error => {
            var contenido = document.getElementById('statusLogin3');
            contenido.innerHTML = error.message;
        });


}

function recursoJWTprotegido() {
    var contenido = document.getElementById('statusLogin3');
    contenido.innerHTML = '';

    let username = document.getElementById("username3").value;
    let password = document.getElementById("password3").value;
    let headers = new Headers();
    headers.set('usuario', username);
    headers.set('password', password);
    headers.set('Content-Type', 'application/json');
    headers.set('Authorization', 'Bearer ' + TOKEN_JWT);

    fetch(API.endpoint41, {
        method: 'GET',
        headers: headers
    })
        .then(response => {
            /*if (!response.ok) {
                throw new Error('Network response was not ok');
            }*/
            return response.json();
        })
        .then(data => {
            var contenido = document.getElementById('statusLogin3');
            contenido.innerHTML = data.message;
        })
        .catch(error => {
            var contenido = document.getElementById('statusLogin3');
            contenido.innerHTML = error.message;
        });


}


/**getTOKENJWT()">Login</button><button onclick="recursoJWTprotegido */




