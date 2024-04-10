# Nordeste Nacional
_Provisoriamente, este repositório está armazenando todos os exercícios finais da disciplina Automação do Master em Jornalismo de Dados, Automação e Storytelling do Insper._
<hr>

[ACESSE O NORDESTE NACIONAL AQUI](nordeste-nacional.onrender.com)

## **NAVEGUE PELO REPOSITÓRIO**
| **Exercício** | **Documentação** | **Repositório** |
------------|-------------- | --------- |
| Portfólio Parte 2 | [Portfólio Parte 2](https://github.com/cindydamasceno/nordestenacional#portf%C3%B3lio-parte-2) | [[LINK]](https://github.com/cindydamasceno/nordestenacional/blob/main/app.py) |
| Página Dinâmica | [Página Dinâmica](https://github.com/cindydamasceno/nordestenacional#p%C3%A1gina-din%C3%A2mica) | [[APP]](https://github.com/cindydamasceno/nordestenacional/blob/main/app.py)/[[RASPADOR]](https://github.com/cindydamasceno/nordestenacional/blob/main/nordeste_nacional.py) |
| Nordeste Nacional (Projeto final) | [Automatização e API Sheets](https://github.com/cindydamasceno/nordestenacional#automatiza%C3%A7%C3%A3o-e-api-sheets) | [[LINK]](https://github.com/cindydamasceno/nordestenacional/blob/main/planilha_nordeste_nacional.py) |

<hr>

### Portfólio (Parte 2)

Adaptação do portfólio de Paulo Fehlauer para `framework Flask`. Para armazenar imagens localmente no github foi utilizada a pasta `static` em paralelo à função `url_for`, nativa do framework. <br><br>
A apresentação do autor está dividida em três páginas: **projetos**, **cursos** e **bio**.
- Home ([/portfolio/home](https://nordeste-nacional.onrender.com/portfolio/home))
- Cursos ([/portfolio/cursos](https://nordeste-nacional.onrender.com/portfolio/cursos))
- Bio ([/portfolio/bio](https://nordeste-nacional.onrender.com/portfolio/bio))

<hr>
 
### Página dinâmica

O Nordeste Nacional traz diariamente as últimas dez citações aos estados nordestinos no Jornal Nacional. Por trás da ferramenta está um raspador que acessa, diariamente, a página do Jornal Nacional no g1 às 12h e seleciona as notícias com base em um filtro pré-definido. 

Este acesso utiliza gatilhos HTTP para agendar as raspagens. Uma url do Nordeste Nacional, omitida por questões de segurança, ativa o raspador ao ser acessada. Este processo faz parte de um sistema de comunicação entre duas ferramentas chamado _webhook_. O Nordeste nacional utiliza a plataforma Pipedream para agendar o acionador. 

A data da raspagem é armazenada em uma célula específica na Planilha e é atualizada no momento de acesso ao site. Esta informação é resgatado na página inicial a partir da variável `data_raspagem``. 

```Python
# CRIA VARIÁVEL DATA DE RASPAGEM NA FUNÇÃO obter_data_planilha

def salva_data():
    # CREDENCIAIS API SHEETS
    data=datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-3))).strftime("%d-%m-%Y-%Hh%M")
    conta = ServiceAccountCredentials.from_json_keyfile_name("KEY_SHEET.json") # CREDENCIAL
    api = gspread.authorize(conta)
    db = api.open_by_key(ID_SHEET)
    aba_data=db.get_worksheet(1) # SEGUNDA ABA PARA SALVAR SOMENTE A DATA
    aba_data.update_title(f"Data de atualização:{data}") # RENOMEIA PELA DATA DO LOOPING DO CODIGO
    print(f"Nome da aba: {aba_data}")

    # CRIAÇAO DE DATA
    data_raspador=datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y às %Hh%M')
    aba_data.update_cell(1,1,data_raspador)

    return aba_data

def obter_data_planilha():
    # CREDENCIAIS API SHEETS
    conta = ServiceAccountCredentials.from_json_keyfile_name("KEY_SHEET.json") # CREDENCIAL
    api = gspread.authorize(conta)
    db = api.open_by_key(ID_SHEET)
    aba_data = db.get_worksheet(1) # SEGUNDA ABA PARA A DATA
    data_raspagem = aba_data.cell(1, 1).value
    return data_raspagem


# GATILHO WEBHOOK PELO PIPEDREAM (ATUALIZA PLANILHA E SALVA DATA DE ATUALIZACAO)
@app.route(f"/{URL_RASPADOR}", methods=["GET"])
def raspador():
  salva_data()
  ....

@app.route("/")
def home():
    f=open("atualizacao.json")
    data_raspagem=json.load(f)
    ...
```

<hr>

### Automatização e API Sheets

O Nordeste Nacional não faz raspagem em tempo real a cada acesso à página inicial. Por trás da interface existe um banco de dados persistente, construído e atualizado em planilha Google Sheets. Esta escolha contorna possíveis problemas oriundos de falta de conexão com o g1, já que mantém uma armazenamento fixo independente do site. 

Desta forma, o que aparece para o usuário é consequência da última raspagem de informação. O robô adiciona à planilha somente reportagens novas, evitando a duplicidade de entradas a cada raspagem. As reportagens são, em seguida, organizadas da mais recente para a menos recente. 

```Python
#planilha_nordeste_nacional.py
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

  return planilha_atualizada

# ORGANIZA CONTEÚDO DA TABELA NA HOME (app.py):

def home():
    data_raspagem=obter_data_planilha()
    df=pd.read_csv(URL_PLANILHA)
    df["QNT_DIAS"] = (datetime.now() - pd.to_datetime(df["DATA_PUB"], format='%d/%m/%Y')).dt.days
    df=df.sort_values(by=["QNT_DIAS"])
    material_nordeste_json=df.to_json(orient="records",force_ascii=False,indent=4)
    material_nordeste=json.loads(material_nordeste_json)
    return render_template("index.html",material_nordeste=material_nordeste,data_raspagem=data_raspagem)

```

#### Como configurar o ambiente para este código

Certifique se adicionar em um arquivo `.env` as variáveis no seguinte formato:

```Python
ID_SHEET = "ENDERECO_PLANILHA_BANCO_PERSISTENTE"
KEY_SHEET = {CHAVE_API_SEM_QUEBRA_DE_LINHA}
URL_RASPADOR = "CAMINHO_PARA_ATIVAR_RASPADOR"
URL_PLANILHA = "URL_PLANILHA_EM_CSV"

```

#### Autentificação e variáveis de ambiente

```Python
# ATENÇÃO: ESTE CÓDIGO PODE APRESENTAR PROBLEMAS DE PERFORMANCE EM VERSÕES DO PYTHON SUPERIORES A 3.11.7

from dotenv import load_dotenv, find_dotenv

import os

load_dotenv()
find_dotenv()

ID_SHEET= os.getenv("ID_SHEET") # ENDEREÇO DA PLANILHA A SER EXPLORADA COMO BANCO PERSISTENTE

with open ("KEY_SHEET.json", "w") as f:
   f.write(os.environ["KEY_SHEET"]) # GERA UM ARQUIVO KEY_SHEET.json PARA SER ACHAMADO NO CÓDIGO
   
URL_PLANILHA=os.getenv("URL_PLANILHA") # URL DA PLANILHA PARA CHAMAR NO FRONT-END

URL_RASPADOR=os.getenv("URL_RASPADOR")

```

#### Filtragem 
Este protótipo considera apenas reportagens categorizadas como `type=materias` no site do [Jornal Nacional do G1](http://g1.globo.com/jornal-nacional/). 

Nomenclaturas e variações dos estados nordestinos: 
```Python
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

```
