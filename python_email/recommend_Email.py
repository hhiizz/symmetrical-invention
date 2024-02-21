
from pathlib import Path
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from pathlib import Path
import smtplib




def recmooemd_email(email,vertical):
    content = MIMEMultipart()  #建立MIMEMultipart物件
    print('正在傳送請稍後...')
    content.add_header('Subject', '驗證碼')
    content.add_header('From', 'vu56032613@gmail.com')
    content.add_header('To', email)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 使用相對路徑引用 myemail2.html 檔案
    template_path = os.path.join(current_dir,'myemail2.html')
    template = Template(Path(template_path).read_text(encoding="utf-8"))
    body = template.substitute({'vertical':vertical})

    content.attach(MIMEText(body,'html'))  #郵件內容
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("vu56032613@gmail.com",'rvpxedxzczrrabik')  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)