#=============================================
# Определение переменных для установки и запуска UssmpPbx
SETUP=${SETUP_WEBSCAN}
install-webscan: ${DEPENDENCES_WEBSCAN} install
	${PIP} install pip wheel -U
	${PIP} install --editable ${WEBSCAN}

# Запуск приложения UssmpPbx
run-webscan: ${SETUP_WEBSCAN} venv
	${GUNICORN} --chdir ${WEBSCAN} \
		"${WEBSCAN}.__main__:${WEBSCAN_WEBAPP}()" \
		--bind ${WEBSCAN_HOST}:${WEBSCAN_PORT} \
		--log-level ${WEBSCAN_DEBUG} \
		--workers ${WEBSCAN_WORKERS} \
		--name ${WEBSCAN} \
		--reload

#=============================================
