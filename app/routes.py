from flask import Blueprint, render_template

# 创建一个 Blueprint 实例
main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def home():
    return render_template('home.html')

@main_routes.route('/meetingNote')
def meeting_note():
    return render_template('meetingNote.html')

@main_routes.route('/meetingAssistant')
def meeting_assistant():
    return render_template('meetingAssistant.html')

@main_routes.route('/meetingHistory')
def meeting_history():
    return render_template('meetingHistory.html')

