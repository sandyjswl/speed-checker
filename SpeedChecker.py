import speedtest
import threading
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# SPEEDTEST SETUP #

speedtester = speedtest.Speedtest()
speedtester.get_best_server()
#Configure Email-ID and Password
MY_ADDRESS = '' 
PASSWORD = ''

def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """ 
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def getSpeed(down=25, up=25, time=600, threshold=10):
    # down and up are the expected values for download and upload speed, respectively, in Megabytes.
    # threshold is the "cutoff" point. If obtained download speed < down-threshold or obtained upload speed < up-threshold, then we'll nag your ISP!
    threading.Timer(time, getSpeed).start() # Runs the function every 10 minutes (unless you specify another one).

    speedtester = speedtest.Speedtest()
    speedtester.get_best_server()

    # speedtester.download() and speedtester.upload() return a float which represents the internet speed in B/s.
    
    dSpeed = speedtester.download() / 1000000  # B/s to MB/s
    uSpeed = speedtester.upload() / 1000000  # B/s to MB/
  

    if dSpeed < down-threshold and uSpeed < up-threshold:
        
        
        print(f"\n\nCurrent download speed {dSpeed}MB/s and upload speed {uSpeed}MB/s on a bandwith of {down}/{up} MB/s.\n Sending mail.......\n\n")
        sending(dSpeed,uSpeed)
        print("---------------------------------------------------------------------------------------------------------------")
    elif dSpeed < down-threshold: # Compares the download speed from the speedtest with the expected download speed passed as a function argument minus the threshold value. 

       
        
        print(f"Current download speed {dSpeed}MB/s and upload speed {uSpeed}MB/s on a bandwith of {down}/{up} MB/s.\n Sending mail.......")
        sending(dSpeed,uSpeed)
        print("---------------------------------------------------------------------------------------------------------------")
    elif uSpeed < up-threshold: # Compares the upload speed from the speedtest with the expected download speed passed as a function argument minus the threshold value.
       
       
        print(f"Current download speed {dSpeed}MB/s and upload speed {uSpeed}MB/s on a bandwith of {down}/{up} MB/s.\n Sending mail.......")
        sending(dSpeed,uSpeed)
        print("---------------------------------------------------------------------------------------------------------------")
                


def sending(down_speed, up_speed):
    names, emails = get_contacts('mycontacts.txt') # read contacts
    message_template = read_template('message.txt')

    # set up the SMTP server
    #s = smtplib.SMTP(host='your_host_address_here', port=your_port_here)
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title(),DOWN_SPEED=down_speed,UPLOAD_SPEED=up_speed)

        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="Network Down"
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()    


getSpeed()
