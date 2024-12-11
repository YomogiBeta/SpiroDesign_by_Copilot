
TCL_VERSION=8.6.13
TK_VERSION=8.6.13

INSTALL_TCL-TK_DIR=$(HOME)/.local/tcl-tk/$(TCL_VERSION)

TCL_SRC_URL=http://jaist.dl.sourceforge.net/project/tcl/Tcl/$(TCL_VERSION)/tcl$(TCL_VERSION)-src.tar.gz
TK_SRC_URL=http://jaist.dl.sourceforge.net/project/tcl/Tcl/$(TK_VERSION)/tk$(TK_VERSION)-src.tar.gz

download-tcl-tk:
	curl -O $(TCL_SRC_URL)
	curl -O $(TK_SRC_URL)

unpack-tcl-tk:
	tar xzvf tcl$(TCL_VERSION)-src.tar.gz
	tar xzvf tk$(TK_VERSION)-src.tar.gz

build-mac-tcl:
	cd tcl$(TCL_VERSION)/unix && \
	./configure --enable-aqua --prefix=$(INSTALL_TCL-TK_DIR) && \
	make && \
	make install

build-mac-tk:
	cd tk$(TK_VERSION)/unix && \
	./configure --enable-aqua --prefix=$(INSTALL_TCL-TK_DIR) && \
	make && \
	make install

tcl-tk-clean:
	rm -rf tcl$(TCL_VERSION) tk$(TK_VERSION) tcl$(TCL_VERSION)-src.tar.gz tk$(TK_VERSION)-src.tar.gz

install-mac-tcl-tk:
	${MAKE} download-tcl-tk
	${MAKE} unpack-tcl-tk
	${MAKE} build-mac-tcl
	${MAKE} build-mac-tk
	${MAKE} tcl-tk-clean

setup-python-mac:
	env \
	PATH="$(INSTALL_TCL-TK_DIR)/bin:${PATH}" \
	LDFLAGS="-L$(INSTALL_TCL-TK_DIR)/lib" \
	CPPFLAGS="-I$(INSTALL_TCL-TK_DIR)/include" \
	PKG_CONFIG_PATH="$(INSTALL_TCL-TK_DIR)/lib/pkgconfig" \
	PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I$(INSTALL_TCL-TK_DIR)/include' --with-tcltk-libs='-L$(INSTALL_TCL-TK_DIR)/lib -ltcl8.6 -ltk8.6'" \
	pyenv install --skip-existing 3.10.11
	pip install -r requirements.txt

setup-python:
		pyenv install --skip-existing 3.10.11
		pip install -r requirements.txt

rady_javascript:
	python rady_mixed_file.py src/bridge_pyjs javascript

rady_python:
	python rady_mixed_file.py src/bridge_pyjs python

lint:
	flake8 --exclude pyjsdl,__target__ --ignore E116 --max-line-length 140

mac-build:
	${MAKE} rady_python
	python setup.py bdist_dmg

windows-build:
	${MAKE} rady_python
	python setup.py bdist_msi
	
run:
	${MAKE} rady_python
	python src/main.py

test:
	@echo "Test: Constants"
	env PYTHONPATH="${PYTHONPATH}:`pwd`/src" \
	python -m unittest discover -v -s src/Tests/
	@echo "Test: Model"
	env PYTHONPATH="${PYTHONPATH}:`pwd`/src" \
	python -m unittest discover -v -s src/Tests/Model
	@echo "Test: View"
	env PYTHONPATH="${PYTHONPATH}:`pwd`/src" \
	python -m unittest discover -v -s src/Tests/View
	@echo "Test: Controller"
	env PYTHONPATH="${PYTHONPATH}:`pwd`/src" \
	python -m unittest discover -v -s src/Tests/Controller


zstd_build:
	(cd zstd_wasm_builder && yarn install && npx webpack)
	- mv zstd_wasm_builder/dist/zstd_webpacked.js web_page/Javascript/lib/zstd_webpacked.js
	- mv zstd_wasm_builder/dist/*.wasm web_page/Javascript/lib/
	- rm -rf zstd_wasm_builder/dist

web-build-dev:
	${MAKE} rady_javascript
	$(MAKE) zstd_build
	- transcrypt -n -m -od ../web_page/__target__ src/main.py
	- ${MAKE} rady_python

web-build:
	${MAKE} rady_javascript
	$(MAKE) zstd_build
	- transcrypt -od ../web_page/__target__ src/main.py
	- ${MAKE} rady_python
	find web_page/__target__ -type f -exec sed -i '' '/\/\/# sourceMappingURL=/s/.*/''/' {} \; 2>	/dev/null

web-run:
	open http://localhost:8000/web_page & python -m http.server 8000

metrics:
	python metrics.py src cc Tests,pyjsdl > MetricsCyclomaticComplexity.txt
	python metrics.py src mi Tests,pyjsdl > MetricsMaintainabilityIndex.txt
	python metrics.py src raw Tests,pyjsdl > MetricsRaw.txt

clean-metrics:
	rm -rf MetricsCyclomaticComplexity.txt MetricsMaintainabilityIndex.txt MetricsRaw.txt

clean:
	rm -rf web_page/__target__	build dist MetricsCyclomaticComplexity.txt MetricsMaintainabilityIndex.txt MetricsRaw.txt