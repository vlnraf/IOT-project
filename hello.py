from flask import Flask, render_template, request
from dbconnect import connection

app = Flask(__name__)

@app.route("/")
def homepage():
    try:
        cur, conn = connection()
        cur = conn.cursor()
        cur.execute("SELECT user.name FROM user")
        user = cur.fetchall()
        user = [row[0] for row in user]
        cur.close()
        return render_template('index.html', users=user)

    except Exception as e:
        return('Connection error')


@app.route("/bins", methods= ['GET', 'POST'])
def bin():
    if request.method == 'POST':
        try:
            cur, conn = connection()
            cur = conn.cursor()
            cur.execute("SELECT type FROM bin")
            bin_type = cur.fetchall()
            bin_type = [row[0] for row in bin_type]
            cur.execute("SELECT capacity FROM bin")
            capacity = cur.fetchall()
            capacity = [row[0] for row in capacity]
            cur.close()
            bar_labels = bin_type
            bar_values = capacity
            return render_template('bins.html', title='bins', max = 100, labels=bar_labels, values=bar_values)
    
        except Exception as e:
            return('Connection error')
    

@app.route("/user", methods=['GET','POST'])
def user_interaction():
    if request.method == 'POST':
        req = request.form
        name = req.get("utenti")
        print(name)
        try:
            cur, conn = connection()
            cur = conn.cursor()
            sql = "SELECT user.name, user_interaction.garbage_weight, user_interaction.timestamp FROM user INNER JOIN user_interaction ON user.card_id = user_interaction.user_id WHERE name = %s "
            name = (str(name), )
            cur.execute(sql, name)
            data = cur.fetchall()
            user = [row[0] for row in data]
            garbage = [row[1] for row in data]
            time = ["" + str(row[2].day) + "/" + str(row[2].month) + "/" + str(row[2].year) for row in data]
            cur.close()
            bar_labels = time
            bar_values = garbage
            return render_template('user.html', title=str(user[0]), max = 5000, labels=bar_labels, values=bar_values)
    
        except Exception as e:
            return('Connection error')






@app.route("/weight", methods= ['GET', 'POST'])
def user_weight():
    if request.method == 'POST':
        req = request.form
        name = req.get("utenti")
        print(name)
        try:
            cur, conn = connection()
            cur = conn.cursor()
            name = (str(name),)
            sql = "SELECT user.name, SUM(user_interaction.garbage_weight), bin.type FROM user JOIN user_interaction ON user.card_id = user_interaction.user_id JOIN bin ON user_interaction.bin_id = bin.id WHERE user.name = %s GROUP BY bin.type"
            cur.execute(sql, name)
            data = cur.fetchall()
            user = [row[0] for row in data]
            garbage = [row[1] for row in data]
            bin_type = [row[2] for row in data]
            cur.close()
            bar_labels = bin_type
            bar_values = garbage
            return render_template('interaction.html', title="Weights", max = 5000, labels=bar_labels, values=bar_values)
    
        except Exception as e:
            return('Connection error')
