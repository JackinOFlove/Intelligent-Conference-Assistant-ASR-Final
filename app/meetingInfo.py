import csv
from flask import Blueprint, request, jsonify
from pathlib import Path
from datetime import datetime
import os

# 创建一个 Blueprint 实例
meetingInfo_routes = Blueprint('meetingInfo', __name__, url_prefix='/meetingInfo')


# 这个接口的路由是 http://127.0.0.1:5000/meetingInfo/saveMeeting
@meetingInfo_routes.route('/saveMeeting', methods=['POST'])
def save_meeting():
    # 从请求中获取数据
    data = request.get_json()
    print("data",data)

    meeting_title = data.get('meetingTitle')

    summary = data.get('Summary')

    # 检查必需字段是否存在
    if not all([meeting_title, summary]):
        return jsonify({'error': '缺少必需的字段'}), 400

    # 确保目录存在
    data_dir = Path('app/data')
    data_dir.mkdir(parents=True, exist_ok=True)

    # 使用 os.path.join 构建文件路径
    file_path = os.path.join('app', 'data', 'meetingInfo.csv')

    # 读取文件并查找 meeting_title
    updated = False
    rows = []
    if os.path.exists(file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['meetingTitle'] == meeting_title:  # 使用列名 'meetingTitle' 来索引
                    # 找到 meeting_title，更新 summary
                    row['Summary'] = summary  # 使用列名 'Summary' 来更新
                    updated = True
                rows.append(row)

    if not updated:
        return jsonify({'error': '未找到指定的 meetingTitle'}), 404

    # 写回文件
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['meetingID', 'meetingTitle', 'startTime', 'endTime', 'persons', 'Summary']  # 确保字段名与 CSV 文件一致
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return jsonify({'message': '会议信息已更新'}), 200


# 这个接口的路由是 http://127.0.0.1:5000/meetingInfo/saveHalfMeeting
@meetingInfo_routes.route('/saveHalfMeeting', methods=['POST'])
def save_half_meeting():
    # 从请求中获取数据
    data = request.get_json()
    meeting_title = data.get('meetingTitle')
    start_time = data.get('startTime')
    end_time = data.get('endTime')
    # 将时间戳转换为正常时间格式
    print("data=",data)
    #start_time = datetime.fromtimestamp(int(start_time) / 1000).strftime('%Y-%m-%dT%H:%M:%S')
    #end_time = datetime.fromtimestamp(int(end_time) / 1000).strftime('%Y-%m-%dT%H:%M:%S')
    persons = data.get('persons')

    # 检查必需字段是否存在
    if not all([meeting_title, start_time, end_time, persons]):
        return jsonify({'error': '缺少必需的字段'}), 400

    # 确保目录存在
    data_dir = Path('app/data')
    data_dir.mkdir(parents=True, exist_ok=True)

    # 使用 os.path.join 构建文件路径
    file_path = os.path.join('app', 'data', 'meetingInfo.csv')

    # 获取最大的meeting_id并加1
    max_id = 0
    if os.path.exists(file_path):
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0].isdigit():
                    max_id = max(max_id, int(row[0]))

    meeting_id = max_id + 1

    # 写入文件
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([meeting_id, meeting_title, start_time, end_time, persons, ""])  # 确保每行都有结束符

    return jsonify({'message': '会议信息已保存'}), 201


# 这个接口的路由是 http://127.0.0.1:5000/meetingInfo/getMeetings
@meetingInfo_routes.route('/getMeetings', methods=['GET'])
def get_meetings():
    # 使用 os.path.join 构建文件路径
    file_path = os.path.join('app', 'data', 'meetingInfo.csv')

    # 读取文件
    meetings = []
    if os.path.exists(file_path):
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                meetings.append(row)

    return jsonify(meetings), 200