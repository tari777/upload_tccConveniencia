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
total = 0
prod_venda_nome = ''
prod_venda_desc = ''
prod_venda_qntd = ''
prod_venda_entrada = ''
prod_venda_unitario = ''
testo = 'fodase'
i = 0
tabelVendas = []
if not os.path.exists('C:/pastaTCC'):
    os.makedirs('C:/pastaTCC')
banco = sqlite3.connect('C:/pastaTCC/tcc_database.db')
#banco = sqlite3.connect("C:/Users/mathe/Desktop/tcc conveniencia/tcc_database.db") 
#data = pd.read_sql_query("SELECT * from produtos", banco)
#print(data[data['valor_total'] == 25]) #PROCURA ONDE VALOR TOTAL = 24

cursor = banco.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS produtos (cod_produto INTEGER PRIMARY KEY AUTOINCREMENT, nome text, quantidade real, cod_barras text, desc text, ncm text, icms text, valor_entrada float, valor_unitario float, valor_total float)")
cursor.execute("CREATE TABLE IF NOT EXISTS fornecedores (cod_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT, nome text, razao_social text, nome_fantasia text, rua text, cep text, bairro text, numero text, cidade text, estado text, complemento text, cnpj text, insc_estadual text, telefone text)")
cursor.execute("CREATE TABLE IF NOT EXISTS entrada (nmr_nota_fiscal TEXT PRIMARY KEY, nome text, nome_fornecedor text, quantidade integer, data_entrada text, valor_unitario real, valor_total real)")
cursor.execute("CREATE TABLE IF NOT EXISTS saida (nmr_nota_fiscal TEXT PRIMARY KEY, nome text, quantidade integer, data_saida text, valor_unitario real, valor_total real)")
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
        ['&Cadastro', ['&Cadastrar Entrada', '&Cadastrar Produto']],
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
        
        
        [sg.Button('Cadastrar',pad=(10,30))],
    ]
    return sg.Window('Cadastro', layout=layout, size=(600,400), element_justification='center', finalize = True)

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
        [sg.Button('Filtra', key='nomesfiltrar'),sg.Button('Tirar Filtro', key='tirarFiltro'), sg.Button('Selecionar', key = 'select_vendas'), sg.Button('Deletar', key ='delete'), sg.Button('Editar', key='edit')],
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

def filtrarConteudo():
    cursor.execute(f'''SELECT * FROM produtos WHERE {filtroColuna} LIKE "%{filtro_procurar}%"''') #É PRECISO USAR ASPAS ENTRE O FILTRO PROCURAR, POIS SE NÃO N DA CERTO ASPAS DUPLAS NO CASO ) ESSE LIKE E AS % entre o texto faz com que ele procure algo próximo
    data = cursor.fetchall()
    banco.commit()
    return data
    
def deletarBanco():
    cursor.execute(f"DELETE FROM produtos WHERE nome = '{nomeDeletar}'")
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


 
   
        
filtroColuna = ''
filtro_procurar = ''

tabelaProdutos = read_task() 
tabelaVendas = read_task_venda() #alterar



janela1,janela2,janela3,janela4,janela5,janela6,janela7, janelaVenda, janelaProdutosVenda = janelaMain(), None, None, None, None, None, None, None, None


while True:
    window,event,values = sg.read_all_windows()    
    if  event == sg.WINDOW_CLOSED and window != janela1:
        window.close()
    elif event == sg.WIN_CLOSED and window == janela1:
        break

    if event == 'Cadastrar Entrada':
        janela4 = cadastrarEntrada()
       
    elif event == 'Cadastrar Produto':
        janela5 == cadastrarProduto()
    elif event == 'Consultar Produtos':
        print(janela6)
        tabelaProdutos = read_task() #ATUALIZA A TABELA QUANDO MUDA A TELA
        janela6 = consultaProdutos() 

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

    
    if event == 'Backup':
        sg.popup('BACKUP')
        
    #USAR FILTRO
    if event == 'nomesfiltrar':
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
    if event == 'tirarFiltro':
        tabelaProdutos = read_task()
        window.find_element('box').Update(tabelaProdutos)
    if event == 'select':
        #TRATAMENTO DE ERRO
        try:
            if tabelaProdutos:
                x = values['box'][0] #ISSO FAZ COM QUE SEJA POSSIVEL ESCOLHER UM ITEM DA LISTA CLICANDO
                print(x)
                print(tabelaProdutos[x])
                sg.popup(f'Voce selecionou {tabelaProdutos[x]}')
        except IndexError as erro:
            sg.popup('Erro de Indice: Selecione algum item da tabela')

    #DELETE
    if event == 'delete': 
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

    if event == 'Cadastrar': #BOTÃO DA TELA DE CADASTRO DE ENTRADA
        add_entrada()
    if event == 'cadastrar_produto': #BOTÃO DA TELA DE CADASTRO DE PRODUTO
        add_produto()     

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
            sg.popup('Erro de Indice: Selecione algum item da tabela')

        
        
    if event == 'Inserir': #INSERI OS VALORES DOS INPUTS NA TABELA
        #REPLACE DA PARTE DE QUANTIDADE
        prod_venda_qntd = values['qnt_produto_venda']
        prod_venda_qntd = prod_venda_qntd.replace(',','')
        novo_qntd = prod_venda_qntd.split(".",1)
        nova_qntd_produto = novo_qntd[0]
        nova_qntd_produto = nova_qntd_produto.replace('(','')
        nova_qntd_produto = int(nova_qntd_produto)
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
        

        
        
    
        valor_total = float(nova_qntd_produto) * float(values['valor_unitario'])
        if prod_venda_nome and prod_venda_entrada and prod_venda_desc and prod_venda_qntd and prod_venda_unitario != '':
                try: #TRATAMENTO DE ERRO
                    prod_codigo = values['cod_barra_venda']
                    prod_nome = values['nome_produto_venda']
                    cursor.execute('SELECT * FROM produtos WHERE nome = ? AND cod_barras = ?', (prod_nome, prod_codigo))
                    print(prod_codigo)
                    if cursor.fetchall():
                        tabelVendas.insert(0, [novo_prod_venda_nome,novo_prod_venda_desc,nova_qntd_produto,values['cod_barra_venda'],values['valor_unitario'],valor_total]) #O NMR 0 É PRA INSERIR NA LINHA 0
                        window.find_element('box_vendas').Update(tabelaVendas) #ATUALIZAR A TABELA
                        print(tabelVendas)
                    else:
                        sg.popup('Existem informações Incorretas ou não cadastradas no sistema')
                except ValueError as erro:
                    sg.popup("Algum campos foram preenchidos errado!")
        else:
            sg.popup("Erro de cadastro: Existem campos vázios", title='ERRO')
        

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
        else:
            sg.popup('Venda concluida com sucesso')
            print('acabou')
            print(total)


            total = 0 #RESETA O TOTAL
            i = 0 #RESETA O LOOP

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
    
    
        print(data_qnt) 
        window.Element('qnt_produto_venda').Update(data_qnt)
        data_qnt = str(data_qnt)
        data_qnt = data_qnt.replace(',', '')
        
       

   
        
      

        
        
  
       

        
  



          
        


    
     
        


        

    

    




     

 

       