ifeq ($(OS),Windows_NT)
    DELETE := cmd /C rd /s /q
else
    DELETE := rm -rf
endif

NAME := YA-ADB-Fastboot-GUI.exe

clean:
	@$(DELETE) dist build
	@$(DELETE) *.spec
	@$(DELETE) *.exe

program:
	@cd src && pyinstaller --onefile --windowed main.py --name="YA-ADB-Fastboot-GUI.exe" --clean
	@$(DELETE) *.spec
	@echo "File saved in src/dist/$(NAME)"

libraries:
	@python -m pip install pipreqs pyinstaller --break-system-packages
	@pipreqs . --force
	@python -m pip install -r requirements.txt --break-system-packages