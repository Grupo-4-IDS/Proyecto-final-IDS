from flask import Flask, jsonify, request, abort, send_file
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
    fecha_registro = db.Column(db.Date, nullable=False, default=db.func.current_date)