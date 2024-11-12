run_app:
	python3 dashApp.py & sleep 30

	wget -rkpN -e robots=off http://127.0.0.1:8050

	mv 127.0.0.1:8050 pages_files
	ls -a pages_files

	mv pages_files/_dash-layout pages_files/_dash-layout.json
	mv pages_files/_dash-dependencies pages_files/_dash-dependencies.json

	ps -C python -o pid= | xargs kill -9

clean_dirs:
	ls
	rm -rf 127.0.0.1:8050/
	rm -rf pages_files/
	rm -rf joblib