# SAMPLE 1
# --------
# from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow

# app = Flask(__name__)
# app.config ['SQLALCHEMY_DATABASE_URI']= 'sqlite:///notes.db'
# db = SQLAlchemy(app)
# ma = Marshmallow(app)                     

# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)
    
# class NoteSchema(ma.Schema):
#     class Meta:
#         fields = ["id","title","content"]

# note_schema= NoteSchema()
# notes_schema= NoteSchema(many=True)

# def sample():
#     note= Note(title="Hello", content="World!")
#     db.session.add(note)
#     db.session.commit()


# if __name__=="__main__":
#     with app.app_context():
#         db.create_all()
#         sample()
#     app.run(debug=True)

# ---------------





from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI']= 'sqlite:///notes.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)                     

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
class NoteSchema(ma.Schema):
    class Meta:
        fields = ["id","title","content"]

note_schema= NoteSchema()
notes_schema= NoteSchema(many=True)

@app.route("/api/notes", methods=["GET"])
def get_notes():
    all_notes= Note.query.all()
    response = notes_schema.dump(all_notes)
    return jsonify(response), 200

@app.route("/api/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    try:
        note = Note.query.get(note_id)
        if note:
            response = note_schema.dump(note)
            return jsonify(response), 200
        else:
            response = {
                "error": "Note not found"
            }
            return jsonify(response), 404
    except:
        response = {
            "error": "Invalid ID"
        }
        return jsonify(response), 400

@app.route("/api/notes", methods=["POST"])
def create_note():
    try:
        title = request.json["title"]
        content = request.json["content"]
        note = Note(title = title, content=content)
        db.session.add(note)
        db.session.commit()

        response = {
        "note_id": note.id,
        "message": "Successfully added note entry."
        }
        return jsonify(response), 201
    
    except:
        response = {
            "error": "Invalid Data"
        }
        return jsonify(response), 400

@app.route("/api/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    try:
        note = Note.query.get(note_id)
        if note:
            note.title =request.json["title"]
            note.content = request.json["content"]
            db.session.commit()

            response = {
                "note_id": note.id,
                "message" : "Succesfully updated note entry"
            }
            return jsonify(response), 202
        else:
            response = {
                "error" : "note that not exist"
            }
            return jsonify(response), 404
    except:
        response = {
            "error" : "Invalid data"
        }
        return jsonify(response), 402
    
@app.route("/api/notes/<int:note_id>/delete", methods=["DELETE"])
def delete_note(note_id):
    try:
        note = Note.query.get(note_id)
        if note:
            db.session.delete(note)
            db.session.commit()

            response = {
                "note_id": note.id,
                "message" : "Succesfully deleted"
            }
            return jsonify(response), 200
        else:
            response = {
                "error" : "note that not exist"
            }
            return jsonify(response), 404
    except:
        response = {
            "error" : "Invalid request"
        }
        return jsonify(response), 400


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)




























# def sample():
#     note= Note(title="Hello", content="World!")
#     db.session.add(note)
#     db.session.commit()


# if __name__=="__main__":
#     with app.app_context():
#         db.create_all()
#         sample()
#     app.run(debug=True)

