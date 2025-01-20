# File Encryption and Brute Force Demo

## Opis Projektu
Aplikacja demonstruje:
1. Zastosowanie szyfrowania plików przy użyciu AES (CBC).
2. Brute force na plik ZIP oraz zabezpieczenia przed tego typu atakiem.

## Jak Uruchomić Projekt
1. Zainstaluj wymagane zależności:
```bash
pip install flask pycryptodome
```
2. Uruchom aplikację:
```bash
python file_encryption.py
```
3. API będzie dostępne pod `http://127.0.0.1:5000`.

## Endpointy

### 1. Szyfrowanie pliku
- **POST** `/encrypt`
  - Parametry wejściowe (JSON):
    ```json
    {
      "file_path": "ścieżka_do_pliku",
      "output_path": "ścieżka_zaszyfrowanego_pliku",
      "key": "16-bajtowy_klucz"
    }
    ```
  - Zwracane dane:
    ```json
    {
      "message": "File encrypted and saved to ..."
    }
    ```

### 2. Deszyfrowanie pliku
- **POST** `/decrypt`
  - Parametry wejściowe (JSON):
    ```json
    {
      "file_path": "ścieżka_do_zaszyfrowanego_pliku",
      "output_path": "ścieżka_odkodowanego_pliku",
      "key": "16-bajtowy_klucz"
    }
    ```
  - Zwracane dane:
    ```json
    {
      "message": "File decrypted and saved to ..."
    }
    ```

### 3. Brute Force na ZIP
- **POST** `/bruteforce`
  - Parametry wejściowe (JSON):
    ```json
    {
      "zip_file": "ścieżka_do_pliku_zip",
      "max_length": 4
    }
    ```
  - Zwracane dane:
    ```json
    {
      "password": "odkryte_hasło"
    }
    ```

## Problemy i ich Rozwiązania
1. Problem z szyfrowaniem dużych plików - rozwiąż przez dzielenie plików na bloki.
2. Długi czas brute force przy dużych zakresach - zastosuj ograniczenia długości haseł.