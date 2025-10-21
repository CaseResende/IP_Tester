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
    copy_btn = create_copy_button()

    results = []

    # Função chamada ao clicar no botão
    def run_ping(e):
        nonlocal results
        table.rows.clear()
        error_msg.value = ""
        table.visible = False
        progress.visible = True
        copy_btn.visible = False
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
        copy_btn.visible = True
        page.update()


    def copy_results(e):
        if not results:
            error_msg.value = "Nenhum resultado disponível para copiar!"
            page.update()
            return

        # Cabeçalho
        text_to_copy = f"{'Endereço IP':<16} {'Status':<10} {'Tempo (ms)':<10} Mensagem\n"
        text_to_copy += "-" * 50 + "\n"

        # Cada linha da tabela
        for ip, online, rtt, msg in results:
            status_text = "🟢 Online" if online else "🔴 Offline"
            rtt_text = f"{rtt:.2f}" if rtt else "—"
            text_to_copy += f"{ip:<16} {status_text:<10} {rtt_text:<10} {msg}\n"

        # Copia para a área de transferência
        page.set_clipboard(text_to_copy)
        error_msg.value = "Resultados copiados para a área de transferência!"
        page.update()


    # Conecta o botão ao evento
    run_button.on_click = run_ping
    copy_btn.on_click = copy_results

    # Layout principal da página
    page.add(
        ft.Text("🔎 Verificador de Conectividade", size=28, weight=ft.FontWeight.BOLD),
        ip_input,
        run_button,
        progress,
        ft.Divider(),
        copy_btn,
        error_msg,
        table,
    )

# Executa o app
if __name__ == "__main__":
    ft.app(target=main)
