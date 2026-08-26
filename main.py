"""
MÓDULO PRINCIPAL - SISTEMA DE CHECKLIST DE EQUIPAMENTOS
Este script gerencia a interface de usuário (CLI) para o sistema de inspeção.
Permite autenticação de inspetores, preenchimento de checklist e consulta relatórios
"""
import database # Módulo responsável pela conexão e persistência de dados
import operacoes # Módulo que contém as regras de negócio e lógica do sistema


equipamentos_validos = ["RTG-01", "RTG-02", "RTG-03", "RTG-04", "RTG-05", "RTG-06", "RTG-07", "RTG-08", "RS-01", "RS-02", "RS-03", "RS-04"]


def pausar():
    """
    Cria uma pausa na tela do terminal.
    Aguarda a interação do usuário antes de limpar ou avançar para a próxima tela
    """
    
    input("\nPressione ENTER para continuar...")




def exibir_menu():
    """
    Exibe o menu de opções principal no terminal.
    Apresenta visivelmente os comandos disponívels para o usuário
    """
    print("=" * 50)
    print(" CHECK LIST DE EQUIPAMENTOS")
    print("=" *50)
    print("1. Registrar nova inspeção")
    print("2. Listar inspecões")
    print("0. Sair")
    print("=" *50)


    

def fazer_tela_login():
    """
    Gerencia a tela de autenticação do inspetor da manutenção.

    Permite até 3 tentativas de acesso. Se s dados coicidirem com o sistema, retorna os dados do inspetor conectado. caso contrário, bloqueia o acesso.
    Retorna:
        dict: Dados do inspetor se o login for bem-sucedido.
        None: Se o acesso for negado por até 3 tentativas
    """
    tentativas = 0

    while tentativas < 3:
        print("\n--- LOGIN ---")
        #captura os dados limpando espaços invisíveis nas pontas com .strip()
        nome = input("Nome: ").strip()
        matricula = input("matricula: ").strip()

        # Valida as credenciais através do módulo de operações
        inspetor = operacoes.fazer_login(nome, matricula)


        if inspetor:
            print(f"\nBem-vindo, {nome}!")
            return inspetor  # Retorna o usuário autenticado e encerra a função
        else:
            tentativas +=1
            print(f"\n Matrícula ou nome incorreto. Tentativa {tentativas} de 3.")

    print("\nAcesso negado. Muitas tentativas incorretas.")
    return None




def tela_registrar_inspecao(inspetor_logado): 
    """Gerencia o fluxo de preenchimento e gravação de uma nova inspeção técnica
    
         Passa dinamicamente por cada item configurado no checklist de operações, solicita o status (OK/Pendência) e obriga o preenchumento de observação caso haja alguma falha detectada.
    
         Parâmetros:
         inspetor_logado (dict): Dados do inspetor que está realizando a vistoria"""  
    print("\n--- REGISTRAR NOVA INSPEÇÃO ---")

    # Coleta de informações básicas da máquina
    tipo_maquina = input("Tipo de máquina (RTG / RS): ").strip()

    numero_equipamento = input("Numero do equipamento (ex: RTG-05): ").strip()
    
    while numero_equipamento not in equipamentos_validos:
        print("Equipamento inválido! Digite um número válido.")
        numero_equipamento = input("Número do equipamento (ex: RTG-05): ").strip()

    print("\nAgora vamos passar por cada item do checklist.")

    #loop que percorre a estrutura de itens cadastrada no módulo de operações
    for item in operacoes.itens_checklist:
        print(f"\nItem: {item['nome_item']}")
        resposta = input("Status (OK / Pendência): ").strip()
        item["status"] = resposta

        # Condicional: se houver pendência, exige um detalhamento do problema
        if resposta == "Pendência":
            item["observacao"] = input("Observação: ").strip()
        else:
            item["observacao"] = ""  # Limpa observações anteriores

    resultado_final = input("\nResultado final (Liberado / Bloqueado): ").strip()

    # Envia todos os dados coletados para serem processados e salvos em definitivo
    id_inspecao = operacoes.registrar_inspecao(
        tipo_maquina,
        numero_equipamento,
        inspetor_logado["nome"],
        resultado_final,
        operacoes.itens_checklist
    )

    print(f"\n Inspeção registrada com sucesso! (ID {id_inspecao})")



def tela_listar_inspecoes():
    """
    Gerencia a tela de relatórios e consulta de inspeções.
    Solicita um filtro opcional por ID de equipamento. Caso o usuário deixe em branco, o sistema busca o histórico geral de todas as vistorias realizadas.
    """
    print("\n--- LISTAR INSPEÇÕES ---")
    numero_equipamento = input("Filtrar por equipamento (deixe em branco para listar todas): ").strip()

    # Operador ternário: se o usuário só apertar ENTER, transforma a string vazia em None
    numero_equipamento = numero_equipamento if numero_equipamento else None

    # Busca registros através do método.
    resultados = operacoes.listar_inspecoes(numero_equipamento)

    # Tratamento de segurança caso a busca não retorne nenhum dado
    if not resultados:
        print("\nNenhuma inspeção encontrada.")
        return
    
    # Exibe a quantidadem total encontrada e varre a lista exibindo os detalhes formatados.
    print(f"\n{len(resultados)} inspeção(ões) encontrada(s):")
    for inspecao in resultados:
        print("-" * 50)
        print(f"ID: {inspecao['id']}")
        print(f"Máquina: {inspecao['tipo_maquina']} - {inspecao['numero_equipamento']}")
        print(f"Inspetor: {inspecao['inspetor_manutencao']}")
        print(f"Data: {inspecao['data_hora']}")
        print(f"Resultado: {inspecao['resultado_final']}")
        print("-" * 50)



def main():
    # 1. Garante que as tabelas existam (chama as 3 funções de criar tabela)
    database.criar_tabela()
    database.criar_tabela_itens()
    database.criar_tabela_inspetores()

    # 2. Faz o login
    inspetor_logado = fazer_tela_login()

    # 3. Se o login falhou, encerra o programa aqui
    if inspetor_logado is None:
        return

    # 4. Loop do menu 
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            tela_registrar_inspecao(inspetor_logado)
        elif opcao =="2":
            tela_listar_inspecoes()
        elif opcao =="0":
            print("\nAté Logo!")
            break
        else:
            print("\nOpção Inválida.")

        pausar()

if __name__ == "__main__":
    main()
