import requests, pandas as pd,json,os
from flask import Flask, render_template,url_for,jsonify
from datetime import datetime, timedelta,timezone
from planilha_nordeste_nacional import salva_planilha

########################### CREDENCIAIS ############################
URL_PLANILHA=os.getenv("URL_PLANILHA") # URL DA PLANILHA PARA CHAMAR NO FRONT-END
URL_RASPADOR=os.getenv("URL_RASPADOR")
######################################################################

app=Flask(__name__,template_folder="templates")

# CRIA VARIÁVEL GLOBAL COM A DATA DE RASPAGEM
data_raspagem=None

# GATILHO WEBHOOK PELO PIPEDREAM (ATUALIZA PLANILHA)
@app.route(f"/{URL_RASPADOR}", methods=["GET"])
def raspador():
    global data_raspagem # ARMAZENA O VALOR NA VARIÁVEL data_raspagem 
    data_raspagem=datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y às %Hh%M')
    salva_planilha()
    
    return f"Dados raspados em {data}"

@app.route("/")
def home():
    global data_raspagem
    # data_raspagem=datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y às %Hh%M')
    df=pd.read_csv(URL_PLANILHA)
    material_nordeste_json=df.to_json(orient="records",force_ascii=False,indent=4)
    material_nordeste=json.loads(material_nordeste_json)
    for item in material_nordeste:
        item["QNT_DIAS"]=(datetime.now() - datetime.strptime(item["DATA_PUB"], '%d/%m/%Y')).days
    return render_template("index.html",material_nordeste=material_nordeste,data_raspagem=data_raspagem)

if __name__== "__main__":
    app.run(debug=True)
