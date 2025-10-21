import flet as ft
from app.utils import ping_ips, process_input
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
        table.rows.clear()
        error_msg.value = ""
        progress.visible = True
        page.update()

        raw_ips = ip_input.value.strip()
        if not raw_ips:
            error_msg.value = "Por favor, insira pelo menos um IP!"
            progress.visible = False
            table.visible = False
            page.update()
            return

        valid_ips, invalid_ips = process_input(raw_ips)

        if not valid_ips:
            error_msg.value = "Todos os IPs inseridos são inválidos!"
            progress.visible = False
            table.visible = False
            page.update()
            return

        results = ping_ips(valid_ips)

        if invalid_ips:
            error_msg.value = f"Os seguintes IPs são inválidos:\n{', '.join(invalid_ips)}"
        else:
            error_msg.value = ""

        update_table(table, results)
        progress.visible = False
        table.visible = True
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
        error_msg,
    )

# Executa o app
if __name__ == "__main__":
    ft.app(target=main)
