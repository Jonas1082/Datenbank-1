from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("recipes", lazy=True))

class GroceryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("grocery_items", lazy=True))

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Benutzer erfolgreich registriert"})
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # Anmelden erfolgreich
            return jsonify({"message": "Anmeldung erfolgreich"})
        return jsonify({"message": "Falsches Passwort oder Benutzername"})
    return render_template("login.html")

@app.route("/recipes")
def recipes():
    recipes = Recipe.query.all()
    return render_template("recipes.html", recipes=recipes)

@app.route("/recipe/<id>")
def recipe(id):
    recipe = Recipe.query.get(id)
    if recipe:
        return render_template("recipe.html", recipe=recipe)
    return jsonify({"message": "Rezept nicht gefunden"})

@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        user_id = request.form["user_id"]
        recipe = Recipe(title=title, description=description, ingredients=ingredients, instructions=instructions, user_id=user_id)
        db.session.add(recipe)
        db.session.commit()
        return jsonify({"message": "Rezept erfolgreich hinzugefügt"})
    return render_template("add_recipe.html")

@app.route("/grocery_items")
def grocery_items():
    grocery_items = GroceryItem.query.all()
    return render_template("grocery_items.html", grocery_items=grocery_items)

@app.route("/add_grocery_item", methods=["GET", "POST"])
def add_grocery_item():
    if request.method == "POST":
        name = request.form["name"]
        quantity = request.form["quantity"]
        user_id = request.form["user_id"]
        grocery_item = GroceryItem(name=name, quantity=quantity, user_id=user_id)
        db.session.add(grocery_item)
        db.session.commit()
        return jsonify({"message": "Einkaufsliste erfolgreich hinzugefügt"})
    return render_template("add_grocery_item.html")

if __name__ == "__main__":
    app.run(debug=True)