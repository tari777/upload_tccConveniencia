from calendar import month
from math import prod
import os
from sqlite3.dbapi2 import Error
from tkinter.constants import TRUE
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Button, popup
from playsound import playsound
import sqlite3
from PIL import Image
from datetime import datetime
import pandas as pd
from datetime import datetime

total = 0
prod_venda_nome = ''
prod_venda_desc = ''
prod_venda_qntd = ''
prod_venda_entrada = ''
prod_venda_unitario = ''
testo = 'fodase'
i = 0
x = 0
tabelVendas = []
if not os.path.exists('C:/pastaTCC'):
    os.makedirs('C:/pastaTCC')
banco = sqlite3.connect('C:/pastaTCC/tcc_database.db')
#banco = sqlite3.connect("C:/Users/mathe/Desktop/tcc conveniencia/tcc_database.db") 
#data = pd.read_sql_query("SELECT * from produtos", banco)
#print(data[data['valor_total'] == 25]) #PROCURA ONDE VALOR TOTAL = 24

cursor = banco.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS produtos (cod_produto INTEGER PRIMARY KEY AUTOINCREMENT, nome text, quantidade real, cod_barras text, desc text, ncm text, icms text, valor_entrada float, valor_unitario float, valor_total float)")
cursor.execute("CREATE TABLE IF NOT EXISTS fornecedores (cod_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT, nome text, razao_social text, rua text, cep text, bairro text, numero text, cidade text, estado text, complemento text, cnpj text, insc_estadual text, telefone text)")
cursor.execute("CREATE TABLE IF NOT EXISTS entrada (nmr_nota_fiscal TEXT PRIMARY KEY, nome text, nome_fornecedor text, cod_barras text, quantidade integer, data_entrada text, valor_unitario real, valor_total real)")
cursor.execute("CREATE TABLE IF NOT EXISTS saida (nmr_nota_fiscal INTEGER, nome text, cod_barras text, quantidade integer, data_saida text, valor_unitario real, valor_total real)")
cursor.execute("CREATE TABLE IF NOT EXISTS conveniencia (razao_social TEXT PRIMARY KEY, nome text, nome_fantasia text, rua text, cep text, bairro text, numero text, cidade text, estado text, complemento text,  cnpj text, insc_estadual text, telefone text)")

def on_table_row_click(self, table, row, item):
            index = -1
            #each widget (and specifically in this case the table) has a _render_children_list attribute that
            # is an ordered list of the children keys
            #first, we search for the row in the children dictionary
            for key, value in table.children.items():
                 if value == row:
                     #if the row is found, we get the index in the ordered list
                     index = table._render_children_list.index(key)
            print(index)

def janelaMain():
    menu_def = [
        ['&Cadastro', ['&Cadastrar Entrada', '&Cadastrar Produto', '&Cadastrar Fornecedor']],
        ['&Venda', ['&Vender Produto']],
        ['&Consulta', ['&Consultar Entrada', '&Consultar Produtos']],
        ['&Faturamento', ['&Ver Faturamento']],
        ['&Fornecedores', ['&Ver Fornecedores']],
        ['&Compras', ['&Ver Compras']],
        ['&Configurações', ['&Informações', 'Backup']]
    ]
    sg.theme('Reddit')
    sg.theme_text_color() #COR DO TEXTO
    sg.theme_background_color()
   
    layout = [
        [sg.Menu(menu_def, tearoff=False, key='-MENU BAR-')],
        [sg.Text('Sistema de Cadastro')],
        [sg.Frame('AAAAAAA', [[ sg.Image('gay.png')]])]
        #[sg.Listbox(name,size = (30,10), key='box')],
    ]
    return sg.Window('Tela Lista', layout=layout, size=(700,500), element_justification='center', finalize = True)


def cadastrarEntrada():
    sg.theme('Reddit')
    layout = [
        [sg.Text('Cadastro de Entrada')],
        #Mesma linha
        [sg.Frame('Nome Produto',[ [sg.Input(key='nome_produto', size=(15,30))]],title_color='black', title_location='n'), 
            sg.Frame('Quantidade',[ [sg.Input(key='qnt_produto', size=(15,30))]],title_location='n'),   
            sg.Frame('Nome Fornecedor',[ [sg.Input(key='nome_fornecedor', size=(15,70))]], title_location='n'),
            ],
        [sg.Frame('Número Nota Fiscal',[ [sg.Input(key='nmr_notafiscal', size=(15,30))]], title_location='n'), 
            sg.Frame('Código de Barras',[ [sg.Input(key='cod_barra', size=(15,30))]], title_location='n'), 
            sg.Frame('Data',[ [sg.Input(key='data_produto', size=(20,70)), sg.Button('Date', key='data_entrada')]], title_location='n'),
            ],
        [sg.Frame('Valor Unitário',[ [sg.Input(key='valor_unitario', size=(15,30))]], title_location='n')],
        [sg.Table(tabelaVendas, key = 'box_vendas', headings=['Nota Fiscal','Nome', 'Quantidade', 'Nome Fornecedor', 'Código Barras','Data', 'Valor Unitário', 'Valor Total'], auto_size_columns=False, col_widths=[10], vertical_scroll_only=False)],
        
        
        [sg.Button('Cadastrar',pad=(10,30))],
    ]
    return sg.Window('Cadastro', layout=layout, size=(600,500), element_justification='center', finalize = True)

def cadastrarProduto():
    sg.theme('Reddit')
    layout = [
        [sg.Text('Cadastro de Produto')],
        #Mesma linha
        [sg.Frame('Nome Produto',[ [sg.Input(key='nome_produto', size=(15,30))]],title_color='black', title_location='n'), 
            sg.Frame('Quantidade',[ [sg.Input(key='qnt_produto', size=(15,30))]],title_location='n'),   
            sg.Frame('Código de Barras',[ [sg.Input(key='cod_barra', size=(15,30))]], title_location='n'),
            ],
        [sg.Frame('NCM',[ [sg.Input(key='nmr_ncm', size=(15,30))]], title_location='n'), 
            sg.Frame('ICMS',[ [sg.Input(key='nmr_icms', size=(10,30))]],title_location='n'),
            ], 
        [sg.Frame('Valor Entrada', [ [sg.Input(key='valor_entrada', size=(15,30))]], title_location='n'),
         sg.Frame('Valor Unitário',[ [sg.Input(key='valor_unitario', size=(15,30))]], title_location='n')
        ],
        [sg.Frame('Descrição',[ [sg.Multiline(key='desc_produto', size=(35,3))]],  title_location='n')],
       
        
        [sg.Button('Cadastrar', key='cadastrar_produto',pad=(10,30))],
    ]
    return sg.Window('Cadastro', layout=layout, size=(600,400), element_justification='center', finalize = True)

def cadastrarFornecedor():
    sg.theme('Reddit')
    layout = [
        [sg.Text('Cadastro de Fornecedor')],
        #Mesma linha
        [sg.Frame('Nome',[ [sg.Input(key='nome_fornecedor', size=(15,30))]],title_color='black', title_location='n'), 
            sg.Frame('Razão Social',[ [sg.Input(key='razao_social_fornecedor', size=(15,30))]],title_location='n'),   
            sg.Frame('Rua',[ [sg.Input(key='rua_fornecedor', size=(15,30))]], title_location='n'),
            ],
        [sg.Frame('CEP',[ [sg.Input(key='cep_fornecedor', size=(10,30))]], title_location='n'), 
            sg.Frame('Bairro',[ [sg.Input(key='bairro_fornecedor', size=(17,30))]],title_location='n'),
            sg.Frame('Número', [ [sg.Input(key='numero_fornecedor', size=(15,30))]], title_location='n'),
            ], 
        [sg.Frame('Cidade',[ [sg.Input(key='cidade_fornecedor', size=(15,30))]], title_location='n'),
         sg.Frame('Estado',[ [sg.Combo(values=('SP', 'AC', 'RJ'), default_value='SP',  key='estado_fornecedor'),]],  title_location='n'),
         sg.Frame('Complemento',[ [sg.Input(key='complemento_fornecedor', size=(15,30))]],  title_location='n'),
            ],
        [sg.Frame('CNPJ',[ [sg.Input(key='cnpj_fornecedor', size=(15,30))]],  title_location='n'),
         sg.Frame('Inscrição Estadual',[ [sg.Input(key='ie_fornecedor', size=(15,30))]],  title_location='n'),
         sg.Frame('Telefone',[ [sg.Input(key='telefone_fornecedor', size=(15,30))]],  title_location='n')
        ],
      
       
        
        [sg.Button('Cadastrar', key='cadastrar_fornecedor',pad=(10,30))],
    ]
    return sg.Window('Cadastro', layout=layout, size=(600,400), element_justification='center', finalize = True)

def editarProduto():
    sg.theme('Reddit')
    layout = [
        [sg.Text('Editar produto')],
        #Mesma linha
        [sg.Frame('Nome Produto',[ [sg.Input(prod_nome_produto,key='nome_produto', size=(15,30))]],title_color='black', title_location='n'), 
            sg.Frame('Quantidade',[ [sg.Input(prod_qnt_produto,key='qnt_produto', size=(15,30))]],title_location='n'),   
            sg.Frame('Código de Barras',[ [sg.Input(prod_cod_barra,key='cod_barra', size=(15,30))]], title_location='n'),
            ],
        [sg.Frame('NCM',[ [sg.Input(prod_nmr_ncm,key='nmr_ncm', size=(15,30))]], title_location='n'), 
            sg.Frame('ICMS',[ [sg.Input(prod_nmr_icms,key='nmr_icms', size=(10,30))]],title_location='n'),
            ], 
        [sg.Frame('Valor Entrada', [ [sg.Input(prod_valor_entrada,key='valor_entrada', size=(15,30))]], title_location='n'),
         sg.Frame('Valor Unitário',[ [sg.Input(prod_valor_unitario,key='valor_unitario', size=(15,30))]], title_location='n')
        ],
        [sg.Frame('Descrição',[ [sg.Multiline(prod_desc_produto,key='desc_produto', size=(35,3))]],  title_location='n')],
       
        
        [sg.Button('Alterar', key='alterar_produto',pad=(10,30))],
    ]
    return sg.Window('Editar produto', layout=layout, size=(600,400), element_justification='center', finalize = True)


def add_entrada():
    ent_nome_produto = values['nome_produto']
    ent_qnt_produto = values['qnt_produto']
    ent_nome_fornecedor = values['nome_fornecedor']
    ent_nmr_notafiscal = values['nmr_notafiscal']
    ent_cod_barra = values['cod_barra']
    ent_data_produto = values['data_produto']
    ent_valor_entrada = values['valor_entrada']
    ent_valor_unitario = values['valor_unitario']
    if ent_nome_produto and ent_qnt_produto and ent_nome_fornecedor and ent_nmr_notafiscal and ent_cod_barra and ent_data_produto and ent_valor_entrada and ent_valor_unitario != '':
        try: #TRATAMENTO DE ERRO
            ent_valor_total = float(ent_valor_unitario) * float(ent_qnt_produto)
            cursor.execute(f"INSERT INTO entrada VALUES('{ent_nmr_notafiscal}', '{ent_nome_produto}','{ent_nome_fornecedor}','{ent_qnt_produto}','{ent_data_produto}', '{ent_valor_entrada}','{ent_valor_unitario}','{ent_valor_total}')")
            banco.commit()
            sg.popup("Entrada cadastrada com sucesso!", title="Sucesso")
        except ValueError as erro:
            sg.popup("Algum campo foi preenchido errado!")
        except sqlite3.IntegrityError as erro:
            sg.popup ("O campo [NÚMERO NOTA FISCAL] já existe no sistema!")
    else:
        sg.popup("Erro de cadastro: Existem campos vázios", title='ERRO')

def add_produto():
    prod_nome_produto = values['nome_produto']
    prod_qnt_produto = values['qnt_produto']
    prod_cod_barra = values['cod_barra']
    prod_nmr_ncm = values['nmr_ncm']
    prod_nmr_icms = values['nmr_icms']
    prod_desc_produto = values['desc_produto']
    prod_valor_entrada = values['valor_entrada']
    prod_valor_unitario = values['valor_unitario']
    if prod_nome_produto and prod_qnt_produto and prod_cod_barra and prod_nmr_ncm and prod_nmr_icms and prod_desc_produto and prod_valor_entrada and prod_valor_unitario != '':
        try: #TRATAMENTO DE ERRO
            cursor.execute('SELECT * FROM produtos WHERE nome = ? OR cod_barras = ?', (prod_nome_produto, prod_cod_barra))
            if cursor.fetchall():
                sg.popup('Erro: Produto já cadastrado no sistema!')
            else:
                prod_valor_total = float(prod_valor_unitario) * float(prod_qnt_produto)
                cursor.execute(f"INSERT INTO produtos VALUES(Null, '{prod_nome_produto}', '{prod_qnt_produto}', '{prod_cod_barra}', '{prod_desc_produto}', '{prod_nmr_ncm}', '{prod_nmr_icms}', '{prod_valor_entrada}',' {prod_valor_unitario}', '{prod_valor_total}')")
                banco.commit()
                sg.popup("Produto cadastrado com sucesso!", title="Sucesso")
        except ValueError as erro:
            sg.popup("Algum campo foi preenchido errado!")
            print(erro)
    else:
        sg.popup("Erro de cadastro: Existem campos vázios", title='ERRO')
def add_fornecedor():
    nome_fornecedor = values['nome_fornecedor']
    razao_social_fornecedor = values['razao_social_fornecedor']
    rua_fornecedor = values['rua_fornecedor']
    cep_fornecedor = values['cep_fornecedor']
    bairro_fornecedor = values['bairro_fornecedor']
    numero_fornecedor = values['numero_fornecedor']
    cidade_fornecedor = values['cidade_fornecedor']
    estado_fornecedor = values['estado_fornecedor']
    complemento_fornecedor = values['complemento_fornecedor']
    cnpj_fornecedor = values['cnpj_fornecedor']
    ie_fornecedor = values['ie_fornecedor']
    telefone_fornecedor = values['telefone_fornecedor']
    if nome_fornecedor and razao_social_fornecedor and rua_fornecedor and cep_fornecedor and bairro_fornecedor and numero_fornecedor and cidade_fornecedor and estado_fornecedor and complemento_fornecedor and cnpj_fornecedor and ie_fornecedor and telefone_fornecedor != '':
        try:
            cursor.execute('SELECT * FROM fornecedores WHERE nome = ? OR cnpj = ?', (nome_fornecedor, cnpj_fornecedor))
            if cursor.fetchall():
                sg.popup('Erro: Fornecedor já cadastrado no sistema!')
            else:
                cursor.execute(f"INSERT INTO fornecedores VALUES(Null, '{nome_fornecedor}', '{razao_social_fornecedor}', '{rua_fornecedor}', '{cep_fornecedor}', '{bairro_fornecedor}', '{numero_fornecedor}', '{cidade_fornecedor}', '{estado_fornecedor}', '{complemento_fornecedor}', '{cnpj_fornecedor}', '{ie_fornecedor}', '{telefone_fornecedor}')")
                banco.commit()
                sg.popup("Fornecedor cadastrado com sucesso!", title="Sucesso")
        except ValueError as erro:
            sg.popup("Algum campo foi preenchido errado!")
            print(erro)
    else:
        sg.popup("Erro de cadastro: Existem campos vázios", title='ERRO')

                
def consultaFornecedores():
    sg.theme('Reddit')
    layout2 = [
        [sg.Button('Voltar', key='voltar_fornecedor')],
        [sg.Text('Produtos cadastrados')],
        [sg.Table(tabelaFornecedores, size = (500,15), key='box_fornecedor',headings=['CódigoForn','Nome', 'Razão', 'Rua', 'CEP', 'Bairro', 'Número', 'Cidade','Estado', 'Complemento', 'Cnpj', 'IE', 'Telefone'],auto_size_columns=True,max_col_width=35, vertical_scroll_only=False)],
        [sg.Button('Filtra', key='nomesfiltrar_fornecedor'),sg.Button('Tirar Filtro', key='tirarFiltro_fornecedor'), sg.Button('Selecionar', key = 'select_fornecedor'), sg.Button('Deletar', key ='delete_fornecedor'), sg.Button('Editar', key='edit_fornecedor')],
        [sg.Input(key='filtroProcurar_fornecedor')],
        [sg.Radio('ID','filters',key = 'radioID_fornecedor', default=True), sg.Radio('Nome','filters',key = 'radioNome_fornecedor'), sg.Radio('CNPJ','filters',key = 'radioCNPJ_fornecedor')]
    ]   

    return sg.Window('Tela Lista', layout=layout2, size=(800,500), element_justification='center', finalize = True)

def consultaProdutos():
    sg.theme('Reddit')
    layout2 = [
        [sg.Button('Voltar')],
        [sg.Text('Produtos cadastrados')],
        [sg.Table(tabelaProdutos, size = (500,15), key='box',headings=['CódigoProd','Nome', 'Quantidade', 'Cod_barras', 'Descrição', 'NCM', 'ICMS', 'Valor_Entrada','Valor_Uni', 'Valor_Total'],auto_size_columns=True,max_col_width=35, vertical_scroll_only=False)],
        [sg.Button('Filtra', key='nomesfiltrar'),sg.Button('Tirar Filtro', key='tirarFiltro'), sg.Button('Selecionar', key = 'select'), sg.Button('Deletar', key ='delete'), sg.Button('Editar', key='edit')],
        [sg.Input(key='filtroProcurar')],
        [sg.Radio('ID','filters',key = 'radioID', default=True), sg.Radio('Nome','filters',key = 'radioNome'), sg.Radio('CodBarras','filters',key = 'radioCODBARRAS')]
    ]   

    return sg.Window('Tela Lista', layout=layout2, size=(800,500), element_justification='center', finalize = True)

def consultaProdutosVenda():
    sg.theme('Reddit')
    layout2 = [
        [sg.Text('Produtos cadastrados')],
        [sg.Table(tabelaProdutos, size = (500,15), key='box_produtos_venda',headings=['CódigoProd','Nome', 'Quantidade', 'Cod_barras', 'Descrição', 'NCM', 'ICMS', 'Valor_Entrada','Valor_Uni', 'Valor_Total'],auto_size_columns=True,max_col_width=35, vertical_scroll_only=False)],
        [sg.Button('Filtra', key='nomesfiltrar'),sg.Button('Tirar Filtro', key='tirarFiltro'), sg.Button('Selecionar', key = 'select_vendas')],
        [sg.Input(key='filtroProcurar')],
        [sg.Radio('ID','filters',key = 'radioID', default=True), sg.Radio('Nome','filters',key = 'radioNome'), sg.Radio('CodBarras','filters',key = 'radioCODBARRAS')]
    ]   

    return sg.Window('Tela Lista', layout=layout2, size=(800,500), element_justification='center', finalize = True)

def venderProduto():
    sg.theme('Reddit')
    layout = [
        [sg.Text('Venda')],
        #Mesma linha
        [sg.Frame('Nome Produto',[ [sg.Button('Abrir',key = 'abrir_produtos', size = (5,1)), sg.Input(prod_venda_nome,key='nome_produto_venda', size=(15,30), readonly=True)]],title_color='black', title_location='n'), 
            sg.Frame('Código Barra', [ [ sg.Button('F5', key = 'procurar_cod_barra', size = (2,1)), sg.Input(prod_venda_entrada, key = 'cod_barra_venda', size=(15,30))]], title_location= 'n'),
            sg.Frame('Descrição', [ [sg.Input(prod_venda_desc,key='desc_produto_venda', size=(15,30), readonly=True)]], title_location='n')        
            ], 
        [sg.Frame('Quantidade',[ [sg.Input(prod_venda_qntd,key='qnt_produto_venda', size=(15,30))]],title_location='n'), 
            sg.Frame('Valor Unitário',[ [sg.Input(prod_venda_unitario, key = 'valor_unitario', size=(15,30), readonly=True)]], title_location='n'),
            sg.Button('Inserir')
        ],
        [sg.Table(tabelaVendas, key = 'box_vendas', headings=['Nome','Descrição', 'Quantidade', 'Código Barras', 'Valor Unitário', 'Valor Total'], auto_size_columns=False, col_widths=[10])],
        [sg.Button('Concluir', key='concluir_venda',pad=(10,30))],
    ]
    return sg.Window('Venda', layout=layout, size=(600,450), element_justification='center', finalize = True)

filtro = '*' #Define qual sera o filtro usado, o padrão é não filtrar, ou seja, mostrar todos


filtroColuna = ''
filtro_procurar = ''
filtroColuna_fornecedor = ''
filtro_procurar_fornecedor = ''

def filtrarConteudo():
    cursor.execute(f'''SELECT * FROM produtos WHERE {filtroColuna} LIKE "%{filtro_procurar}%"''') #É PRECISO USAR ASPAS ENTRE O FILTRO PROCURAR, POIS SE NÃO N DA CERTO ASPAS DUPLAS NO CASO ) ESSE LIKE E AS % entre o texto faz com que ele procure algo próximo
    data = cursor.fetchall()
    banco.commit()
    return data

def filtrarConteudoFornecedor():
    cursor.execute(f'''SELECT * FROM fornecedores WHERE {filtroColuna_fornecedor} LIKE "%{filtro_procurar_fornecedor}%"''') #É PRECISO USAR ASPAS ENTRE O FILTRO PROCURAR, POIS SE NÃO N DA CERTO ASPAS DUPLAS NO CASO ) ESSE LIKE E AS % entre o texto faz com que ele procure algo próximo
    data = cursor.fetchall()
    banco.commit()
    return data
    
def deletarBanco():
    cursor.execute(f"DELETE FROM produtos WHERE nome = '{nomeDeletar}'")
    banco.commit()

def deletarBancoFornecedor():
    cursor.execute(f"DELETE FROM fornecedores WHERE nome = '{nomeDeletar}'")
    banco.commit()
  
filtro = '*' #Define qual sera o filtro usado, o padrão é não filtrar, ou seja, mostrar todos

def read_task():
    cursor.execute(f'''SELECT {filtro} FROM produtos''')
    data = cursor.fetchall()
    banco.commit()
    #print(data[0])
    return data

def read_task_venda():
    teste = tabelVendas
    data = teste
    return data

def read_task_fornecedor():
    cursor.execute(f'''SELECT {filtro} FROM fornecedores''')
    data = cursor.fetchall()
    banco.commit()
    return data


 
   
        
filtroColuna = ''
filtroColuna_fornecedor = ''

filtro_procurar = ''
filtro_procurar_fornecedor = ''

tabelaFornecedores = read_task_fornecedor()
tabelaProdutos = read_task() 
tabelaVendas = read_task_venda() #alterar



janela1,janela2,janela3,janela4,janela5,janela6,janela7, janelaVenda, janelaProdutosVenda, JanelaFornecedor, janelaVerFornecedor = janelaMain(), None, None, None, None, None, None, None, None, None, None


while True:
    window,event,values = sg.read_all_windows()    
    if  event == sg.WINDOW_CLOSED and window != janela1:
        window.close()
    elif event == sg.WIN_CLOSED and window == janela1:
        break

    if event == 'Cadastrar Entrada':
        cursor.execute("SELECT * FROM produtos ORDER BY cod_produto DESC LIMIT 1")
        result = cursor.fetchone()
        print(result[0])
        janela4 = cadastrarEntrada()
       
    elif event == 'Cadastrar Produto':
        janela5 == cadastrarProduto()
    elif event == 'Consultar Produtos':
        print(janela6)
        tabelaProdutos = read_task() #ATUALIZA A TABELA QUANDO MUDA A TELA ------- IMPORTANTE COLOCAR ISSO ANTES DE ABRIR JANELA
        janela6 = consultaProdutos() 
    elif event == 'Cadastrar Fornecedor':
        JanelaFornecedor = cadastrarFornecedor()
    elif event == 'Ver Fornecedores':
        tabelaFornecedores = read_task_fornecedor() #ATUALIZA A TABELA QUANDO ABRE A JENELA ------- IMPORTANTE COLOCAR ISSO ANTES DE ABRIR JANELA
        janelaVerFornecedor = consultaFornecedores()
        print('fornecedor')

    if event == 'edit':
        try:
            if tabelaProdutos:
                deletar = values['box'][0] #ISSO FAZ COM QUE SEJA POSSIVEL ESCOLHER UM ITEM DA LISTA CLICANDO
                ofc = tabelaProdutos[deletar]
                prod_nome_produto = ofc[1] #ISSO MOSTRA O PARAMETRO 1 DENTRO DA TUPLA  ----- SERVE PARA PASSAR AS INFOS PRO INPUT DEFAULT TEXT
                prod_qnt_produto = ofc[2] #ISSO MOSTRA O PARAMETRO 2 DENTRO DA TUPLA ----- SERVE PARA PASSAR AS INFOS PRO INPUT DEFAULT TEXT
                prod_cod_barra = ofc[3] #ISSO MOSTRA O PARAMETRO 3  DENTRO DA TUPLA ----- SERVE PARA PASSAR AS INFOS PRO INPUT DEFAULT TEXT
                prod_desc_produto = ofc[4]
                prod_nmr_ncm = ofc[5]
                prod_nmr_icms = ofc[6]
                prod_valor_entrada = ofc[7]
                prod_valor_unitario = ofc[8]
                
                janela7 = editarProduto()
                window.close() #FECHA A TELA DE LISTA DE PRODUTOS
        except IndexError as erro:
            sg.popup('Erro de Indice: Selecione algum item da tabela')

    if event == 'alterar_produto':
       
        #IDENTIFICA OS NOVO CAMPO PRA ALTERAR
        nprod_nome_produto =  values['nome_produto'] 
        nprod_qnt_produto=  values['qnt_produto']
        nprod_cod_barra =  values['cod_barra']
        nprod_nmr_ncm = values['nmr_ncm']
        nprod_nmr_icms = values['nmr_icms']
        nprod_valor_entrada = values['valor_entrada']
        nprod_valor_unitario = values['valor_unitario']
        nprod_desc_produto = values ['desc_produto']

        print(nprod_valor_unitario)
        print(values['valor_unitario'])
        
        

        if nprod_nome_produto and nprod_qnt_produto and nprod_cod_barra and nprod_nmr_ncm and nprod_nmr_icms and nprod_desc_produto and nprod_valor_unitario != '':
            try: #TRATAMENTO DE ERRO
                nprod_valor_total = float(nprod_valor_unitario) * float(nprod_qnt_produto)
                cursor.execute(f"UPDATE produtos SET nome = '{nprod_nome_produto}' WHERE nome = '{prod_nome_produto}'")
                cursor.execute(f"UPDATE produtos SET quantidade = '{nprod_qnt_produto}' WHERE nome = '{prod_nome_produto}'")
                cursor.execute(f"UPDATE produtos SET cod_barras = '{nprod_cod_barra}' WHERE nome = '{prod_nome_produto}'")
                cursor.execute(f"UPDATE produtos SET ncm = '{nprod_nmr_ncm}' WHERE nome = '{prod_nome_produto}'")
                cursor.execute(f"UPDATE produtos SET icms = '{nprod_nmr_icms}' WHERE nome = '{prod_nome_produto}'")
                cursor.execute(f"UPDATE produtos SET valor_entrada = '{nprod_valor_entrada}' WHERE nome = '{prod_nome_produto}'")
                cursor.execute(f"UPDATE produtos SET valor_unitario = '{nprod_valor_unitario}' WHERE nome = '{prod_nome_produto}'")
                cursor.execute(f"UPDATE produtos SET desc = '{nprod_desc_produto}' WHERE nome = '{prod_nome_produto}'")  
                cursor.execute(f"UPDATE produtos SET valor_total = '{nprod_valor_total}' WHERE nome = '{prod_nome_produto}'") 
                banco.commit()  
                
                print('oi')
                window.close() #FECHA A TELA DE EDIÇÃO DE PRODUTOS / EU USEI ISSO POIS ELE CONSEGUE ATUALIZAR QUANDO ABRE A TELA, DIFERENTE DO HIDE E UNHIDE
                
                tabelaProdutos = read_task()
                janela6 = consultaProdutos()
                

            except ValueError as erro:
                sg.popup("Algum campo foi preenchido errado!")
        else:
            sg.popup("Erro de cadastro: Existem campos vázios", title='ERRO')
                
        


    if event == 'Voltar':
        janela6.hide()

    if event == 'voltar_fornecedor':
        janelaVerFornecedor.hide()

    
    if event == 'Backup':
        sg.popup('BACKUP')
        
    #USAR FILTRO CONSULTA PRODUTOS
    if event == 'nomesfiltrar' and window == janela6:
        if values['radioID'] == True: ##Se o botão do NOME estiver selecionado, ele procura por user
            filtroColuna = 'cod_produto'
        elif values['radioNome'] == True: ##Se o botão de SENHA estiver selecionado, ele procura por senha
            filtroColuna = 'nome'
        elif values['radioCODBARRAS'] == True: ##Se o botão do EMAIL estiver selecionado, ele procura por EMAIL
            filtroColuna = 'cod_barras'
        filtro_procurar = values['filtroProcurar']
        print(f'procurar: {filtro_procurar}')
        print(f'coluna: {filtroColuna}')
        tabelaProdutos = filtrarConteudo()
        window.find_element('box').Update(tabelaProdutos)

    #SE TIRAR O FILTRO
    if event == 'tirarFiltro' and window == janela6:
        tabelaProdutos = read_task()
        window.find_element('box').Update(tabelaProdutos)
    if event == 'select' and window == janela6:
        #TRATAMENTO DE ERRO
        try:
            if tabelaProdutos and window == janela6:
                x = values['box'][0] #ISSO FAZ COM QUE SEJA POSSIVEL ESCOLHER UM ITEM DA LISTA CLICANDO
                print(x)
                print(tabelaProdutos[x])
                sg.popup(f'Voce selecionou {tabelaProdutos[x]}')
        except IndexError as erro:
            sg.popup('Erro de Indice: Selecione algum item da tabela')

    #DELETE
    if event == 'delete' and window == janela6: 
        try:
            if tabelaProdutos:
                deletar = values['box'][0]
                ofc = tabelaProdutos[deletar]
                nomeDeletar = ofc[1] #ISSO MOSTRA O PARAMETRO 1 DENTRO DA TUPLA
                print(nomeDeletar) 
                deletarBanco()
                tabelaProdutos= read_task()  #ATUALIZA OS DADOS
                window.find_element('box').Update(tabelaProdutos) #ATUALIZA OS DADOS
                sg.popup(f'O produto {nomeDeletar} excluido com sucesso!')
                

        except IndexError as erro:
            sg.popup('Erro de Indice: Selecione algum item da tabela')




        #USAR FILTRO CONSULTA PRODUTOS VENDA
    if event == 'nomesfiltrar' and window == janelaProdutosVenda:
        if values['radioID'] == True: ##Se o botão do NOME estiver selecionado, ele procura por user
            filtroColuna = 'cod_produto'
        elif values['radioNome'] == True: ##Se o botão de SENHA estiver selecionado, ele procura por senha
            filtroColuna = 'nome'
        elif values['radioCODBARRAS'] == True: ##Se o botão do EMAIL estiver selecionado, ele procura por EMAIL
            filtroColuna = 'cod_barras'
        filtro_procurar = values['filtroProcurar']
        print(f'procurar: {filtro_procurar}')
        print(f'coluna: {filtroColuna}')
        tabelaProdutos = filtrarConteudo()
        window.find_element('box_produtos_venda').Update(tabelaProdutos)

    #SE TIRAR O FILTRO
    if event == 'tirarFiltro' and window == janelaProdutosVenda:
        tabelaProdutos = read_task()
        window.find_element('box_produtos_venda').Update(tabelaProdutos)
    if event == 'select' and window == janelaProdutosVenda:
        #TRATAMENTO DE ERRO
        try:
            if tabelaProdutos:
                x = values['box_produtos_venda'][0] #ISSO FAZ COM QUE SEJA POSSIVEL ESCOLHER UM ITEM DA LISTA CLICANDO
                print(x)
                print(tabelaProdutos[x])
                sg.popup(f'Voce selecionou {tabelaProdutos[x]}')

        except IndexError as erro:
            sg.popup('Erro de Indice: Selecione algum item da tabela')


        #---------------------------------------------------------------------------------------------
        #USAR FILTRO CONSULTA fornecedores
    if event == 'nomesfiltrar_fornecedor' and window == janelaVerFornecedor:
        if values['radioID_fornecedor'] == True: ##Se o botão do NOME estiver selecionado, ele procura por user
            filtroColuna_fornecedor = 'cod_fornecedor'
        elif values['radioNome_fornecedor'] == True: ##Se o botão de SENHA estiver selecionado, ele procura por senha
            filtroColuna_fornecedor = 'nome'
        elif values['radioCNPJ_fornecedor'] == True: ##Se o botão do EMAIL estiver selecionado, ele procura por EMAIL
            filtroColuna_fornecedor = 'cnpj'
        filtro_procurar_fornecedor = values['filtroProcurar_fornecedor']
        print(f'procurar: {filtro_procurar_fornecedor}')
        print(f'coluna: {filtroColuna_fornecedor}')
        tabelaFornecedores = filtrarConteudoFornecedor()
        window.find_element('box_fornecedor').Update(tabelaFornecedores)

    #SE TIRAR O FILTRO
    if event == 'tirarFiltro_fornecedor' and window == janelaVerFornecedor:
        tabelaFornecedores = read_task_fornecedor()
        window.find_element('box_fornecedor').Update(tabelaFornecedores)
    if event == 'select_fornecedor' and window == janelaVerFornecedor:
        #TRATAMENTO DE ERRO
        try:
            if tabelaFornecedores:
                x = values['box_fornecedor'][0] #ISSO FAZ COM QUE SEJA POSSIVEL ESCOLHER UM ITEM DA LISTA CLICANDO
                print(x)
                print(tabelaFornecedores[x])
                sg.popup(f'Voce selecionou {tabelaFornecedores[x]}')

        except IndexError as erro:
            sg.popup('Erro de Indice: Selecione algum item da tabela')


    if event == 'delete' and window == janelaVerFornecedor: 
            try:
                if tabelaFornecedores:
                    deletar = values['box_fornecedor'][0]
                    ofc = tabelaFornecedores[deletar]
                    nomeDeletar = ofc[1] #ISSO MOSTRA O PARAMETRO 1 DENTRO DA TUPLA
                    print(nomeDeletar) 
                    deletarBancoFornecedor()
                    tabelaFornecedores= read_task()  #ATUALIZA OS DADOS
                    window.find_element('box_fornecedor').Update(tabelaFornecedores) #ATUALIZA OS DADOS
                    sg.popup(f'O produto {nomeDeletar} excluido com sucesso!')
                    

            except IndexError as erro:
                sg.popup('Erro de Indice: Selecione algum item da tabela')

    #-----------------------------------------------------------------------------------


    if event == 'Cadastrar': #BOTÃO DA TELA DE CADASTRO DE ENTRADA
        add_entrada()
    if event == 'cadastrar_produto': #BOTÃO DA TELA DE CADASTRO DE PRODUTO
        add_produto()   
    if event == 'cadastrar_fornecedor':
        add_fornecedor()  

    if event == 'Cancelar':
        janela3.hide()
        janela2.un_hide()

    if event == 'data_entrada': #Faz com que o calendario funcione
        data_adicionar = sg.popup_get_date(close_when_chosen=True)
        if data_adicionar:
            day, monthh, year = data_adicionar
        window['data_produto'].update(f"{monthh:0>2d}-{day:0>2d}-{year}")

    if event == 'Vender Produto':
        janelaVenda = venderProduto()
        

    if window == janelaVenda and event == 'abrir_produtos':
        tabelaProdutos = read_task()
        janelaProdutosVenda = consultaProdutosVenda()
        window.close()
        #window['nome_produto_venda'].update(prod_nome_produto)


    if window == janelaProdutosVenda: #MOSTRAR LINHA CLICADA
        try:
            if tabelaProdutos:
                linha = values['box_produtos_venda'][0] #ISSO FAZ COM QUE SEJA POSSIVEL ESCOLHER UM ITEM DA LISTA CLICANDO
                ofc = tabelaProdutos[linha]

                if event == 'select_vendas':
                    prod_venda_nome = ofc[1]
                    prod_venda_desc = ofc[4]
                    prod_venda_entrada = ofc[3]
                    prod_venda_unitario = ofc[8]
                    prod_venda_qntd = ofc[2]
                    print(prod_venda_nome)     
                    janelaVenda = venderProduto()
                    window.close() 
        except IndexError as erro:
            pass

        
        
    if event == 'Inserir' : #INSERI OS VALORES DOS INPUTS NA TABELA
        #REPLACE DA PARTE DE QUANTIDADE
        prod_venda_qntd = values['qnt_produto_venda']
        prod_venda_qntd = prod_venda_qntd.replace(',','')
        novo_qntd = prod_venda_qntd.split(".",1)
        nova_qntd_produto = novo_qntd[0]
        nova_qntd_produto = nova_qntd_produto.replace('(','')
        nova_qntd_produto = int(nova_qntd_produto)

        #REPLACE DA PARTE DO VALOR UNITARIO 
        prod_venda_valor_unitario = values['valor_unitario']
        prod_venda_valor_unitario = prod_venda_valor_unitario.replace(',', '')
        novo_valor_unitario = prod_venda_valor_unitario.split(".", 1)
        novo_valor_unitario_produto = novo_valor_unitario[0]
        novo_valor_unitario_produto = novo_valor_unitario_produto.replace('(','')
        novo_valor_unitario_produto = int(novo_valor_unitario_produto)
        #REPLACE NA PARTE DO NOME

        novo_prod_venda_nome = values['nome_produto_venda'].replace(')','')
        novo_prod_venda_nome = novo_prod_venda_nome.replace('(', '')
        novo_prod_venda_nome = novo_prod_venda_nome.replace(',', '')
        novo_prod_venda_nome = novo_prod_venda_nome.replace("'", "")
       
        #REPLACE NA PARTE DA DESC
        novo_prod_venda_desc = values['desc_produto_venda'].replace(')','')
        novo_prod_venda_desc = novo_prod_venda_desc.replace('(', '')
        novo_prod_venda_desc = novo_prod_venda_desc.replace(',', '')
        novo_prod_venda_desc = novo_prod_venda_desc.replace("'", "")
        

        
        
        print('---------------')
        print()
        valor_total = float(nova_qntd_produto) * float(novo_valor_unitario_produto)
        if values['nome_produto_venda'] and values['cod_barra_venda'] and values['desc_produto_venda'] and values['qnt_produto_venda'] and values['valor_unitario'] != '':
                try: #TRATAMENTO DE ERRO
                    prod_codigo = values['cod_barra_venda']
                    prod_nome = novo_prod_venda_nome #SE EU PEGASSE DO VALUES COMO FIZ ACIMA, ELE TERIA VARIOS () e ,, então peguei oq eu já tinha dado replace acima
                    cursor.execute('SELECT * FROM produtos WHERE nome = ? AND cod_barras = ?', (prod_nome, prod_codigo))
                    if cursor.fetchall():
                        tabelVendas.insert(0, [novo_prod_venda_nome,novo_prod_venda_desc,nova_qntd_produto,values['cod_barra_venda'],novo_valor_unitario_produto,valor_total]) #O NMR 0 É PRA INSERIR NA LINHA 0
                        window.find_element('box_vendas').Update(tabelaVendas) #ATUALIZAR A TABELA
                        print(tabelVendas)
                    else:
                        sg.popup('Existem informações Incorretas ou não cadastradas no sistema')
                except ValueError as erro:
                    sg.popup("Algum campos foram preenchidos errado!")
  
        

    if window == janelaVenda and event == sg.WINDOW_CLOSED:
            tabelVendas.clear() #LIMPAR A TABELA QUANDO FECHAR A JANELA
            print('como esta'+ str(tabelVendas))

    
        


    if event == 'concluir_venda' and window == janelaVenda:
        print('>>>>')
        while i < len(tabelaVendas): #FAZ UM LOOP PARA SOMAR TODOS OS VALORES TOTAIS DOS PRODUTOS DA LISTA
            print(tabelaVendas[i][0])
            total = total + tabelaVendas[i][5]
            total = total #ISSO FAZ COM QUE NÃO BUGUE AO SOMAR, JÁ QUE O VALOR VAI SOMAR EM CIMA DO VALOR 
            i +=1
        else: #QUANDO A VENDA FOR EFETUADA
            sg.popup('Venda concluida com sucesso')
            print('acabou')
            print(total)

            #----------------------------------------------------------------
            #ESSE CÓDIGO FAZ COM QUE VERIFIQUE SE JÁ EXISTE ALGUM DADO NA TABELA DE SAIDA, SE NÃO EXISTIR ELE VAI DEIXAR A NOTA COMO NMR 1
            cursor.execute("SELECT * FROM saida WHERE nmr_nota_fiscal = 1")
            data = cursor.fetchone()
            if data is None:
                nmr_notafiscal = 1       
            else:
                cursor.execute("SELECT * FROM saida ORDER BY nmr_nota_fiscal DESC LIMIT 1")
                result = cursor.fetchone() 
                #nmr_notafiscal_antes = result[0] 
                nmr_notafiscal = result[0] + 1

            #----------------------------------------------------------------
                
     

            while x < len(tabelaVendas):
                
                cod_prod = tabelaVendas[x][0]
                
                
                nome_saida = tabelaVendas[x][0]
                codbarra_saida = tabelaVendas[x][3]
                qntd = tabelaVendas[x][2]
                data_saida = datetime.today().strftime('%d-%m-%Y')
                valor_unitario_saida = tabelaVendas[x][4]
                valor_total_saida = tabelaVendas[x][5]

                cursor.execute(f"INSERT INTO saida VALUES({nmr_notafiscal}, '{nome_saida}', '{codbarra_saida}', '{qntd}', '{data_saida}', '{valor_unitario_saida}', '{valor_total_saida}')")
                banco.commit()
                

                #cursor.execute("INSERT INTO saida VALUES")
        
                print('INSERINDO...')
                cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE nome = ?", (qntd,  cod_prod))
                banco.commit()
                x += 1
           


            total = 0 #RESETA O TOTAL
            i = 0 #RESETA O LOOP
            x = 0


    if event == 'Ver Faturamento':
        print('faturamento')
        cursor.execute("SELECT * FROM saida")
        result = cursor.fetchone()
        nmr_notafiscal_antes = result
        print(nmr_notafiscal_antes)


        
       
        

        

    if event == 'procurar_cod_barra' and window == janelaVenda:
        barras= values['cod_barra_venda']
         
        #ATUALIZAR INPUT NOME
        cod_barra_nome = cursor.execute(f"SELECT nome FROM produtos WHERE cod_barras = '{barras}'")
        data_nome = cursor.fetchall()
     
  
        window.Element('nome_produto_venda').Update(data_nome)
        #ATUALIZAR INPUT DESC
        cod_barra_desc = cursor.execute(f"SELECT desc FROM produtos WHERE cod_barras = '{barras}'")
        data_desc = cursor.fetchall()
        
       


        window.Element('desc_produto_venda').Update(data_desc)


        #ATUALIZAR INPUT QUANTIDADE
        cod_barra_qnt = cursor.execute(f"SELECT quantidade FROM produtos WHERE cod_barras = '{barras}'")
        data_qnt = ''
        data_qnt = cursor.fetchall()
        banco.commit()
    
    
        
        window.Element('qnt_produto_venda').Update(data_qnt)
        data_qnt = str(data_qnt)
        data_qnt = data_qnt.replace(',', '')

        #ATUALIZA O INPUT DO VALOR UNITARIO
        cod_barra_valor_unitario = cursor.execute(f"SELECT valor_unitario FROM produtos WHERE cod_barras = '{barras}'")
        data_valor_unitario = ''
        data_valor_unitario = cursor.fetchall()
    
        banco.commit()



        window.Element('valor_unitario').Update(data_valor_unitario)
        data_valor_unitario = str(data_valor_unitario)
        data_valor_unitario = data_valor_unitario.replace(',', '')

        
        
  
       

        
  



          
        


    
     
        


        

    

    




     

 

       