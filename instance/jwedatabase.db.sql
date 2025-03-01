BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "roles" (
	"idRol"	INTEGER,
	"nombreRol"	CHAR(15) NOT NULL UNIQUE,
	PRIMARY KEY("idRol")
);
CREATE TABLE IF NOT EXISTS "tarjetones" (
	"idTarjeton"	INTEGER,
	"fechaAlta"	CHAR(30) NOT NULL,
	"idVehiculo"	INTEGER NOT NULL,
	PRIMARY KEY("idTarjeton")
);
CREATE TABLE IF NOT EXISTS "usuarios" (
	"idUsuario"	INTEGER,
	"username"	CHAR(40) NOT NULL UNIQUE,
	"password"	CHAR(40) NOT NULL,
	"idRol"	INTEGER NOT NULL,
	PRIMARY KEY("idUsuario")
);
CREATE TABLE IF NOT EXISTS "vehiculos" (
	"idVehiculo"	INTEGER,
	"dominio"	CHAR(25) NOT NULL UNIQUE,
	"segmento"	CHAR(25) NOT NULL,
	"marca"	CHAR(25) NOT NULL,
	"modelo"	CHAR(60) NOT NULL,
	"motor"	CHAR(25) NOT NULL,
	"chasis"	CHAR(25) NOT NULL,
	"año"	CHAR(25) NOT NULL,
	PRIMARY KEY("idVehiculo")
);
COMMIT;
