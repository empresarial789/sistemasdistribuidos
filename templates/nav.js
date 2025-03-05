// JavaScript Version
const buttonMenu = document.querySelector('#nav-mobile');
const navMenu = document.querySelector('.nav-menu');
const formularioAccess = '<form onSubmit="event.preventDefault();"><div><label for="username" style="display:inline-block; width: 100px;">Username</label><input id="username" type="text" name="username" /></div><div><label for="password" style="display:inline-block; width: 100px;">Password</label><input id="password" type="password" name="password" /></div><div id="statusLogin"></div><br/><button onclick="loginBasic()">Login</button></form >';
const formularioAccessAPIKEY = '<form onSubmit="event.preventDefault();"><div><label for="username2" style="display:inline-block; width: 100px;">Username</label><input id="username2" type="text" name="username2" /></div><div><label for="password2" style="display:inline-block; width: 100px;">Password</label><input id="password2" type="password"  name="password2" /></div><div id="statusLogin2">Solo se admiten caracteres alfanumericos,_, <br/>password con minima longitud de 8</div><br/><button onclick="registerAPIKEY()">Registro</button><button onclick="getAPIKEY()">GetAPIKEY</button><button onclick="recursoAPIKEYprotegido()">AccesoARecurso</button></form >';
const formularioAccessJWT = '<form onSubmit="event.preventDefault();"><div><label for="username3" style="display:inline-block; width: 100px;">Username</label><input id="username3" type="text" name="username3" /></div><div><label for="password3" style="display:inline-block; width: 100px;">Password</label><input id="password3" type="password"  name="password3" /></div><div id="statusLogin3"></div><br/><button onclick="getTOKENJWT()">Login</button><button onclick="recursoJWTprotegido()">AccesoARecurso</button></form >';
const formularioAccessJWTROL = '<form onSubmit="event.preventDefault();"><div><label for="username4" style="display:inline-block; width: 100px;">Username</label><input id="username4" type="text" name="username4" /></div><div><label for="password4" style="display:inline-block; width: 100px;">Password</label><input id="password4" type="password"  name="password4" /></div><div id="statusLogin4"></div><br/><button onclick="getTOKENJWTROL()">Login</button><button onclick="recursoJWTprotegidoAdmin()">AccesoARecurso Admin</button><button onclick="recursoJWTprotegidoGestor()">AccesoARecurso Gestor</button><button onclick="recursoJWTprotegidoAgente()">AccesoARecurso Agente</button></form >';


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
            divMensajeStatus.innerHTML = 'TOKEN JWT';
            var contenido = document.getElementById('contenido4');
            contenido.innerHTML = formularioAccessJWT;
            
            break;
        case API.endpoint5:
            divMensajeStatus.innerHTML = 'BLOCKCHAIN';
            var contenido = document.getElementById('contenido5');
            contenido.innerHTML = "Registrando tarjeton en la BLOCKCHAIN";
            let headers2 = new Headers();
            headers2.set('Content-Type', 'application/json');
            headers2.set('Accept', 'application/json');

            fetch(API.endpoint5, {
                method: 'GET',
                headers: headers2
            })
                .then(response => {
                    /*if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }*/
                    return response.json();
                })
                .then(data => {
                    var contenido = document.getElementById('contenido5');
                    contenido.innerHTML = data.message;
                })
                .catch(error => {
                    var contenido = document.getElementById('contenido5');
                    contenido.innerHTML = data.message;
                });
            break;
        case API.endpoint6:
            divMensajeStatus.innerHTML = 'Restrict HTTP Methods';
            fetch(API.endpoint31, {
                method: 'GET'
            })
                .then(response => {
                    /*if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }*/
                    return response.json();
                })
                .then(data => {
                    var contenido = document.getElementById('contenido6');
                    contenido.innerHTML = data.message;
                })
                .catch(error => {
                });
            break;
        case API.endpoint7:
            divMensajeStatus.innerHTML = 'Input Validation';
            document.getElementById('contenido3').style.display = "inline"; 
            document.getElementById('contenido7').style.display = "none";
            var contenido = document.getElementById('contenido3');
            contenido.innerHTML = formularioAccessAPIKEY;
            break;
        case API.endpoint8:
            divMensajeStatus.innerHTML = 'Validate Content Types';
            let headers = new Headers();
            headers.set('Content-Type', 'text/plain');
            headers.set('Accept', 'application/json');

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
                    var contenido = document.getElementById('contenido8');
                    contenido.innerHTML = data.message;
                })
                .catch(error => {
                    var contenido = document.getElementById('contenido8');
                    contenido.innerHTML = data.message;
                });
            break;
        case API.endpoint9:
            divMensajeStatus.innerHTML = 'Management endpoint';
            var contenido = document.getElementById('contenido9');
            contenido.innerHTML = formularioAccessJWTROL;
            break;
        case API.endpoint10:
            divMensajeStatus.innerHTML = 'Error handling';
            fetch(API.endpoint10, {
                method: 'POST'
            })
                .then(response => {
                    /*if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }*/
                    return response.json();
                })
                .then(data => {
                    var contenido = document.getElementById('contenido10');
                    contenido.innerHTML = data.message;
                })
                .catch(error => {
                    var contenido = document.getElementById('contenido10');
                    contenido.innerHTML = data.message;
                });
            break;
        case API.endpoint11:
            divMensajeStatus.innerHTML = 'Audit logs';
            document.getElementById('contenido3').style.display = "inline";
            document.getElementById('contenido11').style.display = "none";
            var contenido = document.getElementById('contenido3');
            contenido.innerHTML = formularioAccessJWTROL;
            break;
        case API.endpoint12:
            divMensajeStatus.innerHTML = 'Security headers';
            document.getElementById('contenido3').style.display = "inline";
            document.getElementById('contenido12').style.display = "none";
            var contenido = document.getElementById('contenido3');
            contenido.innerHTML = formularioAccessJWTROL;
            break;
        case API.endpoint13:
            divMensajeStatus.innerHTML = 'CORS';
            document.getElementById('contenido1').style.display = "inline";
            document.getElementById('contenido13').style.display = "none";
            var contenido = document.getElementById('contenido1');
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
                    var contenido = document.getElementById('contenido1');
                    contenido.innerHTML = "Esta intentando acceder desde un dominio no permitido";
                });
            break;
        case API.endpoint14:
            divMensajeStatus.innerHTML = 'Sensitive Information in HTTP requests';
            document.getElementById('contenido1').style.display = "inline";
            document.getElementById('contenido14').style.display = "none";
            var contenido = document.getElementById('contenido1');
            contenido.innerHTML = "Los datos sensibles se transmiten en POST en el encabezado o el body y en GET solo por encabezado";
            break;
        case API.endpoint15:
            divMensajeStatus.innerHTML = 'HTTP return code';
            document.getElementById('contenido1').style.display = "inline";
            document.getElementById('contenido15').style.display = "none";
            var contenido = document.getElementById('contenido1');
            contenido.innerHTML = "Todas las peticiones responden con el codigo de estado correspondiente segun la respuesta";
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
        headers: headers, credentials: 'include' })
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

//login jwt + rol
function getTOKENJWTROL() {
    var contenido = document.getElementById('statusLogin4');
    contenido.innerHTML = '';

    let username = document.getElementById("username4").value;
    let password = document.getElementById("password4").value;
    let headers = new Headers();
    headers.set('usuario', username);
    headers.set('password', password);
    headers.set('Content-Type', 'application/json');

    fetch(API.endpoint9, {
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
            var contenido = document.getElementById('statusLogin4');
            contenido.innerHTML = data.message;
            TOKEN_JWT = data.access_token;
        })
        .catch(error => {
            var contenido = document.getElementById('statusLogin4');
            contenido.innerHTML = error.message;
        });


}

function recursoJWTprotegidoAdmin() {
    var contenido = document.getElementById('statusLogin4');
    contenido.innerHTML = '';

    let username = document.getElementById("username4").value;
    let password = document.getElementById("password4").value;
    let headers = new Headers();
    headers.set('usuario', username);
    headers.set('password', password);
    headers.set('Content-Type', 'application/json');
    headers.set('Authorization', 'Bearer ' + TOKEN_JWT);

    fetch(API.endpoint91, {
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
            var contenido = document.getElementById('statusLogin4');
            contenido.innerHTML = data.message;
        })
        .catch(error => {
            var contenido = document.getElementById('statusLogin4');
            contenido.innerHTML = error.message;
        });


}
function recursoJWTprotegidoGestor() {
    var contenido = document.getElementById('statusLogin4');
    contenido.innerHTML = '';

    let username = document.getElementById("username4").value;
    let password = document.getElementById("password4").value;
    let headers = new Headers();
    headers.set('usuario', username);
    headers.set('password', password);
    headers.set('Content-Type', 'application/json');
    headers.set('Authorization', 'Bearer ' + TOKEN_JWT);

    fetch(API.endpoint92, {
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
            var contenido = document.getElementById('statusLogin4');
            contenido.innerHTML = data.message;
        })
        .catch(error => {
            var contenido = document.getElementById('statusLogin4');
            contenido.innerHTML = error.message;
        });


}
function recursoJWTprotegidoAgente() {
    var contenido = document.getElementById('statusLogin4');
    contenido.innerHTML = '';

    let username = document.getElementById("username4").value;
    let password = document.getElementById("password4").value;
    let headers = new Headers();
    headers.set('usuario', username);
    headers.set('password', password);
    headers.set('Content-Type', 'application/json');
    headers.set('Authorization', 'Bearer ' + TOKEN_JWT);

    fetch(API.endpoint93, {
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
            var contenido = document.getElementById('statusLogin4');
            contenido.innerHTML = data.message;
        })
        .catch(error => {
            var contenido = document.getElementById('statusLogin4');
            contenido.innerHTML = error.message;
        });


}
/**getTOKENJWT()">Login</button><button onclick="recursoJWTprotegido */




