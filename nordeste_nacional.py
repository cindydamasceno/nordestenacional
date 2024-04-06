import pandas as pd, requests, json
from datetime import datetime, timedelta,timezone
import pendulum # CONVERTE FUSOHORÁRIOS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

titulos = []
datas = []
sumarios = []
links = []
videos = []

def lista_nordeste():
  referencias = [ # UF E CAPITAIS
              "Alagoas","AL", "Maceió",
              "Bahia","BA","Salvador",
              "Ceará","CE","Fortaleza",
              "Maranhão","MA",
              "Paraíba","PB",
              "Pernambuco","PE","Recife",
              "Piauí","PI","Teresina",
              "RN","Natal", # RETIRA MENÇÕES AO FERIADO NATALINO AO COLOCAR NATAL EM MAIÚSCULO
              "Sergipe","SE","Aracaju",
              "Nordeste","NE"] # PROCURA POR REFERÊNCIAS DIRETAS AO NORDESTE, TAMBÉM
  referencias_composto=["São Luís",
                       "João Pessoa",
                       "Rio Grande do Norte",
  ]
  return referencias, referencias_composto 

def procura_nordeste():
  referencias_encontradas = 0
  pg = 1 # API COMEÇA NA PAGINA 1
  while referencias_encontradas < 10:
      referencias,referencias_composto=lista_nordeste()
      print(f"Estou na página {pg}")
      url = f"https://falkor-cda.bastian.globo.com/tenants/g1/instances/f25a60a6-fee2-43db-b6f3-25c91d636aba/posts/page/{pg}"
      raspa = requests.get(url).json()
      
      for item in raspa["items"]:
          if item["type"] == "materia":
              titulo = item["content"]["title"]
              # EVITA PEGAR SUBSTRINGS SEM AFETAR NOMES COMPOSTOS
              if any(referencia in titulo.split() for referencia in referencias) \
                  or any(referencia_composto in titulo for referencia_composto in referencias_composto): 
                  print(f"Referência encontrada: {titulo}") 
                  referencias_encontradas += 1
                  
                  data = pendulum.parse(item["publication"]).in_timezone('America/Sao_Paulo').strftime("%d/%m/%Y")
                  link = item["content"]["url"]
                  titulos.append(titulo)
                  datas.append(data)
                  links.append(link)
                  
                  if "summary" in item["content"]:
                      sumario = item["content"]["summary"]
                      sumarios.append(sumario)
                  else:
                      sumarios.append(None)
                      
                  if referencias_encontradas >= 10:
                      break
      
      pg += 1
  return titulos,datas,sumarios,links