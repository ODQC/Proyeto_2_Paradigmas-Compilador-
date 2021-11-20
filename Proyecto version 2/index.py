from flask import Flask, render_template, request
from flask.templating import DispatchingJinjaLoader

from AST import AssignCommand
import Compilador

from subprocess import check_output


app = Flask(__name__, static_folder="assets")
@app.route('/')
def principal():
     return render_template('index.html')

@app.route('/result', methods=['GET','POST'])
def result():

    text=""
    text = request.form.get('codigoText')
    content=text.splitlines()
    with open('test.txt', 'w') as f:
        for line in content:
           f.write(line)
           f.write('\n')

    compilar()

    #carga las lineas
    f1=open('mensaje.txt','r')
    if(f1.mode=='r'):
        mensajeC1=f1.read()

    f2=open('mensaje2.txt','r')
    if(f2.mode=='r'):
        mensajeC2=f2.read()

    f3=open('errores.txt','r')
    if(f3.mode=='r'):
        mensajeC3=f3.read()
        mensajeC4= mensajeC1+mensajeC3

    return render_template('index.html',code=text,errores=mensajeC4,arbolCodigo=mensajeC2)

def compilar():
    with open('mensaje2.txt', 'a') as f:
        f.flush()
        f.close()

    mensaje =[]
    f = 'test.txt'
    controlador= Compilador.Controlador(f)
    i= controlador.verificar_Archivo()
    if i ==1:
               
        archivo1 = open('errores.txt','w')
        archivo1.write('\n')
        archivo1.close()

        sc=Compilador.AnalizadorLexico
     
        Tokens = sc.verificar_Scanner(controlador.get_Archivo())
        sc.getReportErrors()
       
        if(sc.getReportErrors()==0):
            Tree = Compilador.Parser.iniciar_Parser(Tokens)
            if (Compilador.Parser.get_reportErrors() is True):
                
                mensaje1 ="\n==========================================================\n * Ejecutando Analisis semántico\n=========================================================="
                mensaje.append(mensaje1)
                print(mensaje1)
          
                visitor=Compilador.Checker.Checker()
                Compilador.Checker.Checker.check(Tree)
                
        
                archivo = open('mensaje2.txt','w')
                archivo.write('\n')
                archivo.close()
                impresion = Compilador.ImprimirArbol.ImprimirArbol(Tree)
                impresion.imprime_Arbol(Tree)
               
            else:
                mensaje3="--------------------------------------------------"
                mensaje.append(mensaje3)
                print(mensaje3)
                
        else:
            mensaje4 ="\n==========================================================\n  -- Se detectaron errores --\n ============================================="
            
            mensaje.append(mensaje4)
            print(mensaje4)
     

    with open('mensaje.txt', 'w') as f:
        for line in mensaje:
           f.write(line)
           f.write('\n')

 




            
def before_request():
    app.jinja_env.cache = {}
        
 



if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.before_request(before_request)
    app.run(use_reloader= True,debug=True, port =5000)