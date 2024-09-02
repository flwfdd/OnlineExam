'''
Author: flwfdd
Date: 2022-08-28 15:52:41
LastEditTime: 2022-09-07 15:26:37
Description: 
_(:з」∠)_
'''
from sqlalchemy import and_, or_
import random
from flask import Flask, Response, request
from sqlalchemy.sql.expression import func
from datetime import datetime, date, timedelta
from flask_cors import CORS
import requests
import hmac
import json
import config
import db

app = Flask(__name__)
CORS(app, resources=r"/*")


# 数据库设置
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
with app.app_context():
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
    with open("index.html", "r", encoding="utf-8") as f:
        s = f.read()
    return s


@app.route('/exam/info/', methods=['GET'])
def exam_info():
    exam = request.args.get('exam', '')
    e = db.Exam.query.filter(
        and_(db.Exam.id == exam, db.Exam.active == True)).first()
    return res(db.to_dict(e))


def geetest(dic):
    # 1.初始化极验参数信息
    captcha_id = config.geetest_id
    captcha_key = config.geetest_key
    api_server = 'http://gcaptcha4.geetest.com'

    # 2.获取用户验证后前端传过来的验证参数
    lot_number = dic['lot_number']
    captcha_output = dic['captcha_output']
    pass_token = dic['pass_token']
    gen_time = dic['gen_time']

    # 3.生成签名
    # 生成签名使用标准的hmac算法，使用用户当前完成验证的流水号lot_number作为原始消息message，使用客户验证私钥作为key
    # 采用sha256散列算法将message和key进行单向散列生成最终的签名
    lotnumber_bytes = lot_number.encode()
    prikey_bytes = captcha_key.encode()
    sign_token = hmac.new(prikey_bytes, lotnumber_bytes, digestmod='SHA256').hexdigest()

    # 4.上传校验参数到极验二次验证接口, 校验用户验证状态
    query = {
        "lot_number": lot_number,
        "captcha_output": captcha_output,
        "pass_token": pass_token,
        "gen_time": gen_time,
        "sign_token": sign_token,
    }
    # captcha_id 参数建议放在 url 后面, 方便请求异常时可以在日志中根据id快速定位到异常请求
    url = api_server + '/validate' + '?captcha_id={}'.format(captcha_id)
    # 注意处理接口异常情况，当请求极验二次验证接口异常或响应状态非200时做出相应异常处理
    # 保证不会因为接口请求超时或服务未响应而阻碍业务流程
    dic = requests.post(url, query).json()
    return dic['result']=='success'

@app.route('/exam/start/', methods=['POST'])
def exam_start():
    data = request.get_json()
    name = data.get('name', '')
    exam = data.get('exam', '')
    captcha=data.get('captcha', '')
    
    if not geetest(json.loads(captcha)):
        return res({'msg':'验证失败Orz'},401)

    e = db.Exam.query.filter(
        db.Exam.id == exam, db.Exam.active == True).first()
    if db.db.session.query(func.count(db.ExamLog.id)).filter(db.ExamLog.exam == exam, db.ExamLog.name == name, or_(db.ExamLog.finish == True, db.ExamLog.end_time <= datetime.now())).scalar() >= e.limit_number:
        return res({'msg': '提交数量已达上限（{}次）！'.format(e.limit_number)}, 403)
    lg = db.ExamLog.query.filter(db.ExamLog.exam == exam, db.ExamLog.name == name,
                                 db.ExamLog.finish == False, db.ExamLog.end_time > datetime.now()).first()
    if not lg:
        q = db.Problem.query.filter(
            and_(db.Problem.exam == exam, db.Problem.active == True))
        if e.random:
            q = q.order_by(func.rand()).limit(e.random)
        q = q.all()
        lg = db.ExamLog(exam=exam, name=name,
                        problems=q,
                        full_score=sum([i.score for i in q]),
                        end_time=datetime.now()+timedelta(seconds=e.limit_time+4.2))
        db.add(lg)
        db.commit()
    q = lg.problems
    dic = {
        "title": e.title,
        "intro": e.intro,
        "start_time": lg.start_time,
        "end_time": lg.end_time-timedelta(seconds=4.2),
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
    submit_answers = data.get('answers', '')
    out = []
    score = 0
    q = db.ExamLog.query.filter(
        and_(db.ExamLog.id == log_id, db.ExamLog.name == name)).first()
    if datetime.now() > q.end_time:
        return res({'msg': "超出时间限制"}, 500)
    q.end_time = datetime.now()
    q.finish = True
    q.submit_answers = submit_answers
    submit_answers = json.loads(submit_answers)
    answers = [i.answer for i in q.problems]
    scores = [i.score for i in q.problems]
    for i in range(len(answers)):
        if submit_answers[i] == answers[i]:
            out.append({"ac": True})
            score += scores[i]
        else:
            out.append({"ac": False, "answer": answers[i]})
    q.score = score

    # 抽奖
    q.extra="很遗憾，没有中奖捏:("
    if int(random.random()*q.full_score+1)<=((q.score/q.full_score)**3)*q.full_score:
        prizes=db.Prize.query.filter_by(exam=q.exam).with_for_update().all()
        tot=sum([i.remain for i in prizes])
        x=random.random()
        r=0
        if tot!=0:
            for i in prizes:
                r+=i.remain/tot
                if x<r:
                    q.extra="恭喜获得{}！".format(i.text)
                    i.remain-=1
                    break

    db.commit()
    return res({"full_score": q.full_score, "score": score, "result": out, "start_time": q.start_time, "end_time": q.end_time,"extra":q.extra})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
