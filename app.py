from flask import Flask, render_template, request, redirect

#Huom! ei yleisesti suositeltavaa käyttää import *, vaan tuoda vain ne tiedot, joita tarvitaan
# import * >näin voidaan kutsua moduulin funktioita ilman moduulin nimeä, katso rivi 11
from mongo_connection import * 

# Initialisoidaan ohjelma Flask-applikaatioksi:
app = Flask (__name__) # __name__ n paikalle menee tiedoston nimen etuosa 

# kutsutaan mongo_connection -moduulin connect-metodia suoraan
client = connect()

# asetetaan tietokanta (luodaan jos sen nimistä ei löydy)
db=client["taskDB"]                 
# asetetaan collection (luodaan jos sen nimistä ei löydy)
coll=db["task_collection"]          

# määritellään reitti localhost:5000/ -osoitteeseen (portti 5000 oletus, jos sitä ei muuta)
@app.route('/')
def index():
    ### HAE TASKS-MUUTTUJAAN KAIKKI TASKIT TIETOKANNASTA (VINKKI: KONVERTOI KURSORI LISTAKSI)
    tasks=None # 
    return render_template('index.html',all_tasks=tasks) #hakee oletuksena templates-kansiosta

# Kun käyttäjä on syöttänyt tekstiä index.html -sivun tekstikentään ja painaa Add-nappia, mennään tähän reittiin
@app.route('/add', methods=['POST']) 
def add_task():
    task = request.form['task'] # haetaan index.html -sivun formista task-nimisen kentän teksti muuttujaan
    new_id = fetch_new_id(coll) ### MUOKKAA FUNKTIO TOIMIVAKSI
    ### LISÄÄ TIETOKANTAAN UUSI TIETUE, JOSSA SIJOITAT :
    ### id-kenttään new_id-muuttujan
    ### task-kenttään task-muuttujan
    ### isComplete-kenttään False
    
    # lopuksi ohjataan käyttäjä takaisin aloitussivulle
    return redirect('/') 


@app.route('/update/<int:task_id>', methods=['POST','GET'])
def update_task(task_id):
    if request.method=='GET': # käyttäjä painaa Update-nappia index.html -sivulla
        task = fetch_task_by_id(coll,task_id) # MUOKKAA FUNKTIO TOIMIVAKSI
        return render_template("update.html",task=task)        
    elif request.method=='POST': # käyttäjä painaa Update-nappia update.html -sivulla
        task = request.form['task']    
        # PÄIVITÄ TASK TIETOKANTAAN
        return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    # POISTA TASK TIETOKANNASTA task_id -TIEDON PERUSTEELLA   
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True) # debug=True toimii, jos ajetaan python app.py
                        # jos ajetaan flask-komennolla,
                        # pitää ajaa flask run --debug
 
