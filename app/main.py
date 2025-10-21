import flet as ft
import ipaddress
from app.ping_utils import ping_ips, list_ips
from app.ui_components import *

def main(page: ft.Page):
    # Configurações da página
    page.title = "Verificador de Conectividade - Ping de IPs"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 30
    page.scroll = ft.ScrollMode.AUTO

    # Criação dos componentes
    ip_input = create_ip_input()
    run_button = create_run_button()
    table = create_table()
    progress = create_progress_bar()
    error_msg = create_error_msg()

    # Função chamada ao clicar no botão
    def run_ping(e):
        table.rows.clear()       # Limpa resultados anteriores
        progress.visible = True   # Mostra barra de progresso
        page.update()

        # Obtém lista de IPs do campo de texto
        raw_ips = ip_input.value.strip()
        if not raw_ips:
            # Exibe uma mensagem de erro se não houver IP digitado
            error_msg.value = "Por favor, insira pelo menos um IP!"
            progress.visible = False
            table.visible = False
            page.update()
            return
        else:
            error_msg.value = ""

            # Chama a função list_ips para processar e ordenar os IPs
            ip_list = list_ips(raw_ips)

            # Executa os pings em paralelo
            results = ping_ips(ip_list)

            # Preenche a tabela com os resultados
            for ip, online, rtt, msg in sorted(results, key=lambda x: int(ipaddress.IPv4Address(x[0]))):
                color = ft.Colors.GREEN_400 if online else ft.Colors.RED_400
                status_text = "🟢 Online" if online else "🔴 Offline"
                table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(ip)),
                            ft.DataCell(ft.Text(status_text, color=color)),
                            ft.DataCell(ft.Text(f"{rtt:.2f}" if rtt else "—")),
                            ft.DataCell(ft.Text(msg)),
                        ]
                    )
                )

            # Oculta barra de progresso e exibe a tabela
            progress.visible = False
            table.visible = True

            # Atualiza a página
            page.update()

    # Conecta o botão ao evento
    run_button.on_click = run_ping

    # Layout principal da página
    page.add(
        ft.Text("🔎 Verificador de Conectividade", size=28, weight=ft.FontWeight.BOLD),
        ip_input,
        run_button,
        progress,
        ft.Divider(),
        error_msg,
        table
    )

# Executa o app
if __name__ == "__main__":
    ft.app(target=main)
