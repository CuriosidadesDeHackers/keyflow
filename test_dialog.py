#!/usr/bin/env python3
"""Test simple para verificar que los diálogos funcionan"""
import flet as ft

def main(page: ft.Page):
    page.title = "Test Dialog"
    page.theme_mode = ft.ThemeMode.DARK
    
    def show_dialog(e):
        print("Button clicked!")  # Debug
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Test Dialog"),
            content=ft.Text("This is a test dialog"),
            actions=[
                ft.TextButton("Close", on_click=lambda e: close_dialog(dialog)),
            ],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
        print("Dialog should be open now")  # Debug
    
    def close_dialog(dialog):
        dialog.open = False
        page.update()
    
    btn = ft.ElevatedButton(
        "Click me",
        icon=ft.icons.Icons.ADD,
        on_click=show_dialog,
    )
    
    page.add(btn)

if __name__ == "__main__":
    ft.run(main)
