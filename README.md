# 🛠️ Checklist de Inspeção de Equipamentos

Sistema de linha de comando (CLI) para gerenciar inspeções de segurança em
equipamentos portuários (RTG e Reach Stacker): login de inspetores, checklist
item a item, histórico de inspeções e liberação/bloqueio de equipamento.

Este projeto nasceu da minha experiência prática como operador de guindaste em
terminal portuário, onde inspeções de segurança fazem parte da rotina diária.
A proposta foi recriar esse processo como uma aplicação real, com banco de
dados e autenticação de usuários.

## Funcionalidades

- **Login com autenticação**: cada inspetor tem nome e matrícula cadastrados;
  senha (matrícula) armazenada como hash, nunca em texto puro. 3 tentativas
  antes do bloqueio de acesso.
- **Checklist estruturado**: percorre 8 itens de verificação (pneus, cabos,
  sinalização sonora, câmeras, botões de emergência, vidros, óleo, água),
  registrando status (OK/Pendência) e observação quando houver problema.
- **Validação de equipamento**: só aceita números de equipamento previamente
  cadastrados (RTG-01 a RTG-08, RS-01 a RS-04), evitando erros de digitação.
- **Resultado final controlado pelo inspetor**: Liberado ou Bloqueado — a
  decisão é sempre manual, nunca automática, refletindo o processo real de
  segurança.
- **Histórico de inspeções**: consulta com filtro opcional por equipamento.

## Tecnologias

- **Python 3** (sem dependências externas)
- **SQLite** (banco de dados local, via módulo `sqlite3` da biblioteca padrão)
- **hashlib** (hash de senha, biblioteca padrão)

## Estrutura do projeto

```
checklist-equipamentos/
├── main.py          # Menu do terminal, login e telas de interação
├── operacoes.py      # Regras de negócio (login, registrar inspeção, listar...)
├── database.py        # Conexão e criação das tabelas no SQLite
└── README.md
```

## Modelo de dados

Três tabelas relacionadas:

- **`inspetores`** — nome e matrícula (hash) de quem pode logar no sistema
- **`inspecoes`** — dados gerais de cada inspeção (máquina, inspetor, data, resultado)
- **`itens_inspecao`** — cada item do checklist, ligado à inspeção correspondente
  por chave estrangeira (`inspecao_id`)

## Como rodar

Não precisa instalar nenhuma dependência — só Python 3.

```bash
git clone https://github.com/FabianoSeara/checklist-equipamentos.git
cd checklist-equipamentos
python main.py
```

O banco de dados (`inspecoes.db`) é criado automaticamente na primeira execução.

**Inspetores cadastrados para teste:**
| Nome | Matrícula |
|------|-----------|
| Ricardo | 20 |
| Rafael | 21 |
| Fabiano | 22 |
| João | 23 |

## Próximos passos

- [ ] Validar também o tipo de máquina (RTG/RS) contra uma lista fixa
- [ ] Exibir os itens do checklist na tela de listagem, não só o resumo
- [ ] Tela para cadastrar novos inspetores direto pelo menu
- [ ] Exportar relatórios de inspeção em PDF ou CSV

---

Projeto desenvolvido por [Fabiano Seára](https://github.com/FabianoSeara) como
parte do meu portfólio de transição de carreira para desenvolvimento de
software, com apoio de IA (Claude) no processo de aprendizado.
