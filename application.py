import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

# Applikáció konfigurálása
app = Flask(__name__)

# Automatikus újratöltés
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Cache-ek törlése
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Adatbázis felkonfigurálása
db = SQL("sqlite:///history.db")

# Feladatok felkonfigurálása
feladat1 = "Adj egy puszit xyz-nek"
feladat2 = "Adj két puszit xyz-nek"
feladat3 = "Adj három puszit xyz-nek"
feladat4 = "Adj négy puszit xyz-nek"
feladat5 = "Adj öt puszit xyz-nek"

# Jutalmak felkonfigurálása
jutalom1 = "Kapsz egy puszit xyz-től"
jutalom2 = "Kapsz két puszit xyz-től"
jutalom3 = "Kapsz három puszit xyz-től"
jutalom4 = "Kapsz négy puszit xyz-től"
jutalom5 = "Kapsz öt puszit xyz-től"

# Képek a feladathoz és a jutalomhoz
kepf1 = "1.png"
kepf2 = "2.jpg"
kepf3 = "3.jpg"
kepf4 = "4.jpg"
kepf5 = "5.jpg"
kepf6 = "6.jpg"
kepj11 = "11.jpg"
kepj12 = "12.jpg"
kepj13 = "13.jpg"
kepj14 = "14.jpg"
kepj15 = "15.jpg"
kepek = os.path.join('static', 'kepek')
app.config['kepekossz'] = kepek

# Globális változók
global helyzet
global név


@app.route("/")
def index():
    """A játék kezdőképernyője"""
    global helyzet
    helyzet = 0
    return render_template("index.html")


@app.route("/feladat", methods=["GET", "POST"])
def feladat():
    """A feladatok leírása"""
    global név
    global helyzet
    # A képek bekonfigurálása
    eleres = os.path.join(app.config['kepekossz'], eval('kepf'+str((helyzet+1))))
    # Ha az első kör, akkor alaphelyzetbe állítja a rendszert
    if helyzet == 0:
        helyzet = 1
        név = request.form.get("username")
    # Egyébként vegye a következő feladatot
    else:
        helyzet = helyzet + 1
    # Ha teljesítette a 10. szintet, akkor irányítsa a győzelmi felületre
    if helyzet == 6:
        return render_template("win.html", név=név)
    return render_template("feladat.html", név=név, feladat=eval('feladat'+str(helyzet)), hányadik=helyzet, kepf=eleres)


@app.route("/jutalom", methods=["POST"])
def jutalom():
    """A feladatok jutalma"""
    # A megfelelő szintű jutalom kiírása
    eleres = os.path.join(app.config['kepekossz'], eval('kepj'+str((helyzet+10))))
    if request.form['gomb'] == 'tovább':
        pass
        return render_template("jutalom.html", név=név, jutalom=eval('jutalom'+str(helyzet)), hányadik=helyzet, kepj=eleres)
    else:
        pass
        return redirect("/vege")

@app.route("/vege", methods=["GET"])
def vege():
    """Idő előtt befejezte a játékot"""
    result = db.execute("INSERT INTO users (játékos, szint) VALUES(:játékos, :szint)", játékos=név, szint=helyzet-1)
    return render_template("vege.html", név=név)

@app.route("/eddigiek", methods=["GET"])
def eddigiek():
    """Az eddigi kitöltők listája"""
    result = db.execute("SELECT játékos, szint, date, telo FROM users")
    return render_template("eddigiek.html", result=result)

@app.route("/sql", methods=["GET", "POST"])
def sql():
    """Az SQL rögzítése"""
    global név
    result = db.execute("INSERT INTO users (játékos, szint, telo) VALUES(:játékos, :szint, :telo)", játékos=név, szint=5, telo=request.form.get("telefonszám"))
    return render_template("köszi.html")