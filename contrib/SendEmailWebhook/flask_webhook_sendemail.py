#!/usr/bin/env python3

from flask import Flask, request
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import os

app = Flask(__name__)

# Set Your Variables
password = "Spep23br"
from_email = "gsimoes@neotel.com.br"
to_email = ['guilherme.sphc@gmail.com']
server = smtplib.SMTP('smtp.gmail.com: 587')

def sendemail(Operation,Type, Title, User, Severity, Description):

        msg = MIMEMultipart('related')
        
        # format text message
        message = "Prezado(a),<br><br><b>Nova Acao:</b>  %s de %s - %s <br><b>Executado pelo Analista:</b>   %s<br><b>Description:</b> %s<br><b>Severity:</b>  %ss<br><b>Categoria:</b> Nao Conformidade de Configuracao<br><br>Atenciosamente,<br>" %(Operation, Type,Title,User, Description, Severity)
        
        # setup basic parameters of the message
        msg['From'] = from_email
        recipients = to_email
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = "Portal - %s of New %s - %s" %(Operation, Type, Title)

        # message content
        msgAlternative = MIMEMultipart('alternative')
        msg.attach(msgAlternative)
        msgText = MIMEText(message + '<img src="cid:image1">', 'html' )
        msgAlternative.attach(msgText)

        # use it if you need an image as email signature
        fp = open('unnamed.png', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<image1>')
        msg.attach(msgImage)

        #create server usign gmail
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        # send the message via the server.
        server.sendmail(msg['From'], recipients , msg.as_string())
        server.quit()
        return "successfully sent email to %s:" % (msg['To'])


def sendemail_update(Operation,Type, Title, User, Resolution, Cause, Impact):
        
        msg = MIMEMultipart('related')
        # format text message
        message = "Prezado(a),<br><br><b>Case encerrado com acao:</b> %s de %s - %s <br><b>Executado pelo Analista:</b>  %s<br><b>Description:</b>  %s<br><b>Conclusao:</b> %s <br><b>Impact:</b>  %s<br><br>Atenciosamente,<br>" %(Operation, Type,Title,User, Resolution, Cause, Impact)
       

        # setup basic parameters of the message    
        msg['From'] = from_email
        recipients = to_email
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = "Portal - %s of %s - %s" %(Operation, Type, Title)
        
        # message content
        msgAlternative = MIMEMultipart('alternative')
        msg.attach(msgAlternative)
        msgText = MIMEText(message + '<img src="cid:image1">', 'html' )
        msgAlternative.attach(msgText)

        # use it if you need an image as email signature
        fp = open('unnamed.png', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<image1>')
        msg.attach(msgImage)

        #create server
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        # send the message via the server.
        server.sendmail(msg['From'], recipients , msg.as_string())
        server.quit()
        return "successfully sent email to %s:" % (msg['To'])


@app.route("/", methods=['POST'])
def hello():

        #Convert string to  json object
        data=json.loads(request.data)
        
        #set variables to get useful fields
        Operation=(data["operation"])
        Type=(data["objectType"])
        Title=(data["object"]["title"])
        User=(data["object"]["createdBy"])

        #if action is a new case creation
        if Type == 'case' and Operation == 'Creation':
                
                #send email
                Severity = (data["object"]["severity"])
                Description = (data["object"]["description"])
                status = sendemail(Operation,Type, Title, User, Severity, Description)
        
        #if action is an update of existing
        if Type == 'case' and Operation == 'Update':
                
                #get some more useful fields
                Resolution = (data["details"]["summary"])
                Cause = (data["details"]["resolutionStatus"])
                Impact = (data["details"]["impactStatus"])
                
                #send email
                status = sendemail_update(Operation,Type, Title, User, Resolution, Cause, Impact)

        #print(data["operation"])



        #Convert json object to string
        #print(json.dumps(data, indent=4))
        return "OK"

if __name__ == "__main__":
    app.run()
