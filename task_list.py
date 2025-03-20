from flask import Flask,request, jsonify , Blueprint
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
import re

task_list_bp = Blueprint("task_list", __name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client.task_manager
tasks_collection = db.tasks

# Regex for valid URL
URL_REGEX = re.compile(
    r'^(https?:\/\/)?'  # http:// or https://
    r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,})'  # domain
    r'(:\d+)?(\/.'
    '*)?$'  # port and path
)

task_list_bp.route("/display-message", methods=['POST'])
def display_message():
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"status": 0, "msg": "Message cannot be empty!", "class": "error"})
    new_task ={
        "message" : message,
        "created_at":datetime.utcnow()
    }
    result = tasks_collection.insert_one(new_task)
    if result.inserted_id:
        return jsonify({"status": 1, "msg": "Task message added succefylly", "class": "success"})
    else:
        return jsonify({"status": 0, "msg":"Failed to add Task", "class": "error"})





task_list_bp.route("/tasks", methods=['GET'])
def get_tasks():
    """Retrieve tasks in reverse order (newest first)"""
    tasks = list(tasks_collection.find().sort("created_at", -1))  

    task_list = [
        {
            "id": str(task["_id"]),
            "message": task["message"],
            "created_at": task["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        }
        for task in tasks
    ]
    
    return jsonify({"status": 1, "tasks": task_list})


# @app.route("/admin/add-task", methods=['POST'])
# def add_task():
#     """Admin can add a new task as a link"""
#     data = request.get_json()
#     task_link = data.get("link")

#     # Validate the task link
#     if not task_link or not re.match(URL_REGEX, task_link):
#         return jsonify({"status": 0, "msg": "Invalid URL format", "class": "error"})

#     new_task = {
#         "link": task_link,
#         "created_at": datetime.utcnow()
#     }

#     # Insert into MongoDB
#     result = tasks_collection.insert_one(new_task)

#     if result.inserted_id:
#         return jsonify({"status": 1, "msg": "Task added successfully", "class": "success"})
#     else:
#         return jsonify({"status": 0, "msg": "Failed to add task", "class": "error"})

# @app.route("/tasks/<task_id>", methods=['DELETE'])
# def delete_task(task_id):
#     """Admin can delete a task by ID"""
#     result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
    
#     if result.deleted_count == 0:
#         return jsonify({"status": 0, "msg": "Task not found", "class": "error"})

#     return jsonify({"status": 1, "msg": "Task deleted successfully", "class": "success"})


