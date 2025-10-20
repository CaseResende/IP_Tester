# 📝 IP Tester - Verificador de Conectividade

![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/Flet-Framework-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Ativo-success)

## 📌 Descrição
O **IP Tester** é um aplicativo desenvolvido em **Python + Flet** para testar a conectividade de uma lista de endereços IP de forma rápida e visual.  

Permite inserir múltiplos IPs separados por vírgula, ordena-os automaticamente, realiza ping em paralelo e exibe se estão **online** ou **offline**, além do tempo de resposta (RTT) em milissegundos.

---

## ⚙️ Funcionalidades
- Testa múltiplos IPs simultaneamente usando threads.
- Ordena IPs numericamente antes de exibir os resultados.
- Interface moderna e responsiva utilizando **Flet**.
- Mostra status **Online/Offline** com cores diferentes.
- Exibe RTT (tempo de resposta) em milissegundos.
- Barra de progresso enquanto os testes são executados.

---

## 📂 Estrutura do Projeto


```bash

ip_tester/
│
├── app/                     # Código principal da aplicação
│   ├── __init__.py
│   ├── main.py              # Script que roda a interface Flet
│   ├── ping_utils.py        # Funções de ping
│   ├── ui_components.py     # Componentes de interface
│   ├── config.py            # Configurações globais
│
├── tests/                   # Testes unitários
│   ├── __init__.py
│   ├── test_ping_utils.py
│   └── test_ui_components.py
│
├── requirements.txt         # Dependências do projeto
├── README.md                # Documentação do projeto
├── .gitignore               # Arquivos a ignorar no Git
└── setup.py / pyproject.toml # Distribuição opcional
```

---

## 📂 Arquivos
### `main.py`
Arquivo principal que inicializa a interface Flet, conecta os componentes da UI e chama as funções de ping.

### `ping_utils.py`
Módulo responsável por:
- Executar ping em um IP individual (`ping_ip`).
- Executar ping paralelo em múltiplos IPs (`ping_ips`).

### `ui_components.py`
Módulo que cria componentes reutilizáveis da interface:
- Campo de entrada para IPs.
- Botão de execução.
- Tabela de resultados.
- Barra de progresso.

### `config.py`
Configurações globais:
- Timeout de ping.
- Número máximo de threads (`MAX_WORKERS`).
- Largura padrão da tabela.

---

## 🚀 Exemplo de Uso
### 📥 Entrada:
`192.168.0.1, 192.168.0.10, 10.0.0.5`


### 📤 Saída:
| Endereço IP | Status       | Tempo (ms) | Mensagem          |
|------------|-------------|------------|-----------------|
| 192.168.0.1 | 🟢 Online   | 0.82       | OK               |
| 192.168.0.10| 🔴 Offline  | —          | Sem resposta ICMP|
| 10.0.0.5   | 🟢 Online   | 0.56       | OK               |

---

## 🛠 Como Executar

### Via Interface Gráfica
1. Certifique-se de ter o Python instalado.
2. Clone ou baixe este repositório:
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

## 🔥 Melhorias Futuras
- Barra de progresso percentual real.
- Contagem de IPs online/offline em tempo real.
- Temas claros/escuros ajustáveis.
- Exportar resultados para CSV.

## 🤝 Contribuições
Contribuições são bem-vindas! Para contribuir:
1. Faça um fork deste repositório.
2. Crie uma branch para a sua feature:
```bash
  git checkout -b feature/nova-feature
```
3. Commit as suas alterções:
```bash
  git commit -m "Adiciona nova feature"
```
4. Push para a sua branch:
```bash
  git push origin feature/nova-feature
```
5. Abra um Pull Request.

## 📜 Licença
Este projeto está licenciado sob a Licença MIT – veja o arquivo [LICENSE](https://github.com/CaseResende/IP_Tester/blob/main/LICENSE) para mais detalhes.

Desenvolvido por **[Carlos André Resende Belo](https://github.com/CaseResende)**. 😎