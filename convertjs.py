#!/usr/bin/python
import subprocess
from subprocess import PIPE,Popen
import json
import subprocess


print "saaaaa"

#change_res=subprocess.Popen(['cat', 'queue-res' ,'|head','-n 2'],stdout=subprocess.PIPE)
#out,err=change_res.communicate()
#print out

#change_res=subprocess.call("tr ' ' '\n' < queue-res  |  grep -e \"QUEUE(\" -e \"TYPE(\"" )
#queue_res=open('queue-res','r')

#'[{"{#QUEUE}": "DEV.DEAD.LETTER.QUEUE"}]'

#tr ' ' '\n' < queue-res  |  grep -e "QUEUE(" -e "TYPE("


qdesc=[]
qdjson=[]
cmd = '/opt/mqm/bin/dspmq -n '
proc = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
o, e = proc.communicate()
if o:
    res=o.replace(" ","\n").split("\n")
    #print res
    for x in res:
        if x :
           if x.find("QMNAME" ) is not -1:
               print x
               qname=(x.split("(")[1]).replace(")","")
               qdjson.append({"{#QNAME}":qname})
               qdjsondump=json.dumps(qdjson)
               print qname
               #cmd = 'zabbix_sender -vv  -z 192.168.0.166 -s "ibm-queu-1" -k queu-test -o ' + '\''+jslist+'\''
               cmd = 'zabbix_sender -vv  -z 192.168.0.166 -s "ibm-queu-1" -k ' + "queuemanager" + ' -o ' +  '\''+qdjsondump+'\''
               print cmd
               proc = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
               o, e = proc.communicate()
               print o
               print e


           if x.find("STATUS" ) is not -1:
               status=(x.split("(")[1]).replace(")","")
               print status

               qdesc.append({"qname":qname,"status":status})


for i in qdesc:
    status=i["status"]
    qname=i["qname"]

    cmd = 'zabbix_sender -vv  -z 192.168.0.166 -s "ibm-queu-1" -k ' + "state["+qname+"]" + ' -o ' +  status.strip()
    print cmd
    proc = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()







    
    
    
#############

     
     
    #QQUERY=`echo "DISPLAY QUEUE(*) | /opt/mqm/bin/runmqsc "+ qname
    
    cmd='echo "DISPLAY QUEUE(*)" | /opt/mqm/bin/runmqsc  '+qname
    proc = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    #print o
    #print e
    queue_res=o.split("\n")
    print queue_res
     
##################
    
    
    
    
    
    
    
    
    
    
    
    mylist=[]
    for i in queue_res:
        print i
        for s in i.split('\n'):
            #{#QUEUE}
            
            if s.find("QUEUE(")  is not -1 and s.find("TYPE(") is not -1 :
              cl=s.split(" ")
              for x in cl:
                  if len(x) > 0:
                      templist=x.split("(")
                      mylist.append({ "{#" + templist[0] + "}" :templist[1].replace(")","")})
    
    
    
                      #cmd = ['echo', 'I like potatos']
                      #cmd = ['echo','"DISPLAY"',x+"\"",'|','/opt/mqm/bin/runmqsc','QM1']
                      #cmd = ['echo',"salam",">",'/tmp/ssss']
                      #cmd ="echo salam >>/tmp/sss "
                      if x.find("QUEUE") is not -1 :
                        #cmd = 'echo "DISPLAY '+x+'" | /opt/mqm/bin/runmqsc QM1' 
                        cmd = 'echo "DISPLAY '+x+'" | /opt/mqm/bin/runmqsc '+qname 

                        #print cmd
                      #proc = subprocess.Popen(cmd)
                      proc = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                      o, e = proc.communicate()
                      #print('Output: ' + o.decode('ascii'))
    #print('Error: '  + e.decode('ascii'))
    #print('code: ' + str(proc.returncode))
                      
              continue
            if s.find("QUEUE(")  is not -1 or  s.find("TYPE(") is not -1 :
              cl=s.split(" ")
              for x in cl:
                  if len(x) > 1:
    
                      
                      templist=x.split("(")
                      
                      if  len(templist) > 1:
                      
                        mylist.append({"{#"+templist[0]+"}":templist[1].replace(")","")})
                      #mylist.append(x)
    print mylist
    
    jslist=json.dumps(mylist)
    cmd = 'zabbix_sender -vv  -z 192.168.0.166 -s "ibm-queu-1" -k queu-test -o ' + '\''+jslist+'\''
    proc = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    #print o
    #print e
    
    
    
    #QUEUENAME
    
    
    
    
    import re
    for m in json.loads(jslist):
     
        if "{#QUEUE}" in dict(m):
            #print m["{#QUEUE}"]
            cmd = 'echo "DISPLAY '+x+'" | /opt/mqm/bin/runmqsc QM1' 
            #cmd='echo "DISPLAY QUEUE('+ m["{#QUEUE}"] +')" | /opt/mqm/bin/runmqsc  QM1 '
            cmd='echo "DISPLAY QUEUE('+ m["{#QUEUE}"] +')" | /opt/mqm/bin/runmqsc  '+qname
            proc = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            o, e = proc.communicate()
            h=o.replace(" ","\n")
            h=h.split("\n")
            for x in h :
                if x .find("MAXDEPTH") is not -1:
                    x1=re.findall('[0-9]+', x)
                    if x1:
                        #print x1
                        key=m["{#QUEUE}"]
                        #print m["{#QUEUE}"]
                        #cmd = 'zabbix_sender -vv  -z 192.168.0.166 -s "ibm-queu-1" -k "CheckQueue[{{"'+m["{#QUEUE}"]+'"}},QM1,CURDEPTH]"  -o ' + str(x1[0])
                        #cmd = 'zabbix_sender -vv  -z 192.168.0.166 -s "ibm-queu-1" -k "CheckQueue[{{'+key+'}},QM1,CURDEPTH]"  -o ' + str(x1[0])
                        #queuecheck["DEV.DEAD.LETTER.QUEUE",QM1,MAXDEPTH]
    
                        #cmd = 'zabbix_sender -vv  -z 192.168.0.166 -s "ibm-queu-1" -k ' + "queuecheck[DEV.DEAD.LETTER.QUEUE,QM1,MAXDEPTH]" + ' -o ' + str(x1[0])


                        #cmd = 'zabbix_sender -vv  -z 192.168.0.166 -s "ibm-queu-1" -k ' + "queuecheck["+key+",QM1,MAXDEPTH]" + ' -o ' + str(x1[0])
                        cmd = 'zabbix_sender -vv  -z 192.168.0.166 -s "ibm-queu-1" -k ' + "queuecheck["+key+","+qname+",MAXDEPTH]" + ' -o ' + str(x1[0])
                        #print cmd
                        proc = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        o, e = proc.communicate()
                        print o
                        print e
    
    
                if x .find("CURDEPTH") is not -1:
                    x1=re.findall('[0-9]+', x)
                    if x1:
                        #print x1
                        key=m["{#QUEUE}"]
                        #print m["{#QUEUE}"]
                        #cmd = 'zabbix_sender -vv  -z 192.168.0.166 -s "ibm-queu-1" -k "CheckQueue[{{"'+m["{#QUEUE}"]+'"}},QM1,CURDEPTH]"  -o ' + str(x1[0])
                        #cmd = 'zabbix_sender -vv  -z 192.168.0.166 -s "ibm-queu-1" -k "CheckQueue[{{'+key+'}},QM1,CURDEPTH]"  -o ' + str(x1[0])
                        #queuecheck["DEV.DEAD.LETTER.QUEUE",QM1,MAXDEPTH]
    
                        #cmd = 'zabbix_sender -vv  -z 192.168.0.166 -s "ibm-queu-1" -k ' + "queuecheck[DEV.DEAD.LETTER.QUEUE,QM1,MAXDEPTH]" + ' -o ' + str(x1[0])



                        #cmd = 'zabbix_sender -vv  -z 192.168.0.166 -s "ibm-queu-1" -k ' + "queuecheck["+key+",QM1,CURDEPTH]" + ' -o ' + str(x1[0])
                        cmd = 'zabbix_sender -vv  -z 192.168.0.166 -s "ibm-queu-1" -k ' + "queuecheck["+key+","+qname+",CURDEPTH]" + ' -o ' + str(x1[0])
                        #print cmd
                        proc = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        o, e = proc.communicate()
                        #print o
                        #print e
    #/opt/mqm/bin/dspmq -n
    
    
    
    
