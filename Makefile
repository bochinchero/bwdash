run_app:
	python3 dashApp.py & sleep 30

	wget -r http://127.0.0.1:8050/
	wget -r http://127.0.0.1:8050/_dash-layout
	wget -r http://127.0.0.1:8050/_dash-dependencies

	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dcc/async-graph.js
	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dcc/async-highlight.js
	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dcc/async-markdown.js
	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dcc/async-datepicker.js

	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dash_table/async-table.js
	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dash_table/async-highlight.js

	wget -r http://127.0.0.1:8050/_dash-component-suites/plotly/package_data/plotly.min.js

	mv 127.0.0.1:8050 pages_files
	ls -a pages_files

	find pages_files -exec sed -i.bak 's|_dash-component-suites|bwdash\\/_dash-component-suites|g' {} \;
	find pages_files -exec sed -i.bak 's|_dash-layout|bwdash/_dash-layout.json|g' {} \;
	find pages_files -exec sed -i.bak 's|_dash-dependencies|bwdash/_dash-dependencies.json|g' {} \;
	find pages_files -exec sed -i.bak 's|_reload-hash|bwdash/_reload-hash|g' {} \;
	find pages_files -exec sed -i.bak 's|_dash-update-component|bwdash/_dash-update-component|g' {} \;

	mv pages_files/_dash-layout pages_files/_dash-layout.json
	mv pages_files/_dash-dependencies pages_files/_dash-dependencies.json

	pkill -f dashApp.py

clean_dirs:
	ls
	rm -rf 127.0.0.1:8050/
	rm -rf pages_files/
	rm -rf joblib