import flet as ft
import sys

print(f"Python executable: {sys.executable}")
print(f"Flet version: {ft.version.version if hasattr(ft.version, 'version') else 'Unknown'}")
try:
    print(f"Flet __version__: {ft.__version__}")
except:
    pass

def main(page: ft.Page):
    print(f"Page object: {page}")
    print(f"Page type: {type(page)}")
    print(f"Has 'open' attribute: {hasattr(page, 'open')}")
    print(f"Page attributes: {dir(page)}")
    page.window_close()

if __name__ == "__main__":
    print("Starting Flet app...")
    try:
        ft.run(main)
    except Exception as e:
        print(f"Error running app: {e}")
