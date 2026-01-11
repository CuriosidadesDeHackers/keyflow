import flet as ft

def main(page: ft.Page):
    page.add(ft.Text("Debug FilePicker"))
    
    # Initialize FilePicker
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    page.update() # Register it explicitly
    
    def on_click(e):
        print("Opening picker...")
        try:
            file_picker.pick_files(dialog_title="Test Picker")
        except Exception as ex:
            print(f"Error picking files: {ex}")
            page.add(ft.Text(f"Error: {ex}", color="red"))
            page.update()

    page.add(ft.ElevatedButton("Pick File", on_click=on_click))
    page.update()

if __name__ == "__main__":
    ft.run(target=main)
