# Nordeste Nacional
_Provisoriamente, este repositório está armazenando todos os exercícios finais da disciplina Automação do Master em Jornalismo de Dados, Automação e Storytelling do Insper._
<hr>

## **NAVEGUE PELO REPOSITÓRIO**
| **Exercício** | **Documentação** | **Repositório** |
------------|-------------- | --------- |
| Portfólio Parte 2 | [Portfólio Parte 2](https://github.com/cindydamasceno/nordestenacional/edit/main/README.md#p%C3%A1gina-din%C3%A2mica) | [LINK] |
| Página Dinâmica | [Página Dinâmica](https://github.com/cindydamasceno/nordestenacional/edit/main/README.md#p%C3%A1gina-din%C3%A2mica) | [LINK] |
| Nordeste Nacional | [Automatização e API Sheets](https://github.com/cindydamasceno/nordestenacional/edit/main/README.md#p%C3%A1gina-din%C3%A2mica) | [LINK] |

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

Este acesso utiliza webhook para agendar as raspagens. Uma url do Nordeste Nacional, omitida por questões de segurança, ativa o raspador ao ser acessada. Este processo faz parte de um sistema de comunicação entre duas ferramentas chamado _webhook_. O Nordeste nacional utiliza a plataforma Pipedream para agendar o acionador. 
<hr>

### Automatização e API Sheets

O Nordeste Nacional não faz raspagem em tempo real a cada acesso à home. Por trás da página há um banco de dados persistente, construído em planilha Google Sheets. Desta forma, o que aparece para o usuário é consequência da última raspagem de informação. 

Esta escolha contorna possíveis problemas oriundos de falta de conexão com a página. 

#### Como rodar este código

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

## VARIÁVEIS DE AMBIENTE
import os

ID_SHEET= os.getenv("ID_SHEET") # ENDEREÇO DA PLANILHA A SER EXPLORADA COMO BANCO PERSISTENTE

with open ("KEY_SHEET.json", "w") as f:
   f.write(os.environ["KEY_SHEET"]) # GERA UM ARQUIVO KEY_SHEET.json PARA SER ACHAMADO NO CÓDIGO

URL_PLANILHA=os.getenv("URL_PLANILHA") # URL DA PLANILHA PARA CHAMAR NO FRONT-END

URL_RASPADOR=os.getenv("URL_RASPADOR")

```

#### Filtragem 


### Adaptações e segurança

