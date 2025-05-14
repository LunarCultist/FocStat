install:
	sudo install -m 755 main.py /usr/local/bin/focal-ui
	sudo install -m 644 app_icon.png /usr/share/pixmaps/focal-ui.png
	sudo desktop-file-install focal.desktop

