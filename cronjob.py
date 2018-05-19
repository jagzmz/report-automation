import df
from pandasql import sqldf
import schedule
import pandas as pd
import time
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import sys,os

if len(sys.argv)>1:
    check=''.join(sys.argv[1:])
    def send_mail(send_from, send_to, subject, text, files=None,
                server="smtp.gmail.com"):
        

        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)


        smtp = smtplib.SMTP(server)
        smtp.ehlo()
        smtp.starttls()
        smtp.login('','')
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
   



    #importing dataframe
    dict =df.dic()
    pysqldf = lambda q: sqldf(q, globals())
    brics=pd.DataFrame(dict)
    c_job_mins=pysqldf("select sub as Subject,cronTime from brics;")
    # c_job_mins=c_job_mins.cronTime.values

    print("----------------------------\nPrinting Cronjob in Minutes\n----------------------------")

    print(c_job_mins.to_string(index=False))

    print("----------------------------\nCronJob is Running\n----------------------------")

    if check=="sales":
        os.system('python "E:\Python Pandas Numpy\\assignment.py" sales')
        send_mail("mijaganiya@gmail.com",pysqldf("select emailId from brics where sub=\"sales\"").emailId.values.tolist() ,"Report for Sales","Sales",["E:\Python Pandas Numpy\sales_output.png","E:\Python Pandas Numpy\sales_output.xlsx"])
    elif check=="profit":
        os.system('python "E:\Python Pandas Numpy\\assignment.py" profit')        
        send_mail("mijaganiya@gmail.com",pysqldf("select emailId from brics where sub=\"profit\"").emailId.values.tolist() ,"Report for Sales","Profit",["E:\Python Pandas Numpy\profit_output.png","E:\Python Pandas Numpy\profit_output.xlsx"])



        

