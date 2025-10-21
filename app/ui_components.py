import ipaddress
import flet as ft
from app.config import TABLE_WIDTH


def create_ip_input():
    """Cria o campo de texto para inserir os IPs separados por vírgula"""
    return ft.TextField(
        label="Insira os endereços IP separados por vírgula",
        hint_text="Ex: 192.168.0.1, 172.16.0.1, 10.0.0.5",
        multiline=True,
        width=TABLE_WIDTH,
    )


def create_run_button():
    """Cria o botão de execução do ping"""
    return ft.ElevatedButton(
        "Testar Conectividade 🧭",
        icon=ft.Icons.PLAY_ARROW,
        bgcolor=ft.Colors.BLUE_ACCENT_400,
        color=ft.Colors.WHITE,
        width=250,
    )


def create_error_msg():
    """Cria a mensagem de erro para inserir um IP"""
    return ft.Text(
        value="",
        color=ft.Colors.RED_400,
        size=16,
        weight=ft.FontWeight.BOLD,
    )


def create_table():
    """Cria a tabela para exibir resultados"""
    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Endereço IP", text_align=ft.TextAlign.CENTER)),
            ft.DataColumn(ft.Text("Status", text_align=ft.TextAlign.CENTER)),
            ft.DataColumn(ft.Text("Tempo (ms)", text_align=ft.TextAlign.CENTER)),
            ft.DataColumn(ft.Text("Mensagem", text_align=ft.TextAlign.CENTER)),
        ],
        rows=[],
        width=TABLE_WIDTH,
        visible=False
    )


def create_progress_bar():
    """Cria a barra de progresso oculta inicialmente"""
    return ft.ProgressBar(width=TABLE_WIDTH, visible=False)


def update_table(table, results):
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
