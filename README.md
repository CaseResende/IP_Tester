# 📝 IP Tester - Verificador de Conectividade

![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/Flet-Framework-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Ativo-success)

## 📌 Descrição
O **IP Tester** é um aplicativo desenvolvido em **Python + Flet** para testar a conectividade de uma lista de endereços IP de forma rápida, visual e responsiva.

Permite inserir múltiplos IPs separados por vírgula, valida e ordena automaticamente, realiza **pings em paralelo** e exibe de forma clara quais IPs estão **online** ou **offline**, incluindo o **tempo de resposta (RTT)** e mensagens de status.

---

## ⚙️ Funcionalidades

- Inserção de múltiplos endereços IP (separados por vírgula)
- Validação automática dos endereços IP (IPv4)
- Execução de **ping paralelo** com até 50 threads
- Exibição dos resultados com:
  - Endereço IP  
  - Status (Online/Offline)  
  - Tempo médio de resposta (ms)  
  - Mensagem de erro ou sucesso
- Cópia dos resultados para a área de transferência
- Alternância entre **modo claro e escuro**
- Interface moderna e responsiva com **Flet**

---

## 📂 Estrutura do Projeto


```
ip_tester/
├── app/
│ ├── main.py           # Arquivo principal do app (inicializa a interface e eventos)
│ ├── ui_components.py  # Componentes visuais reutilizáveis (botões, tabelas, etc.)
│ ├── utils.py          # Funções de lógica e processamento (ping, validação de IPs)
│ └── config.py         # Configurações globais do projeto
│
├── requirements.txt    # Dependências do projeto
├── .gitignore          # Arquivos a ignorar no Git
└── README.md           # Documentação do projeto
```

---

## 📂 Arquivos
### `main.py`
Arquivo principal que inicializa a interface Flet, conecta os componentes e controla os eventos principais:
- Execução dos pings
- Atualização da tabela de resultados
- Alternância de tema
- Cópia dos resultados formatados

### `ui_components.py`
Define todos os componentes visuais da interface:
- Campo de entrada para IPs  
- Botão de execução  
- Barra de progresso  
- Tabela de resultados  
- Botão de copiar  
- Cabeçalho com botão de alternância de tema

### `utils.py`
Contém as funções de lógica e backend:
- `list_ips()`: limpa, separa e remove duplicados  
- `validate_ip()`: valida e separa IPs válidos e inválidos  
- `process_input()`: integra listagem e validação  
- `ping_ip()`: executa o ping em um IP individual  
- `ping_ips()`: executa os pings em paralelo usando `ThreadPoolExecutor`

### `config.py`
Define parâmetros globais:
- `MAX_WORKERS`: número máximo de threads simultâneas  
- `TIMEOUT`: tempo limite para cada ping (em segundos)  
- `TABLE_WIDTH`: largura padrão da tabela de resultados

---

## 🚀 Exemplo de Uso
### 📥 Entrada:
`192.168.0.1,192.168.0.10,10.0.0.5`


### 📤 Saída:
| Endereço IP | Status       | Tempo (ms) | Mensagem          |
|------------|-------------|------------|-----------------|
| 192.168.0.1 | 🟢 Online   | 0.82       | OK               |
| 192.168.0.10| 🔴 Offline  | —          | Sem resposta ICMP|
| 10.0.0.5   | 🟢 Online   | 0.56       | OK               |

---

## 🛠 Como Executar
### 💻 Requisitos:
- **Python 3.13+**
- Pacotes: `flet`, `pythonping`

### 🧩 Instalação:

1. Clone ou baixe este repositório:
```bash
  git clone https://github.com/seu_usuario/ip_tester.git
  cd ip_tester
```
3. Crie um ambiente virtual e instale as dependências:
```bash
  python -m venv .venv        # Linux / macOS
  source .venv/bin/activate   # Windows
  .venv\Scripts\activate
  pip install -r requirements.txt
```
4. Execute o arquivo principal:
```bash
  python -m app.main
```
5. Insira os IPs separados por vírgula no campo de texto e clique em **Testar Conectividade**.

---

## 🔥 Melhorias Futuras
- Exibir percentual real na barra de progresso.
- Contador de IPs online/offline.
- Exportação dos resultados para CSV.
- Configuração de intervalo de tempo entre pings.
- Histórico de execuções.

---

## 🤝 Contribuições
Contribuições são bem-vindas! Para contribuir:
1. Faça um fork deste repositório.
2. Crie uma branch para a sua feature:
```bash
  git checkout -b feature/nova-feature
```
3. Commit as suas alterações:
```bash
  git commit -m "Adiciona nova feature"
```
4. Envie a sua branch:
```bash
  git push origin feature/nova-feature
```
5. Abra um Pull Request 🎉.

---

## 📜 Licença
Este projeto está licenciado sob a Licença MIT – veja o arquivo [LICENSE](https://github.com/CaseResende/IP_Tester/blob/main/LICENSE) para mais detalhes.

Desenvolvido por **[Carlos André Resende Belo](https://github.com/CaseResende)**. 😎