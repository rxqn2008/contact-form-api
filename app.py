from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # 允许所有域名跨域访问

# 配置邮件发送
app.config['MAIL_SERVER'] = 'smtp.qq.com'  # 替换为您的SMTP服务器
app.config['MAIL_PORT'] = 587  # 替换为您的SMTP端口
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # 邮箱用户名
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # 邮箱密码
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')  # 默认发件人

mail = Mail(app)

@app.route('/api/message', methods=['POST'])
def submit_message():
    """提交留言并发送邮件"""
    try:
        # 获取表单数据
        data = request.json
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        
        # 数据验证
        if not all([name, email, subject, message]):
            return jsonify({"error": "缺少必要字段"}), 400
        
        # 创建邮件内容
        msg = Message(
            f'[网站留言] {subject}',
            recipients=[os.environ.get('RECIPIENT_EMAIL')]  # 收件人邮箱
        )
        msg.body = f"""
        发件人: {name} <{email}>
        
        主题: {subject}
        
        留言内容:
        {message}
        """
        
        # 发送邮件
        mail.send(msg)
        
        return jsonify({"message": "留言提交成功，感谢您的反馈！"}), 200
    
    except Exception as e:
        return jsonify({"error": f"提交失败: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)  