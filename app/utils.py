import ipaddress
from pythonping import ping
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.config import MAX_WORKERS, TIMEOUT


def list_ips(colected_ips):
    """
    Recebe uma string com IPs separados por vírgula,
    remove espaços em branco e duplicados, e retorna uma lista limpa.
    """
    ip_list = [ip.strip() for ip in colected_ips.split(",") if ip.strip()]
    return list(set(ip_list))


def validate_ip(ip_list):
    """
    Valida os IPs da lista, separando válidos e inválidos.
    Retorna uma tupla com os ips ordenados contendo:
        (lista_de_ips_válidos, lista_de_ips_inválidos)
    """
    valid_ip_list = []
    invalid_ip_list = []

    for ip in ip_list:
        try:
            ipaddress.ip_address(ip)
            valid_ip_list.append(ip)
        except ValueError:
            invalid_ip_list.append(ip)

    valid_ip_list = sorted(valid_ip_list, key=lambda x: int(ipaddress.IPv4Address(x)))
    invalid_ip_list = sorted(invalid_ip_list)

    return valid_ip_list, invalid_ip_list


def process_input(colected_ips):
    """
    Realiza o pré-processamento da entrada do usuário:
    - Separa IPs da string informada
    - Remove duplicados
    - Valida e retorna listas de válidos e inválidos
    """
    ip_list = list_ips(colected_ips)
    valid_ips, invalid_ips = validate_ip(ip_list)
    return valid_ips, invalid_ips


def ping_ip(ip, timeout = TIMEOUT):
    """
    Executa um ping em um único endereço IP.

    Retorna uma tupla no formato:
        (ip_str, online, rtt, mensagem)
    """
    try:
        ip_str = str(ipaddress.ip_address(ip.strip()))

        resp = ping(ip_str, count=1, timeout=timeout)

        if resp.success():
            rtt = (resp.rtt_avg or resp.rtt_min or resp.rtt_max) * 1000
            return ip_str, True, round(rtt, 2), "OK"

        return ip_str, False, None, "Sem resposta ICMP"

    except Exception as e:
        return ip, False, None, f"Erro: {e}"


def ping_ips(ip_list, max_workers = MAX_WORKERS):
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

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(ping_ip, ip): ip for ip in ip_list}

        for future in as_completed(futures):
            results.append(future.result())

    return sorted(results, key=lambda x: int(ipaddress.IPv4Address(x[0])))
