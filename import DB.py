import shutil
import os

def backup_to_drive(db_file, drive_folder):
    try:
        shutil.copy(db_file, drive_folder)
        print("Archivo copiado exitosamente a Google Drive.")
    except Exception as e:
        print(f"Error al copiar el archivo a Google Drive: {e}")

if __name__ == "__main__":
    db_file_path = r"C:\Users\Diego\Documents\GitHub\pdv\pdvDB.sqlite"
    drive_folder_path = r"G:\Mi unidad\TF"  # Ruta de la carpeta localmente sincronizada con Google Drive

    backup_to_drive(db_file_path, drive_folder_path)
