import requests, pandas as pd,json,os
from flask import Flask, render_template,url_for,jsonify
from datetime import datetime, timedelta,timezone
from planilha_nordeste_nacional import salva_planilha

########################### CREDENCIAIS ############################
URL_PLANILHA=os.getenv("URL_PLANILHA") # URL DA PLANILHA PARA CHAMAR NO FRONT-END
URL_RASPADOR=os.getenv("URL_RASPADOR")
######################################################################

app=Flask(__name__,template_folder="templates")

# GATILHO WEBHOOK PELO PIPEDREAM (ATUALIZA PLANILHA)
@app.route(f"/{URL_RASPADOR}", methods=["GET"])
def raspador():

    data_raspagem=datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y às %Hh%M')
    with open ("atualizacao.json", "w") as f:
        f.write(json.dumps(data_raspagem, ensure_ascii=False))

    salva_planilha()
    
    return f"Dados raspados em {data_raspagem}"

@app.route("/")
def home():
    f=open("atualizacao.json")
    data_raspagem=json.load(f)
    # data_raspagem=datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y às %Hh%M')
    df=pd.read_csv(URL_PLANILHA)
    df["QNT_DIAS"] = (datetime.now() - pd.to_datetime(df["DATA_PUB"], format='%d/%m/%Y')).dt.days
    df=df.sort_values(by=["QNT_DIAS"])
    material_nordeste_json=df.to_json(orient="records",force_ascii=False,indent=4)
    material_nordeste=json.loads(material_nordeste_json)
    # for item in material_nordeste:
    #     item["QNT_DIAS"]=(datetime.now() - datetime.strptime(item["DATA_PUB"], '%d/%m/%Y')).days
    return render_template("index.html",material_nordeste=material_nordeste,data_raspagem=data_raspagem)

@app.route("/portfolio/home")
def portfolio_home():
    return render_template("index_portfolio.html")

@app.route("/portfolio/cursos")
def portfolio_cursos():
    return render_template("cursos_portfolio.html")

@app.route("/portfolio/bio")
def portfolio_bio():
    return render_template("bio_portfolio.html")

if __name__== "__main__":
    app.run(debug=True)
