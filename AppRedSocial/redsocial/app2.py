from flask import Flask, render_template, request, redirect, url_for, session, Response, make_response
from flask_session import Session
import sqlite3
from functools import wraps


app = Flask(__name__)

# Función para crear la conexión a la base de datos y la tabla si no existe
def create_connection():
    connection = None
    try:
        connection = sqlite3.connect("RedSocial.db")
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tb_usuarios (
                codigoU INT primary key,
                cedula varchar(10),
                nombre varchar(50),
                usuario varchar(20),
                clave varchar(20),
                apellidoP varchar(50),
                apellidoS varchar(50),
                celular INT (8),
                correo varchar(25),
                fecha_nacimiento varchar(20),
                estado varchar(20),
                profesion varchar(50),
                cantante varchar(20),
                comida varchar(20),
                deporte varchar(20),
                signoZodiaco varchar(20),
                pasatiempo varchar(20)  
            )
        ''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS tb_publicaciones (
        id INTEGER PRIMARY KEY,
        comentario TEXT,
        archivo BLOB,
        tipo TEXT
        )
    ''')
        connection.commit()
        return connection  # Devolver la conexión creada
    except sqlite3.Error as e:
       
        #print("Conexión a la base de datos 'RedSocial.db y tabla 'tb_usuarios' creadas exitosamente o ya existentes")
        raise e
db_filename = "RedSocial.db"
# Funciones CRUD
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/conectarBase')
def conectarBase():
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tb_usuarios ORDER BY codigoU")
        usuarios = cursor.fetchall()
        #print(usuarios)
        connection.close()
        return render_template('registro_usuarios.html', usuarios=usuarios)
    except Exception as e:
        return f"An error occurred: {e}"

def es_credencial_valida(usuario, clave):
    # Realiza la consulta en tu base de datos para verificar las credenciales
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tb_usuarios WHERE usuario=? AND clave=?", (usuario, clave))
    usuario = cursor.fetchone()
    connection.close()
    
    return usuario is not None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        
        # Realiza la autenticación verificando si las credenciales coinciden
        if es_credencial_valida(usuario, clave):
            # Si las credenciales son válidas, redireccionar al menu
            return redirect(url_for('menus'))
        else:
            mensaje_error = "Credenciales inválidas. Por favor, intenta de nuevo."
            return render_template('login.html', error=mensaje_error)
    
    return render_template('login.html')

@app.route('/menu')
def menus():
    return render_template('menu.html')

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        codigoU = request.form['codigoU']
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        usuario = request.form['usuario']
        clave = request.form['clave']
        apellidoP = request.form['apellidoP']
        apellidoS = request.form['apellidoS']
        celular = request.form['celular']
        correo = request.form['correo']
        fecha_nacimiento = request.form['fecha_nacimiento']
        estado = request.form['estado']
        profesion = request.form['profesion']
        cantante = request.form['cantante']
        comida = request.form['comida']
        deporte = request.form['deporte']
        signoZodiaco = request.form['signoZodiaco']
        pasatiempo = request.form['cantante']
            
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tb_usuarios (codigoU, cedula, nombre, usuario, clave, apellidoP, apellidoS, celular, correo, fecha_nacimiento,"+ 
                        "estado, profesion, cantante, comida,deporte,signoZodiaco,pasatiempo) VALUES (?,?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                        (codigoU, cedula, nombre, usuario, clave, apellidoP, apellidoS, celular, correo, fecha_nacimiento, estado, profesion, cantante, comida,deporte,signoZodiaco,pasatiempo))
        connection.commit()
        connection.close()
        return redirect(url_for('conectarBase'))
    return render_template('agregar.html')

@app.route('/editar/<int:codigoU>', methods=['GET', 'POST'])
def editar_usuario(codigoU):
    connection = create_connection()
    cursor = connection.cursor()
    if request.method == 'POST':
        codigoU = request.form['codigoU']
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        usuario = request.form['usuario']
        clave = request.form['clave']
        apellidoP = request.form['apellidoP']
        apellidoS = request.form['apellidoS']
        celular = request.form['celular']
        correo = request.form['correo']
        fecha_nacimiento = request.form['fecha_nacimiento']
        estado = request.form['estado']
        profesion = request.form['profesion']
        cantante = request.form['cantante']
        comida = request.form['comida']
        deporte = request.form['deporte']
        signoZodiaco = request.form['signoZodiaco']
        pasatiempo = request.form['pasatiempo']
        cursor.execute("UPDATE tb_usuarios SET cedula=?, nombre=?, usuario=?, clave=?, apellidoP=?, apellidoS=?, celular=?, correo=?,"+ 
                        "fecha_nacimiento=?, estado=?, profesion=?, cantante=?, comida=?, deporte=?, signoZodiaco=?, pasatiempo=?  WHERE codigoU=?", 
                        (cedula, nombre, usuario, clave, apellidoP, apellidoS, celular, correo, fecha_nacimiento, estado, profesion, cantante, comida,deporte,signoZodiaco,pasatiempo, codigoU))
        connection.commit()
        connection.close()
        return redirect(url_for('conectarBase'))
    else:
        cursor.execute("SELECT * FROM tb_usuarios WHERE codigoU=?", (codigoU,))
        usuario = cursor.fetchone()
        connection.close()
        return render_template('editar.html', usuario=usuario)

@app.route('/eliminar/<int:codigoU>', methods=['POST', 'DELETE'])
def eliminar_usuario(codigoU):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tb_usuarios WHERE codigoU=?", (codigoU,))
    connection.commit()
    connection.close()
    return redirect(url_for('conectarBase'))

@app.route('/consultar')
def listar_usuario():
    cedula = request.args.get('cedula', '')
    codigoU = request.args.get('codigoU', '')
    connection = create_connection()
    cursor = connection.cursor()

    usuario = None

    if cedula:
        cursor.execute("SELECT * FROM tb_usuarios WHERE cedula=?", (cedula,))
    elif codigoU:
        cursor.execute("SELECT * FROM tb_usuarios WHERE codigoU=?", (codigoU,))

    usuarios = cursor.fetchall()

    cursor.execute("SELECT DISTINCT cedula FROM tb_usuarios")
    cedulas = cursor.fetchall()

    cursor.execute("SELECT DISTINCT codigoU FROM tb_usuarios")  # Fetch codigoU values
    codigoU = cursor.fetchall()  # Fetch codigoU values

    connection.close()
    return render_template('registro_usuarios.html', codigoU=codigoU, cedula=cedula, usuarios=usuarios, cedulas=cedulas)


# ...

@app.route('/publicaciones')
def listar_publicaciones():
    conn = sqlite3.connect('RedSocial.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_publicaciones")
    items = cursor.fetchall()
    conn.close()
    return render_template('publicaciones.html', items=items)

@app.route('/upload', methods=['POST'])
def upload():
    comentario = request.form['comentario']
    archivo = request.files['archivo']
    datos = archivo.read()
    tipo = archivo.mimetype

    conn = sqlite3.connect('RedSocial.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tb_publicaciones (comentario, archivo, tipo) VALUES (?, ?, ?)",
                   (comentario, datos, tipo))
    conn.commit()
    conn.close()

    return redirect(url_for('listar_publicaciones'))

@app.route('/media/<int:item_id>')
def get_media(item_id):
    conn = sqlite3.connect('RedSocial.db')
    cursor = conn.cursor()
    cursor.execute("SELECT archivo, tipo FROM tb_publicaciones WHERE id = ?", (item_id,))
    archivo, tipo = cursor.fetchone()
    conn.close()

    return archivo, {'Content-Type': tipo}


@app.route('/logout')
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
