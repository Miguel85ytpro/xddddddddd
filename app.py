from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'clave_secreta_ecologica'

# Conexión a MongoDB Atlas
MONGO_URI = "mongodb+srv://Miguel85ytpro5_db_user:Carcam010@cluster0.iifnlr9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['fruteria_los_papus']
usuarios_col = db['usuarios']
frutas_col = db['frutas']

@app.route("/")
def index():
    if 'user' in session:
        return redirect(url_for('almacen'))
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u = request.form.get('usuario')
        p = request.form.get('password')
        # Validación contra la base de datos central
        user = usuarios_col.find_one({"usuario": u, "password": p})
        if user:
            session['user'] = u
            return redirect(url_for('almacen'))
        error = "Credenciales incorrectas. Intente de nuevo."
    return render_template("iniciar_sesion.html", error=error)

@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        u = request.form.get('usuario')
        p = request.form.get('password')
        if u and p:
            if not usuarios_col.find_one({"usuario": u}):
                usuarios_col.insert_one({"usuario": u, "password": p})
                return redirect(url_for('login'))
            return "El usuario ya existe", 400
    return render_template("formulario.html")

@app.route("/almacen")
def almacen():
    if 'user' not in session:
        return redirect(url_for('login'))
    # Consulta compartida para todos los trabajadores
    inventario = list(frutas_col.find())
    return render_template("gestor_tareas.html", productos=inventario)

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)