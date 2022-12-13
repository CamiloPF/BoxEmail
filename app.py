from pickletools import string4
from flask import Flask, render_template, request
import hashlib
import controlador
from datetime import datetime
import envioemail

app = Flask(__name__)

email_origen=" "

@app.route("/")
def hello_world():
    return render_template("login.html")

@app.route("/validarUsuario", methods=['GET','POST'])
def validarUsuario():
    if request.method=="POST":
        usu=request.form["txtusuario"]
        passw=request.form["txtpass"]
        passw2=passw.encode()
        passw2=hashlib.sha384(passw2).hexdigest()

        respuesta=controlador.validar_usuario(usu,passw2)
        global email_origen
        
        if len(respuesta)==0:
            email_origen=""
            mensaje = "ERROR DE AUTENTICACION!!!  Verifique sus datos"
            return render_template("informacion.html",datas=mensaje) 
        else:
            email_origen=usu
        #print("suruario= "+usu)
        #print("password= "+passw)
        #print("password incriptado= "+passw2)
            respuesta2=controlador.lista_destinatarios(usu)
            return render_template("principal.html", datas=respuesta2)   

@app.route("/registrarUsuario", methods=['GET','POST'])
def registrarUsuario():
    if request.method=="POST":
        nombre=request.form["txtnombre"]
        email=request.form["txtusuario2registro"]
        passw=request.form["txtpassregistro"]

        passw2=passw.encode()
        passw2=hashlib.sha384(passw2).hexdigest() #encriptador

        codigo=datetime.now()
        codigo2=str(codigo)
        codigo2=codigo2.replace("-","")
        codigo2=codigo2.replace(" ","")
        codigo2=codigo2.replace(":","")
        codigo2=codigo2.replace(".","")

        print(codigo2)
        
        envioemail.enviar(email,codigo2)

        respuesta=controlador.registrar_usuario(nombre,email,passw2,codigo2)
       
        mensaje = "El Usuario" + " " +nombre+" se ha registrado satisfactoriamente."
        return render_template("informacion.html",datas=mensaje) 


@app.route("/enviarMAIL", methods=["GET","POST"])
def enviarMAIL():
    if request.method=="POST":
        emailDestino=request.form["emailDestino"]
        asunto=request.form["asunto"]
        mensaje=request.form["mensaje"]
        
        controlador.registrar_mail(email_origen, emailDestino, asunto, mensaje)
        
        mensaje2="Sr Usuario, ud recibió un mensaje nuevo, por favor ingrese a la plataforma y verifique su Email en la pestaña Historial. \n\n Muchas Gracias!!!"
        envioemail.enviar(emailDestino,mensaje2,"Nuevo Mensaje Enviado")
        return "Email Enviado Satisfactoriamente"
    
    
@app.route("/actualizacionPassword", methods=['GET','POST'])
def actualizacionpassword():
    if request.method=="POST":
        pass1=request.form["pass"]
        passw2=pass1.encode()
        passw2=hashlib.sha384(passw2).hexdigest() #encriptador
        controlador.actualizarpass(passw2, email_origen)
        
        return "Actualizacion de Password Satisfactoria"

@app.route("/activarUsuario", methods=['GET','POST'])
def activarUsuario():
    if request.method=="POST":
        codigo=request.form["txtcodigo"]
        respuesta=controlador.activar_usuario(codigo)
        
        if len(respuesta)==0:
            mensaje= "El código de activación es erroneo, verifíquelo."
        else: 
            mensaje= "El usuario se ha activado exitosamente."
       
        return render_template("informacion.html",datas=mensaje) 
         
         
 
@app.route("/HistorialEnviados", methods=['GET','POST'])
def HistorialEnviados():
    resultado=controlador.ver_enviados(email_origen)
    return render_template("respuesta.html",datas=resultado)           

@app.route("/HistorialRecibidos", methods=['GET','POST'])
def HistorialRecibidos():
    resultado=controlador.ver_recibidos(email_origen)
    return render_template("respuesta.html",datas=resultado)