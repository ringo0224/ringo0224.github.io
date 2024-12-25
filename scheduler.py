from flask import Flask, request, render_template, redirect, url_for
import datetime

app = Flask(__name__)

# スケジュールデータ（仮想データベース）
schedule = []

# 重複チェック関数
def is_conflict(new_time):
    return any(entry["datetime"] == new_time for entry in schedule)

# ホームページ
@app.route('/')
def index():
    sorted_schedule = sorted(schedule, key=lambda x: x["datetime"])
    return render_template('index.html', schedule=sorted_schedule)

# 面接追加ページ
@app.route('/add', methods=['GET', 'POST'])
def add_interview():
    if request.method == 'POST':
        candidate_name = request.form['candidate_name']
        date = request.form['date']
        time = request.form['time']

        try:
            interview_time = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            if is_conflict(interview_time):
                return "Error: The selected time is already booked."
            else:
                schedule.append({"candidate": candidate_name, "datetime": interview_time})
                return redirect(url_for('index'))
        except ValueError:
            return "Invalid date or time format. Please try again."

    return render_template('add.html')

# 面接削除ページ
@app.route('/delete/<int:index>', methods=['POST'])
def delete_interview(index):
    if 0 <= index < len(schedule):
        schedule.pop(index)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
