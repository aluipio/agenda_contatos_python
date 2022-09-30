"""
#################################################
# Agenda de Contatos
#################################################

    - Cadastra nome, telefone, email, etc...; (certo)
    - Pesquisa alguém cadastrado;
    - Mostra quem foi cadastrado; (certo)
    - Deleta contatos cadastrados; (certo)
    - Bonus: Ao encerrar a execução cria um txt com agenda. (certo)

## Etapa 1 - Gerar Base de Armazenamento
"""

import os

# Inicia Banco de Dados de Agenda
alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
database = [[] for i in range(len(alfabeto))]

"""## Etapa 2 - Carregando Dados Simulados"""

def alimenta_database(database:list):
  from faker import Faker

  fake = Faker('pt_BR')

  for i in range(50):

    # Cria Dados
    nome = fake.name() # fake.first_name_female()
    telefone = fake.unique.random_int(min=1111111111, max=9999999999)
    email = nome.replace(" ","").lower()[:13] + "@exemplo.com"

    # Gera Indice
    indice_letra = alfabeto.index( nome[0].upper() )
    if len(database[indice_letra]) > 0:
      indice = database[indice_letra][-1][0] + 1
    else:
      indice = 1

    # Carrega dados em database
    database[indice_letra].append([indice, nome, telefone, email])

  return database

# Carrega o database com dados simulados
# database = alimenta_database(database)

"""## Etapa 3 - Funções do Sistema

### Funções acessórias
"""

def titulo(texto, elemento = "#"):
  print("".center(90, elemento))
  print(f" {texto} ".center(90, elemento))
  print("".center(90, elemento),"\n")

def sub_titulo(texto, elemento = "-"):
  print(f" {texto} ".center(90, elemento))

def print_linha(elemento = "-"):
  print("".center(90, elemento))

def print_contato(contato:list):
  print("[{:>2}] Nome:  {:<28}".format(contato[0], contato[1]), end="  |  ")
  print("Telefone:  {:<12}".format(contato[2]), end="  |  ")
  print("Email:  {:<30}".format(contato[3]))

def conta_contatos(dataset:list):
  conta = 0
  for lista in dataset:
    conta += len(lista)
  return conta

def limpa_tela():
  os.system('cls' if os.name == 'nt' else 'clear')

"""### Visualizar Contatos - OK

- Mostrar quem foi cadastrado por letra.
"""

def visualizar_letra(dataset:list, letra):
  
  # Carrega alfabeto ordenado
  alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  
  # Tratamento da variável 'letra'
  if type(letra) in [int,str,float,bool]:
    letra = str(letra).replace('.',"").replace(',',"").strip().upper() #[0]
    if letra.isdigit(): 
      letra = alfabeto[int(letra)-1]
  else:
    letra = "A"

  # Imprime o título da lista
  indice_letra = alfabeto.index( letra )
  print(f" Letra {alfabeto[ indice_letra ]} ".center(90, "#"))
  if len(dataset[indice_letra]) > 0 : print("")

  # Realiza loop na lista da Letra
  lista_contatos = dataset[indice_letra]
  for i in lista_contatos:
    print_contato(i)

  # Imprime soma
  print("")
  print(f"Total de ( {len(dataset[indice_letra])} ) contatos em letra {alfabeto[indice_letra]}.", end=" ")
  print(f"Página <{indice_letra+1}/{len(dataset)}>", "\n")

# Testando função
# visualizar_letra(database, "A")
# visualizar_letra(database, "z")

"""- Visualiza todos os contatos"""

def visualizar_agenda(dataset:list):
  
  # Carrega alfabeto ordenado
  alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  
  # Obs: local de total de contatos modificado para melhor visualização
  print(f"Total de ( {conta_contatos(dataset)} ) contatos registrados na agenda.".center(90))
  print("")
  
  # Loop no dataset
  for i in range(len(dataset)):

    # Verifica que existem contatos com o indice conforme a Letra
    if len(dataset[i]) > 0:

      # Lista contato conforme a letra
      visualizar_letra(database, alfabeto[i])
      
# Testando função
# visualizar_agenda(database)

"""### Inserir Contato - OK
Permite cadastrar um novo contato.
"""

# Entrada de Dados e tratamento
def inserir_contato(dataset:list):

  # Tratamento de Nome
  while True:
    nome = input("Nome: ").strip().title()
    if len(nome) > 0 and nome[0].isalpha():
      break
    else:
      print('Erro: campo Nome deve começar com letra.')

  # Tratamento de Telefone
  telefone_entrada = input("Telefone (apenas números): ").strip()
  telefone = ""
  for i in telefone_entrada:
    if i.isnumeric(): telefone += i

  # Tratamento de E-mail
  email = input("E-mail: ").strip().lower()

  # Calculando índice dos contatos
  alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  indice_letra = alfabeto.index( nome[0] )
  if len(dataset[indice_letra]) > 0:
    indice = dataset[indice_letra][-1][0] + 1
  else:
    indice = 1

  # Lista de Dados
  dados = [indice, nome, telefone[:10], email]

  # Carregando no dataset
  dataset[indice_letra].append(dados)

  # Print de Retorno
  sub_titulo("Contato cadastrado com Sucesso", "!")
  print("")

  return dataset, dados

# Testando função
# database, dados = inserir_contato(database)
# visualizar_letra(database, dados[1][0])

"""### Editar Contato - OK
Permite editar um contato.
"""

# Função Editar Contato
def modificar_contato(database:list, letra:str, indice:int):
  
  # Checagem inicial de informações
  alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  
  if len(letra) > 0 and letra.strip()[0].isalpha():
    
    # Trata variavel 'letra'
    letra = letra.strip()[0].upper() 
    
    # localiza index da letra
    index_letra = alfabeto.index(letra)
    letra = alfabeto.index(letra)

    contatos_letra = database[index_letra]
    if len(contatos_letra) >= indice and indice >= 0:
      
      # Carregando Contato
      contato = contatos_letra[indice - 1]
      sub_titulo('CONTATO PARA EDIÇÃO','-')
      print_contato(contato)
      print('')

      # Confirmação de edição
      while True:
        confirmando = input('Deseja editar esse contato?(s/n) ').strip()
        if len(confirmando) > 0 and confirmando[0] in ['s','n']:
          confirmando = confirmando[0]
          break
        else:
          print("Erro: digite opção 's' para SIM ou 'n' para NÃO.")
      
      print('')
      
      if confirmando == 's':

        # Checando qual edição será feita
        print("OBS.: Mantenha o campo vazio quando desejar manter o valor atual.")
        
        # Tratamento do campo NOME
        while True:
          nome = input(f'Mudar NOME de: [{contato[1]}] para: ').strip().title()
          if len(nome) > 0 and nome[0].isalpha():
            break
          elif nome == "":
            nome = contato[1]
            break
          else:
            print('Erro: campo Nome deve começar com letra.')

        # Tratamento do campo TELEFONE
        telefone_entrada = input(f'Mudar TELEFONE de: [{contato[2]}] para: ').strip()
        telefone = ""
        if len(telefone_entrada) > 0:
          for i in telefone_entrada:
            if i.isnumeric(): telefone += i
          if telefone == "": telefone = contato[2]
        elif telefone_entrada == "":
          telefone = contato[2]    

        # Tratamento de E-mail
        email = input(f'Mudar E-MAIL de: [{contato[3]}] para: ').strip().lower()
        if email == "": email = contato[3]
        
        print("")
        
        # Atulaizando contato
        novo_contato = [contato[0], nome, telefone, email]
        database[letra][indice - 1] = novo_contato
        
        # Imprime novo contato
        print_linha()
        sub_titulo("NOVO CONTRATO","#")
        print_contato(novo_contato)
        print("")

    else:
      print('Erro: Indice não localizado')
      
  else:
    print('<entrada de letra invalida>')

  return database

# Testando Função
# modificar_contato('j', 2)

"""###Remover contato - OK"""

# Remover contato baseado na letra e no indice do contato presente na lista da letra
def remove_contato(database:list, letra:str, indice:int):
  
  # Carrega Alfabeto
  alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  
  # Verifica parametros de entrada
  if letra[0].isalpha():
    letra = letra[0].upper()
    
    # Retornar indice de Letra
    index_letra = alfabeto.index(letra)

    # Ajustando Indice de entrada
    indice -= 1    

    # Verifica existência
    if indice >= 0 and indice < len(database[index_letra]):

      # Remove indice
      removido = database[index_letra].pop(indice)

      # Ajustar demais indices dentro na Letra
      for i in range(len(database[index_letra])):
        database[index_letra][i][0] = i + 1
          
      # Retornar contato removido
      sub_titulo("CONTATO REMOVIDO COM SUCESSO", '-')
      print_contato(removido)
      print("")

    else:

      # Contato não localizado
      sub_titulo("CONTATO NÃO LOCALIZADO", '-')
      print("")

    # Retornando nova lista de contatos
    visualizar_letra(database, alfabeto[index_letra])

  else:
    print('Erro: letra invalida.')

  return database

# Testando Função
# remove_contato('s', 3)
# remove_contato('z', 4)

"""### Pesquisar de Contato - OK"""

def pesquisa_contato(database:list, tipo, nome):
  tipo = int(tipo)
  nome = nome.strip()

  if tipo in range(1, 5):
    ###############################################
    # Pesquisando por NOME
    ###############################################
    if tipo == 1:

      # Conta o número de registros
      contador = 0

      # Imprime registros compativel com a busca
      print("")
      sub_titulo('Contratos Localizados por NOME')
      for i in database:
        for j in range(len(i)):
          if nome.lower() in i[j][1].lower():
            print_contato(i[j])
            contador += 1

      if contador == 0:
        sub_titulo('NENHUM CONTATO ENCONTRADO', ' ')
        print_linha()
      else:
        sub_titulo(f"Total de ({contador}) localizado(s).", '-')
    
    ###############################################
    # Pesquisando por Telefone
    ###############################################
    elif tipo == 2:
      
      # Trata valor de Telefone
      telefone = ''
      for i in nome:
        if i.isnumeric(): telefone += i

      
      # Conta o número de registros
      contador = 0

      # Imprime registros compativel com a busca
      print("")
      sub_titulo('Contratos Localizados por TELEFONE')
      for i in database:
        for j in range(len(i)):
          if telefone in str(i[j][2]):
            print_contato(i[j])
            contador += 1

      if contador == 0:
        sub_titulo('NENHUM CONTATO ENCONTRADO', ' ')
        print_linha()
      else:
        sub_titulo(f"Total de ({contador}) localizado(s).", '-')
    
    ###############################################
    # Pesquisando por e-mail
    ###############################################
    elif tipo == 3:

      # Conta o número de registros
      contador = 0

      # Imprime registros compativel com a busca
      print("")
      sub_titulo('Contratos Localizados por E-MAIL')
      for i in database:
        for j in range(len(i)):
          if nome.lower() in i[j][3].lower():
            print_contato(i[j])
            contador += 1

      if contador == 0:
        sub_titulo('NENHUM CONTATO ENCONTRADO', ' ')
        print_linha()
      else:
        sub_titulo(f"Total de ({contador}) localizado(s).", '-')      

  else: 
    print('<tipo de pesquisa inválido>')
    return '<tipo de pesquisa inválido>'

# Testando função
# pesquisa_contato(3, 'joana')

# Busca contato por tipo e nome
def buscar_contato(database:list, tipo, nome):
  
  # Remover espaços vazios do nome
  nome = nome.strip().lower()

  ###############################################
  # Pesquisando em todos os campos
  ###############################################

  # Conta o número de registros
  contador = 0

  # Imprime registros compativel com a busca
  print("")
  sub_titulo('BUSCANDO CONTATO NA BASE')
  for i in database:
    for j in range(len(i)):
      if (nome in i[j][1].lower()) or (nome in i[j][2].lower()) or (nome in i[j][3].lower()):
        print_contato(i[j])
        contador += 1

  if contador == 0:
    sub_titulo('NENHUM CONTATO LOCALIZADO', ' ')
    print_linha()
  else:
    sub_titulo(f"Total de ({contador}) localizado(s).", '-')

# Testando função
# pesquisa_contato(3, 'joana')

"""### Exportar Base - OK"""

def exporta_base(database:list):

  # Pergunta qual formato 
  print("[1] CSV  |  [2] TXT  |  [0] Sair sem Salvar")
  formato = input("Exportar em qual formato? ").strip()
  print("")
  print(" Iniciando Processamento ".center(90, "-"))

  # Carrega Alfabeto
  alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

  if int(formato) == 1:
    # Cria arquivo CSV
    lista_contatos = []

    # Carrega título de colunas CSV
    lista_contatos.append('letra;indice;nome;telefone;email \n')
    for i in range(len(database)):
      for n in database[i]:
        contato = alfabeto[i] + ";" + ";".join(map(str,n)) + "\n"
        lista_contatos.append(contato)

    # Salva em Arquivo Agenda.csv
    with open('Agenda.csv', 'w') as arquivo:
        arquivo.writelines(lista_contatos)

    print("".center(90, "#"))
    print(" AGENDA SALVA COM SUCESSO ".center(90, "#"))
    print("".center(90, "#"))        

  elif int(formato) == 2:
    # Cria arquivo TXT
    lista_contatos = []

    # Insere Título de Agenda
    lista_contatos.append("".center(90, "#") + "\n")
    lista_contatos.append(" AGENDA DE CONTATOS ".center(90, "#") + "\n")
    lista_contatos.append("".center(90, "#") + "\n\n")
    # Insere total de contatos
    print('\n')
    print(f" Total de ( {conta_contatos(database)} ) registrados na agenda.".center(90))
    print("")

    for i in range(len(database)):

      # Insere Título de Letra
      lista_contatos.append(f" Letra {alfabeto[i]} ".center(90, "#")+ "\n")
      if len(database[i]) > 0 : 
        lista_contatos.append("\n")

      # Varre contatos na Letra
      for n in database[i]:
        contato = "[{:>2}] Nome:  {:<28}".format(n[0], n[1]) + "  |  "
        contato += "Telefone:  {:<12}".format(n[2]) + "  |  "
        contato += "Email:  {:<30}".format(n[3])
        lista_contatos.append( contato + "\n" )
      
      # Fechamento da lista na Letra
      lista_contatos.append("\n")
      lista_contatos.append(f">>>>>>> Total de ( {len(database[i])} ) contatos em letra {alfabeto[i]}. \n\n\n")

    # Salva em Arquivo Agenda.txt
    with open('Agenda.txt', 'w') as arquivo:
      arquivo.writelines(lista_contatos)

    print("".center(90, "#"))
    print(" AGENDA SALVA COM SUCESSO ".center(90, "#"))
    print("".center(90, "#"))

  else:
    print("".center(90, "-"))
    print(" AGENDA ENCERRADA - AGENDA NÃO SALVA ".center(90, "-"))
    print("".center(90, "-"))     

# Testando Função
# exporta_base(database)

"""## Etapa 4 - Programa"""

# Inicia o programa
while True:
  
  # Limpar Tela
  limpa_tela()

  # Titulo de Tela
  titulo("AGENDA DE CONTATOS")

  # Imprime total de contatos na agenda
  sub_titulo(f"Total de ({conta_contatos(database)}) contato(s) armazenado(s).", '-')
  print("")

  print("""----   MENU PRINCIPAL   ----
  [  1  ] Adicionar contato
  [  2  ] Editar contato
  [  3  ] Remover contato
  [  4  ] Pesquisar contato
  [  5  ] Visualizar lista por letra
  [  6  ] Visualizar lista completa
  [  7  ] Simular dados
  [  0  ] Encerrar e Salvar \n""")

  # Controla comando de entrada do usuário
  while True:
    cmd = input("Qual operação deseja realizar? ").strip()
    if cmd in ['1','2','3','4','5','6','7','0']:
      cmd = int(cmd)      
      break
    else:
      print('Erro: Digite uma opção válida.')
  print("")

  ##################################################################
  # Salvando e saindo
  ##################################################################
  if cmd == 0:

    # Limpar Tela
    limpa_tela()

    # Titulo da Operação
    titulo("ENCERRANDO O SISTEMA")      

    exporta_base(database)
    break
  
  ##################################################################
  # Adicionando contato
  ##################################################################  
  elif cmd == 1:

    while True:

      # Limpar Tela
      limpa_tela()

      # Titulo da Operação
      titulo("ADICIONAR NOVO CONTATO")    

      sub_titulo('Novo Contato')
      database, dados = inserir_contato(database)
      print_linha()

      visualizar_letra(database, dados[1][0])

      print_linha()
      print("[s][Enter] Adicionar Novo | [n] voltar ao MENU PRINCIPAL")
      teste = input('Deseja ADICIONAR novo contato?(s/n) ').strip().lower()
      print("")

      if len(teste) > 0 and teste[0] == 'n': break
  
  ##################################################################  
  # Editando contato
  ##################################################################  
  elif cmd == 2:

    # Loop de Edicação
    while True:

      # Limpar Tela
      limpa_tela()

      # Titulo da Operação
      titulo("EDITAR CONTATO")      

      # Indicar qual a letra inicial do contato
      while True:
        letra = input('Qual a letra inicial do contato que gostaria de editar? ').strip()
        if len(letra) > 0 and letra[0].isalpha():
          letra = letra[0].upper()
          break
        else:
          print("Erro: Letra invalida. Digite uma letra valida.")
      print("")
      
      # Imprimir Lista da Letra
      visualizar_letra(database, letra)

      # Recebe o indice que deve ser editado
      while True:
        indice = input(f'Digite o indice do contato da Letra [{letra.upper()}] que deve ser editado? ').strip()
        if indice.isnumeric():
          indice = int(indice)
          break
        else:
          print("Erro: Indice invalido. Digite um indice valida.")
      print("")
  
      # Edita do contato
      database = modificar_contato(database, letra, indice)

      # Pergunta se deseja editar mais um contato
      print_linha()
      print("[s] EDITAR OUTRO | [n] voltar ao MENU PRINCIPAL")
      teste = input('Deseja EDITAR mais um contato?(s/n) ').strip().lower()
      print("")

      if len(teste) > 0 and teste[0] == 'n': break

  ##################################################################  
  # Removendo contato
  ##################################################################
  elif cmd == 3:

    # Loop de Remoção
    while True:

      # Limpar Tela
      limpa_tela()

      # Titulo da Operação
      titulo("REMOVER CONTATO")      

      # Indicar qual a letra inicial do contato
      while True:
        letra = input('Qual a letra inicial do contato que gostaria de remover? ').strip()
        if len(letra) > 0 and letra[0].isalpha():
          letra = letra[0].upper()
          break
        else:
          print("Erro: Letra invalida. Digite uma letra valida.")
      print("")

      # Imprimir Lista da Letra
      visualizar_letra(database, letra)

      # Recebe o indice que deve ser removido
      while True:
        indice = input(f'Digite o indice do contato da Letra [{letra.upper()}] que deve ser removido? ').strip()
        if indice.isnumeric():
          indice = int(indice)
          break
        else:
          print("Erro: Indice invalido. Digite um indice valida.")
      print("")

      # Remover do contato
      database = remove_contato(database, letra, indice)
      
      # Pergunta se deseja remover mais um contato
      print_linha()
      print("[s] REMOVER OUTRO | [n] voltar ao MENU PRINCIPAL")
      teste = input('Deseja REMOVER mais algum contato?(s/n) ').strip().lower()
      print("")

      if len(teste) > 0 and teste[0] == 'n': break

  ##################################################################
  # Pesquisando contato
  ##################################################################  
  elif cmd == 4:
    
    while True:
    
      # Limpar Tela
      limpa_tela()

      # Titulo da Operação
      titulo("PESQUISAR CONTATO")

      # Escolher opção
      print("Escolha uma Opção: [1] Nome  [2] Telefone  [3] E-mail")
      while True:
        tipo = input("Gostaria de pesquisar seu contato por: ").strip()
        if tipo in ['1','2','3']:
          break
        else:
          print(f"Erro: Opção [{tipo}] inexistente. Escolha uma das opções acima.")
      print("")

      # Lista de valores
      valores = ['nome', 'telefone', 'e-mail']
      
      # Trata valor de busca
      while True:
        valor_busca = input(f'Qual o {valores[int(tipo)-1]} do contato que gostaria de pesquisar? ').strip()
        if len(valor_busca) > 0 and int(tipo) == 1 and valor_busca[0].isalpha():
          break
        elif len(valor_busca) > 0 and int(tipo) == 2 and valor_busca[0].isnumeric():
          break
        elif len(valor_busca) > 0 and int(tipo) == 3:
          break          
        else:
          print(f"Erro: digite um {valores[int(tipo)-1]} válido.")
      print("")

      pesquisa_contato(database, tipo, valor_busca)
      print("")
  
      # Verifica se deseja realizar outra operação
      print_linha()
      print("[n] Nova Pesquisa | [m] MENU PRINCIPAL")
      teste = input('Qual operação acima deseja fazer? ').strip().lower()
      print("")

      if len(teste) > 0 and teste[0] == 'm': break

  ##################################################################
  # Pesquisando por letra
  ##################################################################  
  elif cmd == 5:
    
    while True:

      # Limpar Tela
      limpa_tela()

      # Titulo da Operação
      titulo("LISTA CONTATOS POR LETRA")
      
      # Tratar erros
      while True:
        # Escolher a letra que deseja listar
        letra = input('Qual letra deseja listar? ou [Enter] para voltar. ').strip()
        if letra.isalpha():
          letra = letra[0].upper()
          break
        elif letra == "":
          break
        else:
          print(f"Erro: digite uma letra válida.")
      print("")

      # Var 'letra' vazia retorna ao MENU PRINCIPAL
      if letra == "": 
        break
      else:
        visualizar_letra(database, letra)
      
      # Verifica se deseja realizar outra operação
      print_linha()
      print("MENU: [n] Listar Novamente | [r] Remover Contato | [m] MENU PRINCIPAL")
      while True:
        escolha = input('Qual operação deseja realizar? ').strip().lower()
        if escolha in ['n','r','e','m']:
          break
        else:
          print(f"Erro: Opção [{escolha}] inexistente. Escolha uma opção no MENU.")

      print("")
      # Voltar para MENU PRINCIPAL
      if escolha == 'm':
        break

      # REMOVER CONTATO DA LISTA
      elif escolha == 'r':

        print_linha()
        while True:

          # Recebe o indice que deve ser removido
          indice = input(f'Digite o indice do contato da Letra [{letra.upper()}] que deve ser removido? ').strip()
          print("")

          # Verifica se o indice informado é númerico
          if indice.isnumeric():

            # Remove o contato
            database = remove_contato(database, letra, int(indice))
            print("")

            # Pergunta se deseja remover outro contato
            print_linha()
            teste = input('Deseja remover mais um contato?(s/n) ').strip().lower()
            print("")

            if len(teste) > 0 and teste[0] == 'n': break

          else:
            print(f"Erro: Digite um indice válido (Apenas números).")
          
  ##################################################################
  # Mostrando lista completa
  ##################################################################
  elif cmd == 6:

    # Limpar Tela
    limpa_tela()

    # Titulo da Operação
    titulo("LISTAR TODOS OS CONTATOS DA AGENDA")

    visualizar_agenda(database)
    print('')

    # Confirmação de retorno
    print_linha()
    input("Aperte [Enter] para retornar ao MENU PRINCIPAL.").strip()
    print('')

  ##################################################################
  # Prencher base com dados simulados
  ##################################################################
  elif cmd == 7:

    # Limpar Tela
    limpa_tela()

    # Titulo da Operação
    titulo("SIMULAR DADOS")

    # Total de dados na base
    print_linha()
    sub_titulo(f"Total de ({conta_contatos(database)}) contatos armazenado(s).", '-')
    print_linha()
    print("")

    # Verifica se deseja realizar outra operação
    print_linha()
    print("MENU: [s] Simular dados | [n] MENU PRINCIPAL")
    while True:
      escolha = input('Deseja simular dados e preencher a base?(s/n) ').strip().lower()
      if escolha in ['s','n']:
        break
      else:
        print(f"Erro: Opção [{escolha}] inexistente. Escolha uma opção no MENU.")
    print("")

    if escolha == 's':

      # Carrega função para simular dados
      database = alimenta_database(database)

      # Resposta de simulação
      sub_titulo(f"+ (50) Contatos simulados com sucesso", '!')
      print("")

      # Total de dados na base
      print_linha()   
      sub_titulo(f"Total de ({conta_contatos(database)}) contatos armazenado(s).", '-')
      print_linha() 
      print("")

      # Confirmação de retorno
      print_linha()
      input("Aperte [Enter] para retornar ao MENU PRINCIPAL.").strip()
      print("")