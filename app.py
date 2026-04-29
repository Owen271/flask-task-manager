from flask import Flask, request, redirect, render_template
from task_manager import TaskManager


app = Flask(__name__)

manager = TaskManager()
manager.loadcsv()

@app.route("/")
def home():
    query = request.args.get("query","")
    if query:
        tasks = sorted(manager.search_tasks(query), key=lambda x: x.id)
    else:
        tasks = sorted(manager.list_tasks(), key=lambda x: x.id)

    output = render_template("index.html", tasks=tasks, query=query)

    return output

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"].upper()
    priority = request.form["priority"].upper()
    due = request.form["due"]

    manager.add_task(title, priority, due)
    manager.savecsv()

    return redirect("/")

@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    manager.complete_task(task_id)
    manager.savecsv()

    return redirect("/")
  
@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    manager.del_task(task_id)
    manager.savecsv()

    return redirect("/")
        
@app.route("/edit/<int:task_id>")
def edit_page(task_id):
    task = manager.tasks[task_id]
    output = render_template("edit.html", task=task)

    return output

@app.route("/edit/<int:task_id>", methods=["POST"])
def edit(task_id):
    title = request.form["title"].upper()
    priority = request.form["priority"].upper()
    due = request.form["due"]
    manager.edit_task(task_id, title, priority, due)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)