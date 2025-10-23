import flet as ft
from app.utils import ping_ips, process_input
from app.ui_components import *


def main(page: ft.Page):
    """
    Função principal da aplicação Flet.
    Responsável por configurar a interface, criar os componentes,
    conectar os eventos e exibir os resultados dos testes de conectividade.
    """

    # === Configurações da página ===
    page.title = "Verificador de Conectividade - Ping de IPs"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.scroll = ft.ScrollMode.AUTO

    # === Criação dos componentes visuais ===
    ip_input = create_ip_input()          # Campo de entrada dos IPs
    run_button = create_run_button()      # Botão de execução
    table = create_table()                # Tabela de resultados
    progress = create_progress_bar()      # Barra de progresso
    error_msg = create_error_msg()        # Mensagem de erro/alerta
    copy_btn = create_copy_button()       # Botão para copiar resultados
    theme_btn = create_theme_button()     # Botão de alternância de tema
    header = create_header(theme_btn)     # Cabeçalho da interface

    # Lista que armazenará os resultados dos testes
    results = []

    # === Funções internas ===
    def change_theme_mode(e):
        """
        Alterna entre o modo claro e escuro da interface.
        Atualiza o ícone e a cor do botão de tema.
        """
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_btn.icon = ft.Icons.DARK_MODE
            theme_btn.icon_color = ft.Colors.BLACK
        else:
            page.theme_mode = ft.ThemeMode.DARK
            theme_btn.icon = ft.Icons.LIGHT_MODE
            theme_btn.icon_color = ft.Colors.WHITE

        page.update()

    def run_ping(e):
        """
        Executa os pings nos IPs informados, atualiza a tabela e exibe mensagens.
        Controla o estado dos componentes durante a execução.
        """
        nonlocal results

        # Reset de estados visuais
        table.rows.clear()
        error_msg.value = ""
        table.visible = False
        progress.visible = True
        copy_btn.visible = False
        page.update()

        raw_ips = ip_input.value.strip()

        # === Validação do campo ===
        if not raw_ips:
            error_msg.value = "Por favor, insira pelo menos um IP!"
            progress.visible = False
            page.update()
            return

        # === Processamento dos IPs ===
        valid_ips, invalid_ips = process_input(raw_ips)

        # Caso todos os IPs sejam inválidos
        if not valid_ips:
            error_msg.value = "Todos os IPs inseridos são inválidos!"
            progress.visible = False
            page.update()
            return

        # === Execução dos pings ===
        results = ping_ips(valid_ips)

        # Mensagem sobre IPs inválidos
        if invalid_ips:
            error_msg.value = f"Os seguintes IPs são inválidos:\n{', '.join(invalid_ips)}"

        # === Atualização da interface ===
        update_table(table, results)
        progress.visible = False
        table.visible = True
        copy_btn.visible = True
        page.update()

    def copy_results(e):
        """
        Copia os resultados formatados da tabela para a área de transferência.
        Exibe mensagem de confirmação.
        """
        if not results:
            error_msg.value = "Nenhum resultado disponível para copiar!"
            page.update()
            return

        # Cabeçalho da tabela (formato texto)
        text_to_copy = f"{'Endereço IP':<16} | {'Status':^10} | {'Tempo (ms)':^10} | {'Mensagem'}\n"
        text_to_copy += "-" * 60 + "\n"

        # Linhas de dados
        for ip, online, rtt, msg in results:
            status_text = "🟢 Online" if online else "🔴 Offline"
            rtt_text = f"{rtt:.2f}" if rtt else "—"
            text_to_copy += f"{ip:<16} | {status_text:<10} | {rtt_text:<10} | {msg}\n"

        # Copia para a área de transferência
        page.set_clipboard(text_to_copy)
        error_msg.value = "Resultados copiados para a área de transferência!"
        page.update()

    # === Conexão de eventos ===
    run_button.on_click = run_ping
    copy_btn.on_click = copy_results
    theme_btn.on_click = change_theme_mode

    # === Layout principal ===
    page.add(
        header,
        ip_input,
        run_button,
        progress,
        ft.Divider(),
        copy_btn,
        error_msg,
        table,
    )


# === Execução do aplicativo ===
if __name__ == "__main__":
    ft.app(target=main)
