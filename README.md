# **Proyecto 2**
**Curso:** Tópicos Especiales en Telemática <br>
**Título:** Diseño e Implementación de un Autoscailing con el SDK de aws <br>
**Estudiantes** Andrés Echeverri Jaramillo, Salomón Vélez Pérez, Jose Manuel Fonseca<br>
### **1. Descripción**
Este proyecto se realizo en python implementando dos metodos, el controller que se encargaba de la gestion de las maquinas de aws y el registro de las instacias creadas y el monitoring el cual se encarga de simular el incremento de trabajo de la cpu de la instancia

### **3. Diseño**
Ver el .jpg adjunto en el github con el nombre de "Arquitectura.jpg" <br />

### **4. Requerimientos**
Para correr este proyecto se necesita tener python 3 instalado, una cuenta de AWS a la cual conectarse y hacer el import de las librerias mencionadas a continuacion para la ejecucion del codigo<br />

### **5. Análisis**
 Este proyecto esta hecho para simular como funciona un Autoscailing group de AWS, atraves esto se hara atraves de la libreria boto3 que permite comunicarse al SDK (Kit de desarrollo de software) de AWS para poder controlar las instancias EC2 de una cuenta, ademas se hara uso de llamados gRPC para la comunicacion de las maquinas creadas y el controlador de estas. <br />

### **6. Guía de uso (En local)**
Para poder correr el codigo primero se tendra que importar las librerias de python de boto3, awscli, grpc y grpcio-tools, esto se lograra con los siguientes comandos <br />
sudo apt-get update<br />
sudo apt-get upgrade<br />
sudo apt-get install python3<br />
sudo apt-get install python3-pip<br />
sudo python3 -m pip install grpcio<br />
sudo python3 -m pip install grpcio-tools<br />
sudo python3 -m pip install boto3<br />
sudo python3 -m pip install awscli<br />

ya con esto se podra correr el controler solo falta iniciar el laboratorio de aws y en la linea de codigo del controller 18-22 cambiar los string por la informacion que salga en aws details y luego en awscli<br />
Tras esto vamos a crear una instancia EC2 y le vamos a asigar un un security group con libre acceso a http, ssh en el puerto 8080, ademas vamos a asignar un .pem que vamos a descargar en la carpeta src de controler.<br />
En detalles avanzados en user_data vamos a poner lo siguiente <br />
#!/bin/bash
sudo apt-get -y update<br />
sudo apt-get -y upgrade<br />
sudo apt-get install -y python3<br />
sudo apt-get install -y python3-pip<br />
sudo python3 -m pip install grpcio<br />
sudo python3 -m pip install grpcio-tools<br />
sudo git clone https://github.com/jmfonsecap/Pruebitas.git<br />
cd Pruebitas/grpc/<br />
sudo python3 monitoring.py <br />
Con esta instancia cremos un launch template y ponemos su id en el el string de la linea 25, ademas de cambiar la el string de la linea 37 por el nombre de la llave de la instancia y ya se corre el archivo controler en la maquina local, si se quiere correr en aws se haria el mismo proceso pero se tendria que hacer una maquina diferente para el controller<br />
### **8. log**
Aca guardamos el registro de todo el proceso es en un txt que se llama archivo.txt.<br />