import requests, pandas as pd,json,os
from flask import Flask, render_template,url_for,jsonify
from datetime import datetime, timedelta,timezone
from planilha_nordeste_nacional import salva_planilha

########################### CREDENCIAIS ############################
from dotenv import load_dotenv,find_dotenv
load_dotenv()
URL_PLANILHA=os.getenv("URL_PLANILHA") # URL DA PLANILHA PARA CHAMAR NO FRONT-END
URL_RASPADOR=os.getenv("URL_RASPADOR")
######################################################################

app=Flask(__name__,template_folder="templates")

# GATILHO WEBHOOK PELO PIPEDREAM (ATUALIZA PLANILHA)
@app.route(f"/{URL_RASPADOR}", methods=["GET"])
def raspador():
    data=datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y às %Hh%M')
    salva_planilha()
    
    return f"Dados raspados em {data}"

@app.route("/")
def home():
    data=datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y às %Hh%M')
    df=pd.read_csv(URL_PLANILHA)
    material_nordeste_json=df.to_json(orient="records",force_ascii=False,indent=4)
    material_nordeste=json.loads(material_nordeste_json)
    for item in material_nordeste:
        item["QNT_DIAS"]=(datetime.now() - datetime.strptime(item["DATA_PUB"], '%d/%m/%Y')).days
    return render_template("index.html",material_nordeste=material_nordeste,data=data)

if __name__== "__main__":
    app.run(debug=True)