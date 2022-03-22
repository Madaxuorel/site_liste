from flask import Flask, render_template, request, redirect,url_for  #importing flask elements to make everything work
app = Flask(__name__)

import pyrebase
import string
import datetime

config={
  "apiKey": "AIzaSyAI0KK-ff21JLuLIDhVbBcwfDh63HfoDCY",
  "authDomain": "site-liste-hydra-e6a25.firebaseapp.com",
  "projectId": "site-liste-hydra-e6a25",
  "storageBucket": "site-liste-hydra-e6a25.appspot.com",
  "messagingSenderId": "809157089116",
  "appId": "1:809157089116:web:a45f65cdcb6f2aff409399",
  "measurementId": "G-VQ33YWV56V",
  "databaseURL" : "https://site-liste-hydra-e6a25-default-rtdb.europe-west1.firebasedatabase.app/"
}


    

def getdbAF():
  #Va chercher des defis à faire dans la DB
    firebase=pyrebase.initialize_app(config)
    authe = firebase.auth()
    database=firebase.database()
    all_defis = database.child("defis").get()
    defilist=[]
    for defi in all_defis:
     
      if defi.key() != 'defi0' :
        
        defilist.append(defi)
       
      
    return defilist

def getdbDone():
  #va chercher les défis faits dans la DB
    firebase=pyrebase.initialize_app(config)
    authe = firebase.auth()
    database=firebase.database()
    all_defis = database.child("done").get()
    defilist=[]
    for defi in all_defis:
          if defi.key() != 'done0':
              defilist.append(defi)
    return defilist


@app.route("/")
def hello():
  allAF = getdbAF()
  allDone = getdbDone()
  print(all)
  return render_template("admin.html",allAF=allAF, allDone=allDone)

def formatall(all):
  i=0
  for a in all:

    all[i]=a.split(":")[1].replace("'","").replace("'","").replace("}","")
    i+=1
  
  return all

@app.route('/delete', methods=['POST'])
def delete():
  count=request.form['donecount']
  
  firebase=pyrebase.initialize_app(config)
  authe = firebase.auth()
  database=firebase.database()

  database.child("done").child("done{}".format(count)).remove()
  c=database.child("donecount").get().val() - 1
  database.child("donecount").set(c)

  return redirect('/')

@app.route('/done', methods=['POST'])
def my_link():
  data = request.form['data']#raw data
  lien = request.form['lien']
  dataformat = str(data).split(',')#data formaté par catégorie

  dataformat = formatall(dataformat)


  firebase=pyrebase.initialize_app(config)
  authe = firebase.auth()
  database=firebase.database()

  #remove defi :
  nom="defi{}".format(dataformat[0].replace(" ",""))
  print(dataformat)
  database.child("defis").child(nom).remove()
  
  #add defi à done:
  n=database.child("donecount").get().val()
  done={"titre":dataformat[6], "desc":dataformat[2], "date":dataformat[1], "donenu":len(database.child('done').get().val())-1, "lienvid":lien, "donneur":dataformat[4],"datedone":str(datetime.datetime.now()), "donecount":n}
  
  database.child("done").child("done{}".format(n)).set(done)
  
  #incrément donecount
  t=database.child("donecount").get().val()
  
  database.child("donecount").set(t+1)
  #redirect vers admin.html
  redirect('/')

  return redirect('/')
  
if __name__ == '__main__':
  app.run(debug=True)