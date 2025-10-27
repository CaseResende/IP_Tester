import flet as ft
from app.config import TABLE_WIDTH


def create_ip_input():
    """
    Cria o campo de texto onde o usuário insere os endereços IP.
    """
    return ft.TextField(
        label="Insira os endereços IP separados por vírgula",
        hint_text="Ex: 192.168.0.1, 172.16.0.1, 10.0.0.5",
        multiline=True,
        width=TABLE_WIDTH,
    )


def create_error_msg():
    """
    Cria o campo de texto para exibição de mensagens de erro
    ou avisos importantes para o usuário.
    """
    return ft.Text(
        value="",
        color=ft.Colors.RED_400,
        size=16,
        weight=ft.FontWeight.BOLD,
    )


def create_run_button():
    """
    Cria o botão responsável por iniciar o teste de conectividade.
    """
    return ft.ElevatedButton(
        text="Testar Conectividade",
        icon=ft.Icons.PLAY_ARROW,
        bgcolor=ft.Colors.BLUE_ACCENT_400,
        color=ft.Colors.WHITE,
        width=250,
    )


def create_copy_button():
    """
    Cria o botão que copia os resultados do teste
    para a área de transferência.
    """
    return ft.ElevatedButton(
        text="Copiar resultados",
        icon=ft.Icons.COPY_ALL,
        bgcolor=ft.Colors.BLUE_ACCENT_400,
        color=ft.Colors.WHITE,
        width=250,
        visible=False,
    )


def create_theme_button():
    """
    Cria o botão de alternância entre temas (claro/escuro).
    """
    return ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        tooltip="Alternar tema",
        icon_color=ft.Colors.WHITE,
        style=ft.ButtonStyle(shape=ft.CircleBorder()),
        visible=True,
    )


def create_table():
    """
    Cria a tabela principal onde os resultados dos pings são exibidos.
    """
    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Endereço IP", text_align=ft.TextAlign.CENTER)),
            ft.DataColumn(ft.Text("Status", text_align=ft.TextAlign.CENTER)),
            ft.DataColumn(ft.Text("Tempo (ms)", text_align=ft.TextAlign.CENTER)),
            ft.DataColumn(ft.Text("Mensagem", text_align=ft.TextAlign.CENTER)),
        ],
        rows=[],
        width=TABLE_WIDTH,
        visible=False,
    )


def update_table(table, results):
    """
    Atualiza a tabela com os resultados retornados pela função `ping_ips`.
    """
    table.rows.clear()

    for ip, online, rtt, msg in results:
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


def create_progress_bar():
    """
    Cria a barra de progresso exibida enquanto os testes estão em execução.
    """
    return ft.ProgressBar(width=TABLE_WIDTH, visible=False)


def create_header(theme_btn):
    """
    Cria o cabeçalho principal da aplicação, exibindo:
    """
    return ft.Row(
        controls=[
            ft.Text(
                "🔎 Verificador de Conectividade",
                size=28,
                weight=ft.FontWeight.BOLD,
            ),
            theme_btn
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        width=TABLE_WIDTH,
    )
