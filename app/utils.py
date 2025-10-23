import ipaddress
from pythonping import ping
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.config import MAX_WORKERS, TIMEOUT


# ============================================================
# 🔹 Manipulação e validação de IPs
# ============================================================

def list_ips(raw_ips: str) -> list[str]:
    """
    Recebe uma string com IPs separados por vírgula,
    remove espaços em branco e duplicados, e retorna uma lista limpa.

    Exemplo:
        Entrada: "192.168.0.1, 192.168.0.2,192.168.0.1"
        Saída: ["192.168.0.1", "192.168.0.2"]
    """
    ip_list = [ip.strip() for ip in raw_ips.split(",") if ip.strip()]
    return list(set(ip_list))


def validate_ip(ip_list: list[str]) -> tuple[list[str], list[str]]:
    """
    Valida os IPs da lista, separando válidos e inválidos.
    Retorna uma tupla contendo:
        (lista_de_ips_válidos, lista_de_ips_inválidos)

    Obs: Os IPs válidos são ordenados numericamente.
    """
    valid_ip_list = []
    invalid_ip_list = []

    for ip in ip_list:
        try:
            ipaddress.ip_address(ip)  # Verifica se o IP é válido
            valid_ip_list.append(ip)
        except ValueError:
            invalid_ip_list.append(ip)

    # Ordena listas para melhor exibição
    valid_ip_list = sorted(valid_ip_list, key=lambda x: int(ipaddress.IPv4Address(x)))
    invalid_ip_list = sorted(invalid_ip_list)

    return valid_ip_list, invalid_ip_list


def process_input(raw_ips: str) -> tuple[list[str], list[str]]:
    """
    Realiza o pré-processamento da entrada do usuário:
    - Separa IPs da string informada
    - Remove duplicados
    - Valida e retorna listas de válidos e inválidos
    """
    ip_list = list_ips(raw_ips)
    valid_ips, invalid_ips = validate_ip(ip_list)
    return valid_ips, invalid_ips


# ============================================================
# 🔹 Execução dos pings
# ============================================================

def ping_ip(ip: str, timeout: float = TIMEOUT) -> tuple[str, bool, float | None, str]:
    """
    Executa um ping em um único endereço IP.

    Retorna uma tupla no formato:
        (ip_str, online, rtt, mensagem)

    Onde:
        ip_str   -> endereço IP (string)
        online   -> True se o host respondeu ao ping, False caso contrário
        rtt      -> tempo médio de resposta (ms) ou None se sem resposta
        mensagem -> texto de status ("OK", "Sem resposta ICMP", "Erro: ...")
    """
    try:
        # Valida e normaliza o IP
        ip_str = str(ipaddress.ip_address(ip.strip()))

        # Envia 1 pacote ICMP e aguarda resposta
        resp = ping(ip_str, count=1, timeout=timeout)

        # Se houver resposta ICMP
        if resp.success():
            # Usa o RTT médio (ou mínimo/máximo, se disponível)
            rtt = (resp.rtt_avg or resp.rtt_min or resp.rtt_max) * 1000
            return ip_str, True, round(rtt, 2), "OK"

        # Sem resposta ICMP
        return ip_str, False, None, "Sem resposta ICMP"

    except Exception as e:
        # Trata qualquer erro inesperado
        return ip, False, None, f"Erro: {e}"


def ping_ips(ip_list: list[str], max_workers: int = MAX_WORKERS) -> list[tuple]:
    """
    Executa pings em paralelo utilizando ThreadPoolExecutor.

    Parâmetros:
        ip_list: lista de IPs válidos
        max_workers: número máximo de threads simultâneas

    Retorna:
        Lista ordenada de tuplas no formato:
        (ip, online, rtt, mensagem)
    """
    results = []

    # Executor para execução multithread
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(ping_ip, ip): ip for ip in ip_list}

        # Conforme cada ping termina, adiciona o seu resultado
        for fut in as_completed(futures):
            results.append(fut.result())

    # Ordena os resultados pelo valor numérico do IP
    return sorted(results, key=lambda x: int(ipaddress.IPv4Address(x[0])))
