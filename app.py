from flask import Flask, render_template, request
import psycopg2

postGreSql_Url = "postgres://seficfue:GKM9vVFlt02nWGdBiXk-Eb9RRygjQxuy@arjuna.db.elephantsql.com:5432/seficfue"
connection = psycopg2.connect(postGreSql_Url)
try:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "CREATE TABLE T_Table (account TEXT,date TEXT,amount REAL);"
            )
except psycopg2.errors.DuplicateTable:
    pass

app = Flask(__name__)


# transactions = []


@app.route('/', methods=["GET", "POST"])
def home():
    # print(request.args)
    # print(request.form.get("amount"))
    if request.method == "POST":
        # print(request.form)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO T_Table VALUES (%s,%s,%s);", (
                        request.form.get("account"),
                        request.form.get("date"),
                        float(request.form.get("amount"))
                    )
                )

        # for x in transactions:
        #     print(x)
    return render_template("form.html")


@app.route("/see_transaction")
def show_transactions():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM T_Table ;")
            transactions = cursor.fetchall()
    return render_template("transactions.jinja2",
                           entries=transactions)  # here extension jinja2 or html doesn't matter as we can embed jinja2 format in html by {{ }}


if __name__ == '__main__':
    app.run()
