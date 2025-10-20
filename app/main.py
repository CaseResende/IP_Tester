import flet as ft
import ipaddress
from app.ping_utils import ping_ips
from app.ui_components import create_ip_input, create_run_button, create_table, create_progress_bar

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

    # Função chamada ao clicar no botão
    def run_ping(e):
        table.rows.clear()       # Limpa resultados anteriores
        progress.visible = True   # Mostra barra de progresso
        page.update()

        # Obtém lista de IPs do campo de texto
        raw_ips = ip_input.value.strip()
        if not raw_ips:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, insira pelo menos um IP!"))
            page.snack_bar.open = True
            page.update()
            progress.visible = False
            return

        # Divide, remove duplicados e ordena os IPs
        ip_list = [ip.strip() for ip in raw_ips.split(",") if ip.strip() != ""]
        ip_list = sorted(set(ip_list), key=lambda x: int(ipaddress.IPv4Address(x)))

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

        progress.visible = False  # Oculta barra de progresso
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
        table,
    )

# Executa o app
if __name__ == "__main__":
    ft.app(target=main)
