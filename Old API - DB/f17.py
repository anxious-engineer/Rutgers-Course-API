import urllib, json
import gzip
from StringIO import StringIO
import ast
from time import gmtime, strftime
import smtplib
import logging

def get_open_sections():
    url = 'https://sis.rutgers.edu/soc/api/openSections.gzip?year=2017&term=9&campus=NB'

    response = urllib.urlopen(url).read()

    buf = StringIO(response)
    f = gzip.GzipFile(fileobj=buf)

    data = ast.literal_eval(f.read())

    return data


if __name__=='__main__':

    logging.basicConfig(filename='snipe.log', level=logging.DEBUG)

    currTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    print currTime
    logging.info("\tCheck run at: " + currTime)

    open_indexes = get_open_sections()

    print(len(open_indexes))

    register_for_index = None
    index1 = '00193'
    index2 = '07143'


    if index1 in open_indexes:
        register_for_index = index1
    elif index2 in open_indexes:
        register_for_index = index2

    if(register_for_index):
        info = "https://sims.rutgers.edu/webreg/editSchedule.htm?login=cas&semesterSelection=92017&indexList="
        info += register_for_index
    	fromaddr = 'Server'
    	toaddrs  = '8568675309@vtext.com'
    	msg = "\r\n".join([
    	  "From: Server",
    	  "To: 8568675309@vtext.com",
    	  "Register Here:",
    	  "",
    	  info
    	  ])
    	username = '<gmail>@gmail.com'
    	password = '<password>'
    	server = smtplib.SMTP('smtp.gmail.com:587')
    	server.ehlo()
    	server.starttls()
    	server.login(username,password)
    	server.sendmail(fromaddr, toaddrs, msg)
    	server.quit()

    currTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    logging.info("\tCheck complete at: " + currTime)
