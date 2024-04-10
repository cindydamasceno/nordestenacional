import pandas as pd
from datetime import datetime, timedelta,timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

from nordeste_nacional import procura_nordeste

########################### CREDENCIAIS ############################
ID_SHEET=os.getenv("ID_SHEET")

with open ("KEY_SHEET.json", "w") as f:
   f.write(os.environ["KEY_SHEET"])
######################################################################
   
## CRIA PLANILHA
def formata_planilha():
    # CREDENCIAIS API SHEETS
    data=datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-3))).strftime("%d-%m-%Y-%Hh%M")
    conta = ServiceAccountCredentials.from_json_keyfile_name("KEY_SHEET.json") # CREDENCIAL
    api = gspread.authorize(conta)
    db = api.open_by_key(ID_SHEET)
    aba=db.sheet1 #ABA COM DADOS
    aba.update_title(data) # RENOMEIA PELA DATA DO LOOPING DO CODIGO
    print(f"Nome da aba: {aba}")

    # CRIAÇAO DE CABEÇALHO
    cabecalho=["DATA_PUB", "TITULO", "LINHA-FINA", "URL"]
    if cabecalho not in aba.get_all_values():
       aba.append_row(cabecalho)
    else:
      print("-----------CABEÇALHO ADICIONADO-----------")

    return aba

## CRIA DF COM RASPAGEM
def df_nordeste():
  titulos,datas,sumarios,links=procura_nordeste()
  df_nordeste=pd.DataFrame({
                            'DATA_PUB':datas,
                            'TITULO':titulos,
                            'LINHA-FINA':sumarios,
                            'URL':links,
  })

  return df_nordeste

def salva_planilha():
  data_raspagem=datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y às %Hh%M')
  aba=formata_planilha()
  df=df_nordeste()
  planilha=pd.DataFrame(aba.get_all_records()) # LÊ COMO DATAFRAME

  # TRANSFORMA CADA LINHA EM LISTA PARA VERIFICAÇÃO E ADIÇÃO EM LOTE
  dados_planilha=planilha.values.tolist()
  dados_raspados=[linha.tolist() for index, linha in df.iterrows()]
  dados_novos=[linha for linha in dados_raspados if linha not in dados_planilha]
  
  #  ADICIONA SOMENTE OS DADOS NOVOS NAS PLANILHAS
  print("-----------IMPRIMINDO DADOS ADICIONADOS-----------")
  print(dados_novos)

  try:
    aba.append_rows(dados_novos)
    print(f"Dados adicionados na planilha:{data_raspagem}")
  except Exception as e:
    print("Nenhum dado novo adicionado na planilha:",str(e))
  
  planilha_atualizada=pd.DataFrame(aba.get_all_records()) # DATAFRAME DA VERSÃO NOVA
  planilha_atualizada["DATA_PUB"]=pd.to_datetime(planilha_atualizada["DATA_PUB"])
  planilha_organizada=planilha_atualizada.sort_values(by=["DATA_PUB"])

  return planilha_organizada
