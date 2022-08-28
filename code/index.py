'''
Author: flwfdd
Date: 2022-08-28 15:52:41
LastEditTime: 2022-08-28 22:55:45
Description: 
_(:з」∠)_
'''
from operator import and_
from flask import Flask, Response, request
from sqlalchemy.sql.expression import func
from datetime import datetime, date
from flask_cors import CORS
import json
import config
import db

app = Flask(__name__)
CORS(app, resources=r"/*")


# 数据库设置
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.db.app = app
db.db.init_app(app)
db.db.create_all()


# 返回
def res(data, status=200):
    class ComplexEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.strftime('%Y/%m/%d %H:%M:%S')
            elif isinstance(obj, date):
                return obj.strftime('%Y/%m/%d')
            else:
                return json.JSONEncoder.default(self, obj)
    return Response(json.dumps(data, cls=ComplexEncoder), status=status, mimetype='application/json')


@app.route('/')
def index():
    with open("index.html","r") as f:
        s=f.read()
    return s


@app.route('/exam/info/', methods=['GET'])
def exam_info():
    exam = request.args.get('exam', '')
    e = db.Exam.query.filter(
        and_(db.Exam.id == exam, db.Exam.active == True)).first()
    return res(db.to_dict(e))


@app.route('/exam/start/', methods=['POST'])
def exam_start():
    data = request.get_json()
    name = data.get('name', '')
    exam = data.get('exam', '')
    e = db.Exam.query.filter(
        and_(db.Exam.id == exam, db.Exam.active == True)).first()
    q = db.Problem.query.filter(
        and_(db.Problem.exam == exam, db.Problem.active == True))
    if e.random:
        q = q.order_by(func.rand()).limit(e.random)
    q = q.all()
    lg = db.ExamLog(exam=exam, name=name,
                    problems=json.dumps([i.id for i in q]),
                    answers=json.dumps([i.answer for i in q], ensure_ascii=False),
                    scores=json.dumps([i.score for i in q]),
                    full_score=sum([i.score for i in q]),
                    end_time=datetime.fromtimestamp(datetime.now().timestamp()+e.limit_time+4.2))
    db.add(lg)
    db.commit()
    dic = {
        "title": e.title,
        "intro": e.intro,
        "limit_time": e.limit_time,
        "log_id": lg.id,
        "problems": [{
            "type": i.type,
            "text": i.text,
            "data": json.loads(i.data),
            "score": i.score,
        } for i in q]
    }
    return res(dic)


@app.route('/exam/submit/', methods=['POST'])
def exam_submit():
    data = request.get_json()
    log_id = data.get('log_id', '')
    name = data.get('name', '')
    submit_answers=data.get('answers','')
    out=[]
    score=0
    q=db.ExamLog.query.filter(and_(db.ExamLog.id==log_id,db.ExamLog.name==name)).first()
    if datetime.now()> q.end_time:
        return res({'msg':"超出时间限制"},500)
    q.end_time=datetime.now()
    q.submit_answers=submit_answers
    submit_answers=json.loads(submit_answers)
    answers=json.loads(q.answers)
    scores=json.loads(q.scores)
    for i in range(len(answers)):
        if submit_answers[i]==answers[i]:
            out.append({"ac":True})
            score+=scores[i]
        else:
            out.append({"ac":False,"answer":answers[i]})
    q.score=score
    db.commit()
    return res({"full_score":q.full_score,"score":score,"result":out})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)

