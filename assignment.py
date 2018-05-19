import numpy as np 
from matplotlib import pyplot as plt  
from pandasql import sqldf
from sqlalchemy import create_engine, text
import pandas as pd
from pandas import ExcelWriter
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders
import df
import time
from os.path import basename
import sys
import smtplib
import sys,os
from email.utils import COMMASPACE, formatdate


#sender address
sender=""
paswd=""
abs="E:\Python Pandas Numpy"


#smtp func
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
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)
        smtp = smtplib.SMTP(server)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender,paswd)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()


#importing DataFrame
dict=df.dic()
brics = pd.DataFrame(dict)
pd.set_option('expand_frame_repr', False)
pysqldf = lambda q: sqldf(q, globals())
try:
    

    if len(sys.argv)>1:
        check=''.join(sys.argv[1:])
        data = pd.read_csv('{}\{}.csv'.format(abs,check))  #change absolute path
        ff = pysqldf("select query from brics where sub=\"{}\"".format(check))
        ff = pysqldf(ff.loc[ff.index[0],'query'])
        print("-----------------------------\nRunning Job For Sales\nPrinting Sales Data to Console\n-----------------------------\n{}\n-----------------------------".format(ff))
        writer = ExcelWriter('{}\{}_output.xlsx'.format(abs,check))
        ff.to_excel(writer,'{}'.format(check))
        writer.save()
        plt.pie(ff[ff.columns[1]],labels=ff.dep,shadow=True,autopct='%1.0f%%')
        plt.title('Total {}'.format(check))
        plt.legend()
        plt.savefig('{}\{}_output.png'.format(abs,check))
        plt.close()
        send_mail(sender,pysqldf("select emailId from brics where sub=\"{}\"".format(check)).emailId.values.tolist() ,"Report for {}".format(check),"{}".format(check),["{}\{}_output.png".format(abs,check),"{}\{}_output.xlsx".format(abs,check)])

except FileNotFoundError as e:
    print("Error!! File May not be created Yet.")
except Exception as e:
    print(e)