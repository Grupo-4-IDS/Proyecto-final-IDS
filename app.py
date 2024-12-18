from flask import Flask, jsonify, request, abort, render_template, send_file
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://proyecto4:1234@db:5432/recudadacion_fondos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    cuit_cuil = db.Column(db.String(20), nullable=False, unique=True)
    contrasena = db.Column(db.String(10), nullable=False)
    fecha_registro = db.Column(db.Date, nullable=False, default=db.func.current_date())

class Causa(db.Model):
    __tablename__ = 'causas'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text, nullable=False)
    meta = db.Column(db.Numeric(11, 2), nullable=False)
    monto_recaudado = db.Column(db.Numeric(12, 2), nullable=False, default=0)

class Donacion(db.Model):
    __tablename__ = 'donaciones'
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Numeric(11, 2), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_causa = db.Column(db.Integer, db.ForeignKey('causas.id'), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/usuarios.html')
def usuarios():
    return render_template('usuarios.html')

@app.route('/usuarios', methods=['POST'])
def registrar_usuario():
    data = request.json
    if not data or 'usuario' not in data or 'email' not in data or 'cuit_cuil' not in data:
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    
    nuevo_usuario = Usuario(
        usuario=data['usuario'],
        email=data['email'],
        cuit_cuil=data['cuit_cuil'],
        contrasena=data.get('contrasena', '1234')  
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"id": nuevo_usuario.id, "mensaje": "Usuario creado con exito"}), 201

@app.route('/causas.html')
def causas():
    return render_template('causas.html')


@app.route('/causas', methods=['GET'])
def listar_causas():
    causas = Causa.query.all()
    respuesta = []
    for causa in causas:
        respuesta.append({
            "id": causa.id,
            "descripcion": causa.descripcion,
            "meta": float(causa.meta),
            "monto_recaudado": float(causa.monto_recaudado)
        })
    return jsonify(respuesta)

@app.route('/causas', methods=['POST'])
def crear_causa():
    data = request.json
    if not data or 'descripcion' not in data or 'meta' not in data:
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    
    nueva_causa = Causa(
        descripcion=data['descripcion'],
        meta=data['meta'],
        monto_recaudado=0
    )
    db.session.add(nueva_causa)
    db.session.commit()
    return jsonify({"id": nueva_causa.id, "mensaje": "Causa creada con éxito"}), 201

@app.route('/donaciones.html')
def donaciones():
    return render_template('donaciones.html')

    
@app.route('/donaciones', methods=['POST'])
def registrar_donacion():
    data = request.json
    if not data or 'monto' not in data or 'id_usuario' not in data or 'id_causa' not in data:
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    
    nueva_donacion = Donacion(
        monto=data['monto'],
        id_usuario=data['id_usuario'],
        id_causa=data['id_causa']
    )
    causa = Causa.query.get(data['id_causa'])
    if not causa:
        return jsonify({"error": "La causa no existe"}), 404
    
    causa.monto_recaudado += data['monto']
    db.session.add(nueva_donacion)
    db.session.commit()
    return jsonify({"id": nueva_donacion.id, "mensaje": "Donación registrada con exito"}), 201

@app.errorhandler(404)
def error_404(error):
    return send_file('templates/error.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)