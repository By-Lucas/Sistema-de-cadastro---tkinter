#SISTEMA DE CADASTRO DE CLIENTES OU USUARIOS
#LUCAS SILVA 74981199190 WHATSAPP
#SISTEMA WEB EM DESENVOLVIMENTO
#SISTEMA INDA INCOMPLOETO, SERÁ TERMINADO EM BREVE
from mysql.connector import cursor
from psycopg2 import connect
import mysql.connector
from mysql.connector import errorcode



from bibliotecas import *
"""from relatorio import relatorios"""

#Janela Root
root = Tk()

#Gerar relatório do cliente
class relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf") # Nome do PDF
    
    def gerarRelatorioCliente(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.codigoReal = self.ID_entry.get()
        self.nomeReal = self.nome_entry.get()
        self.emailReal = self.email_entry.get()
        self.telefoneReal = self.telefone_entry.get()
        self.cidadeReal = self.cidade_entry.get()
        self.idmt5Real = self.idmt5_entry.get()
        self.senhaReal = self.senha_entry.get()
        self.dataReal = self.data_entry.get()
        self.corretoraReal = self.corretora_entry.get()

        self.c.setFont("Helvetica-Bold", 24) #Fonte pdf e tamanho da letra
        self.c.drawString(200, 790, 'Ficha do cliente') #espacamento pdf e titulo

        #Informacões do cleinte no PDF
        self.c.setFont("Helvetica", 15)
        self.c.drawString(50, 755, f"Todas as informações do cadastro do cliente(a) {self.nomeReal}") 
        self.c.drawString(50, 720, 'Codigo: '+ self.codigoReal)
        self.c.drawString(50, 690, 'Nome do Cliente: '+ self.nomeReal)
        self.c.drawString(50, 660, 'E-mail: '+ self.emailReal)
        self.c.drawString(50, 630, 'Telefone: '+ self.telefoneReal)
        self.c.drawString(50, 600, 'Cidade: '+ self.cidadeReal)
        self.c.drawString(50, 570, 'ID do MT5: '+ self.idmt5Real)
        self.c.drawString(50, 540, 'Senha: '+ self.senhaReal)
        self.c.drawString(50, 510, 'Data: '+ self.dataReal)
        self.c.drawString(50, 480, 'Corretora: '+ self.corretoraReal)


        self.c.showPage()
        self.c.save()
        self.printCliente()


#Classe onde vai ficar as funcoes
class funcoes():
    #Funcao de limpas as Entry
    def Limpar_lista_BT (self):

        self.ID_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
        self.idmt5_entry.delete(0, END)
        self.senha_entry.delete(0, END)
        self.data_entry.delete(0, END)
        self.corretora_entry.delete(0, END)
        
    #Conectar ao banco de dados 
    def conectar_db (self):
     
        # Construir conexão com database
        try:
            self.conn = mysql.connector.connect(user = 'login do banco de dados mysql',
                                                password = 'seha do banco de dados mysql',
                                                host =  'host do banco de dados mysql',
                                                database =  'banco de dados',
                                                port =  'porta do mysql',
                                                raise_on_warnings =  True)
            print("Conexão estabelecida com banco de dados")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Nome ou senha do banco de dados incorreto!")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Banco de dados não existe")
            else:
                print(err)
        else:
            self.cursor = self.conn.cursor()
        
    #Desconectar do banco de dados Sqlite3
    def desconecta_db (self):
        self.conn.close()
        print("Desconectado do banco de dados!")


    #Criar Tabela(s)
    def montar_tabelas(self):
        self.conectar_db(); print('Conectato ao bando de dados')

        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER NOT NULL PRIMARY KEY,
                nome TEXT (50)NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL,
                cidade INTEGER NOT NULL,
                idmt5 INTEGER NOT NULL,
                senhamt5 INTEGER NOT NULL,
                vencimento DATE NOT NULL,
                corretora TEXT NOT NULL
        );
        """)
        self.conn.commit(); print("Banco de dados criado")
        
        self.desconecta_db()
        
    #Onde vão ficar os opcoes das entry de cada espaço digitável
    def variaveis(self):
        #Dando nome as funcoes entry criadas na (def Widgets_frames(self):)
        self.cod = self.ID_entry.get()
        self.nome = self.nome_entry.get()
        self.email = self.email_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()
        self.idmt5 = self.idmt5_entry.get()
        self.senhamt5 = self.senha_entry.get()
        self.vencimento = self.data_entry.get()
        self.corretora = self.corretora_entry.get()

    #Cadastrar usuario MYSQL
    def cadastrar_cliente (self):
        self.variaveis() #Chamar variavel onde está as entry
        self.conectar_db() #Conectar no bando de dados na funcao criada
        
        #data
        self.DATETIME = time.strftime("dia "'%d/%m/%Y "as "%H:%M')


        if (self.nome == "" and self.email =="" and self.telefone=="" and self.cidade=="" and self.idmt5=="" and  self.vencimento =="" and self.corretora ==""):
            messagebox.showinfo(title="Erro", message="Preencha todos os campos!")

        else:
            #Inserindo os dados na tabela(conectando com as entry)
            self.cursor.execute(""" INSERT INTO clientes ( nome, email, telefone , cidade, idmt5, senhamt5, vencimento, corretora)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)
                """,  (self.nome, self.email, self.telefone, self.cidade, self.idmt5, self.senhamt5, self.vencimento, self.corretora))
            self.conn.commit()
            messagebox.showinfo(title="CONCLUIDO!", message=f"Cliente {self.nome} Cadastrado(a) {self.DATETIME} com sucesso!")
            
            self.desconecta_db()
            self.select_lista()
            self.Limpar_lista_BT()

    #limpar a lista e selecionar (mostrar lista dentro da treeview)
    def  select_lista(self):
        self.lista_cliente.delete(*self.lista_cliente.get_children())
        
        self.conectar_db()
        lista = self.cursor.execute(""" SELECT cod, nome, email, telefone , cidade, idmt5, senhamt5, vencimento, corretora FROM clientes
        ORDER BY cod ASC;""")
        lista_cli = self.cursor.fetchall()

        #For para criar selecionar as informacoes da tabela e acrescentar de acordo com o total
        for i in lista_cli:
            self.lista_cliente.insert("", END, values=i)
        self.desconecta_db()

    #funcao duplo clicl para selecionar e apagar, adicionar uma opcao(event)
    def duplo_click (self, event):
        self.Limpar_lista_BT() #primeiro apagar campos digitados
        self.lista_cliente.selection()

        for n in self.lista_cliente.selection():
            col1, col2, col3, col4, col5, col6 ,col7, col8, col9 = self.lista_cliente.item(n, 'values')
            
            #Puxar dados das colunas
            self.ID_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.email_entry.insert(END, col3)
            self.telefone_entry.insert(END, col4)
            self.cidade_entry.insert(END, col5)
            self.idmt5_entry.insert(END, col6)
            self.senha_entry.insert(END, col7)
            self.data_entry.insert(END, col8)
            self.corretora_entry.insert(END, col9)

    #Onde o botao deletar vai ser usado
    def deletar_cliente(self):
        self.variaveis()
        self.conectar_db()
        
        if  self.nome != "" and self.email !=""  and self.telefone !="" and self.cidade !="" and self.idmt5 !="" and self.senhamt5 !="" and self.vencimento !="" and self.corretora !="":
            self.cursor.execute("""DELETE FROM clientes WHERE cod = %s """, (self.cod))
            self.conn.commit()
            messagebox.showinfo(title="CLIENTE DELETADO", message=f"Cliente {self.nome} deletado com sucesso!")

            self.desconecta_db()
            self.Limpar_lista_BT()
            self.select_lista()

        else:
            messagebox.showinfo(title="APAGAR ERROR", message="Dê um duplo click encima do cliente para selecionar\n, atualizar ou apagar!")

            self.desconecta_db()
            self.Limpar_lista_BT()
            self.select_lista()
        
    #Alterar cadastro do cliente
    def alterar_cliente(self):
        self.variaveis()
        self.conectar_db()

        #Atualizar cadastro, o self.cod fica no final para nao ser alterado, se mudar de local da erro
        if  self.nome != "" and self.email !=""  and self.telefone !="" and self.cidade !="" and self.idmt5 !="" and self.senhamt5 !="" and self.vencimento !="" and self.corretora !="":
            self.cursor.execute(""" UPDATE clientes SET nome = %s, email = %s, telefone = %s, cidade = %s, idmt5 = %s, senhamt5 = %s, vencimento = %s, corretora = %s
            WHERE cod = %s""",( self.nome, self.email, self.telefone, self.cidade, self.idmt5, self.senhamt5, self.vencimento, self.corretora, self.cod))
            self.conn.commit()
            messagebox.showinfo(title="Concluido!", message=f"O cadastro de {self.nome} atualizado com sucesso!")

            self.desconecta_db()
            self.select_lista()
            self.Limpar_lista_BT()
             
        else:
            messagebox.showerror(title="Erro ao alterar", message="Dê um duplo click encima do cliente para selecionar,\natualizar ou apagar!")
        
    #Backup do banco de dados
    def backup_db(self):
        
        DB_HOST = 'link do Host do database'
        DB_USER = 'usuario de conexao com database'
        DB_USER_PASSWORD = 'senha de conexao com database'
        #DB_NAME = '/backup/dbnames.txt'
        # Se você tiver varias databases listadas em um arquivo, descomente a linha acima e substitua o caminho do diretório.
        DB_NAME = 'nome do login de conexao com database'
        DIRETORIO_BACKUP = 'backup/' #diretório onde deseja salvar o backup
        
        # Pegar hora e data para botar como nome pra pasta
        DATETIME = time.strftime('%d-%m-%Y  %H-%M')
        
        DIRETORIO_BACKUP_HOJE = DIRETORIO_BACKUP + DATETIME
        
        # Checando se a pasta já existe
        print ("Criando pasta de backup")
        if not os.path.exists(DIRETORIO_BACKUP_HOJE):
            os.makedirs(DIRETORIO_BACKUP_HOJE)
        
        # checagem de database unica ou múltipla
        print ("checando arquivo de databases.")
        if os.path.exists(DB_NAME):
            file1 = open(DB_NAME)
            multi = 1
            print ("O arquivo de dbs foi encontrado...")
            print ("Começando o backup de todos os bancos listados... " + DB_NAME)
        else:
            print ("O arquivo de dbs não foi encontrado...")
            print ("Começando o backup " + DB_NAME)
            multi = 0
        
        # Comecando o processo de backup.
        if multi:
            in_file = open(DB_NAME,"r")
            flength = len(in_file.readlines())
            in_file.close()
            p = 1
            dbfile = open(DB_NAME,"r")
        
            while p <= flength:
                db = dbfile.readline()   # lendo nome da database do arquivo
                db = db[:-1]         # deletar linha extra
                dumpcmd = "mysqldump -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + DIRETORIO_BACKUP_HOJE + "/" + db + ".sql"
                os.system(dumpcmd)
                p = p + 1
            dbfile.close()
        else:
            db = DB_NAME
            dumpcmd = "mysqldump -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + DIRETORIO_BACKUP_HOJE + "/" + db + ".sql"
            os.system(dumpcmd)
        
        print ("Backup completo")
        messagebox.showinfo(title="Concluido", message="Seu backup foi criado em '" + DIRETORIO_BACKUP_HOJE + "' diretorio")

    def backup_restaurar(self):
        
        messagebox.showinfo(title="Ola", message="Parte re restaurar backup ainda nao feita")
        

#Classe aplicacao e tambem chama outras classes para que seja executada
class apaplication(funcoes, relatorios):
    def __init__(self): #Todas as funcoes (def) ciradas serao chamadas aqui
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.Widgets_frames()
        self.lista_frame2()
        self.montar_tabelas()
        self.select_lista()
        self.Menus()
        root.mainloop() 

    #Tela principal
    def tela(self):
        self.root.title('SERVIDOR DE LIBRACAO')
        self.root.configure(background='#0B3861') #Background da pagina
        self.root.geometry('1100x588') # Tamanho da janela
        self.root.resizable(True, True) #Se pode aumentar e diminuir tamabnho da janela
        self.root.maxsize(width=1300, height=800) #Tamanho maximo da tela
        self.root.minsize(width=500, height=350) #Tamanho minimo da tela

        '''
        self.root.iconphoto(False, PhotoImage(file='icons/fundo.png')) #Adicionar Icone na pagina
        '''

    #Tela dos frames
    def frames_da_tela (self):
        #Frame 1 com bordas e tendo o mesmo tamanho que a tela ao maximizar/miniminar
        self.frame_1 = Frame(self.root, bd=5, bg='#BDBDBD', highlightbackground='#2ECCFA', highlightthickness=3)
        self.frame_1.place(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.45)

        #Frame 2 com bordas e tendo o mesmo tamanho que a tela ao maximizar/miniminar
        self.frame_2 = Frame(self.root, bd=5, bg='#BDBDBD', highlightbackground='#2ECCFA', highlightthickness=5)
        self.frame_2.place(relx= 0.02, rely= 0.5, relwidth= 0.96, relheight= 0.45)

    #Botoes do frame
    def Widgets_frames (self):
        #Botão Limpar
        self.BT_limpar = Button(self.frame_1, text="Limpar", command=self.Limpar_lista_BT)
        self.BT_limpar.config( font="arial 12 bold", bd=3, bg="#107db2", fg="white")
        self.BT_limpar.place(relx= 0.15 , rely= 0.05, relheight= 0.12, relwidth=0.11)

        #Botao Buscar
        self.BT_buscar = Button(self.frame_1, text="Buscar", font="arial 12")
        self.BT_buscar.config( font="arial 12 bold", bd=3, bg="#107db2", fg="white")
        self.BT_buscar.place(relx= 0.27 , rely= 0.05, relheight= 0.12, relwidth=0.11)

        #Botao Novo
        self.BT_novo = Button(self.frame_1, text="Novo", font="arial 12", command=self.cadastrar_cliente)
        self.BT_novo.config( font="arial 12 bold", bd=3, bg="#107db2", fg="white")
        self.BT_novo.place(relx= 0.6 , rely= 0.05, relheight= 0.12, relwidth=0.11)

        #Botao Alterar
        self.BT_alterar = Button(self.frame_1, command=self.alterar_cliente, text="Alterar", font="arial 12")
        self.BT_alterar.config( font="arial 12 bold", bd=3, bg="#107db2", fg="white")
        self.BT_alterar.place(relx= 0.72 , rely= 0.05, relheight= 0.12, relwidth=0.11)

        #Botao Apagar
        self.BT_apagar = Button(self.frame_1, command=self.deletar_cliente,text="Apagar", font="arial 12")
        self.BT_apagar.config( font="arial 12 bold", bd=3, bg="#107db2", fg="white")
        self.BT_apagar.place(relx= 0.84 , rely= 0.05, relheight= 0.12, relwidth=0.11)

        #CRIAR LABELS ==============
        #Label Entry codigo(ID)
        self.ID_label = Label(self.frame_1, text="Cod:", font="arial 14", bg="#BDBDBD", fg="#107db2")
        self.ID_label.place(relx= 0.00, rely=0.05)

        self.ID_entry = Entry(self.frame_1, font="arial 12")
        self.ID_entry.place(relx= 0.06, rely=0.05, relwidth=0.07, relheight=0.11)

        #Label Nome
        self.ID_label = Label(self.frame_1, text="Nome:", font="arial 14", bg="#BDBDBD", fg="#107db2")
        self.ID_label.place(relx= 0.00, rely=0.25)

        self.nome_entry = Entry(self.frame_1, font="arial 12")
        self.nome_entry.place(relx= 0.00, rely=0.35, relwidth=0.41, relheight=0.11)

        #Label E-mail
        self.Email_label = Label(self.frame_1, text="E-mail:", font="arial 14", bg="#BDBDBD", fg="#107db2")
        self.Email_label.place(relx= 0.54, rely=0.25)

        self.email_entry = Entry(self.frame_1, font="arial 12")
        self.email_entry.place(relx= 0.54, rely=0.35, relwidth=0.41, relheight=0.11)

        #Label E-Telefone
        self.telefone_label = Label(self.frame_1, text="Telefone:", font="arial 14", bg="#BDBDBD", fg="#107db2")
        self.telefone_label.place(relx= 0.00, rely=0.5)

        self.telefone_entry = Entry(self.frame_1, font="arial 12")
        self.telefone_entry.place(relx= 0.0, rely=0.6, relwidth=0.18, relheight=0.11)

        #Label Cidade
        self.cidade_label = Label(self.frame_1, text="Cidade:", font="arial 14", bg="#BDBDBD", fg="#107db2")
        self.cidade_label.place(relx= 0.22, rely=0.49)

        self.cidade_entry = Entry(self.frame_1, font="arial 12")
        self.cidade_entry.place(relx= 0.22, rely=0.6, relwidth=0.19, relheight=0.11)

        #Label ID MT5
        self.idmt5_label = Label(self.frame_1, text="ID MT5:", font="arial 14", bg="#BDBDBD", fg="#107db2")
        self.idmt5_label.place(relx= 0.54, rely=0.49)

        self.idmt5_entry = Entry(self.frame_1, font="arial 12")
        self.idmt5_entry.place(relx= 0.54, rely=0.6, relwidth=0.18, relheight=0.11)

        #Label Senha corretora
        self.senha_label = Label(self.frame_1, text="Senha MT5:", font="arial 14", bg="#BDBDBD", fg="#107db2")
        self.senha_label.place(relx= 0.77, rely=0.49)

        self.senha_entry = Entry(self.frame_1, font="arial 12")
        self.senha_entry.place(relx= 0.77, rely=0.6, relwidth=0.18, relheight=0.11)

        #Label data vencimento
        self.data_label = Label(self.frame_1, text="Vencimento:", font="arial 14", bg="#BDBDBD", fg="#107db2")
        self.data_label.place(relx= 0.00, rely=0.73)

        self.data_entry = Entry(self.frame_1, font="arial 12")
        self.data_entry.place(relx= 0.0, rely=0.84, relwidth=0.18, relheight=0.11)

        #Label Corretora
        self.corretora_label = Label(self.frame_1, text="Corretora:", font="arial 14", bg="#BDBDBD", fg="#107db2")
        self.corretora_label.place(relx= 0.22, rely=0.73)

        self.corretora_entry = Entry(self.frame_1, font="arial 12")
        self.corretora_entry.place(relx= 0.22, rely=0.84, relwidth=0.19, relheight=0.11)

    #Criar um combo de lista(Treeview)
    def lista_frame2 (self):
        self.lista_cliente = ttk.Treeview(self.frame_2, height=3)
        self.lista_cliente.config(column=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8", "col9"  ),selectmode="extended")

        self.lista_cliente.heading("#0", text="", anchor=CENTER)
        self.lista_cliente.heading("#1", text="Cod", anchor=CENTER)
        self.lista_cliente.heading("#2", text="Nome", anchor=CENTER)
        self.lista_cliente.heading("#3", text="E-mail", anchor=CENTER)
        self.lista_cliente.heading("#4", text="Telefone", anchor=CENTER)
        self.lista_cliente.heading("#5", text="Cidade", anchor=CENTER)
        self.lista_cliente.heading("#6", text="ID MT5", anchor=CENTER)
        self.lista_cliente.heading("#7", text="Senha MT5", anchor=CENTER)
        self.lista_cliente.heading("#8", text="Vencimento", anchor=CENTER)
        self.lista_cliente.heading("#9", text="Corretora", anchor=CENTER)
        
        self.lista_cliente.column("#0", width=0, anchor=CENTER)
        self.lista_cliente.column("#1", width=10, anchor=CENTER)
        self.lista_cliente.column("#2", width=150, anchor=CENTER)
        self.lista_cliente.column("#3", width=150, anchor=CENTER)
        self.lista_cliente.column("#4", width=70, anchor=CENTER)
        self.lista_cliente.column("#5", width=80, anchor=CENTER)
        self.lista_cliente.column("#6", width=50, anchor=CENTER)
        self.lista_cliente.column("#7", width=50, anchor=CENTER)
        self.lista_cliente.column("#8", width=50, anchor=CENTER)
        self.lista_cliente.column("#9", width=50, anchor=CENTER)
        
        self.lista_cliente.place(relx=0, rely=0, relheight=0.99 , relwidth=0.98)

        #Criar barra de rolagem Scrollbar
        self.scroolLista = Scrollbar(self.frame_2, orient=VERTICAL, width=20, bg='blue')
        self.lista_cliente.configure(yscrollcommand=self.scroolLista.set)
        self.scroolLista.pack(side="right", fill="y")

        self.lista_cliente.bind("<Double-1>", self.duplo_click)
        #Chamar a funcao de duplo click
        
    # Menu-bar ? Criar informacoes na barra do MENU
    def Menus (self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)
        

        def quit(): self.root.destroy()

        menubar.add_cascade(label= "Opções", menu=filemenu)
        menubar.add_cascade(label= "Relarorios", menu=filemenu2)

        filemenu.add_command(label="Sair", command=quit)
        filemenu.add_command(label="Limpar Cliente", command= self.Limpar_lista_BT)
        filemenu.add_command(label="Backup", command=self.backup_db)
        filemenu.add_command(label="Restaurar Backup", command= self.backup_restaurar)

        filemenu2.add_command(label="Ficha do Cliente", command= self.gerarRelatorioCliente)

apaplication()