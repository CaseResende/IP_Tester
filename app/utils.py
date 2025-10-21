import ipaddress
from pythonping import ping
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.config import MAX_WORKERS, TIMEOUT


def list_ips(raw_ips):
    """
    Recebe uma string com IPs separados por vírgula, remove duplicados,
    remove espaços em branco e retorna uma lista.
    """
    ip_list = [ip.strip() for ip in raw_ips.split(",") if ip.strip() != ""]

    return list(set(ip_list))


def validate_ip(ip_list):
    """
    Valida os IPs da lista, separando válidos e inválidos.
    Retorna (lista_válidos, lista_inválidos)
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


def process_input(raw_ips):
    ip_list = list_ips(raw_ips)
    valid_ips, invalid_ips = validate_ip(ip_list)
    return valid_ips, invalid_ips


def ping_ip(ip, timeout=TIMEOUT):
    """
    Executa um ping em um único IP.
    Retorna uma tupla: (ip_str, online:bool, rtt:float|None, msg:str)
    """
    try:
        # Valida e normaliza o IP
        ip_str = str(ipaddress.ip_address(ip.strip()))

        # Envia 1 pacote ICMP
        resp = ping(ip_str, count=1, timeout=timeout)

        # Se houver resposta
        if resp.success():
            # Converte o RTT para ms
            rtt = (resp.rtt_avg or resp.rtt_min or resp.rtt_max) * 1000
            return ip_str, True, round(rtt, 2), "OK"
        else:
            # Sem resposta ICMP
            return ip_str, False, None, "Sem resposta ICMP"
    except Exception as e:
        # Caso de erro (IP inválido, timeout, etc)
        return ip, False, None, f"Erro: {e}"


def ping_ips(ip_list, max_workers=MAX_WORKERS):
    """
    Executa ping paralelo em uma lista de IPs.
    Retorna uma lista de tuplas (ip, online, rtt, msg)
    """
    results = []
    # Executor para multithreading
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(ping_ip, ip): ip for ip in ip_list}
        # Conforme cada ping finaliza, adiciona ao resultado
        for fut in as_completed(futures):
            results.append(fut.result())
    return sorted(results, key=lambda x: int(ipaddress.IPv4Address(x[0])))
