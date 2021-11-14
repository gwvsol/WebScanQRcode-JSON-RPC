#=============================================
# Определение переменных для установки и запуска UssmpPbx
SETUP=${SETUP_USSMPPBX}
install-ussmppbx: ${DEPENDENCES_USSMPPBX} install
	${PIP} install pip wheel -U
	${PIP} install --editable ${USSMPPBX}

# Запуск приложения UssmpPbx
run-ussmppbx: ${SETUP_USSMPPBX} venv
	${GUNICORN} --chdir ${USSMPPBX} \
		"${USSMPPBX}.__main__:${USSMPPBX_WEBAPP}()" \
		--bind ${USSMPPBX_HOST}:${USSMPPBX_PORT} \
		--worker-class ${USSMPPBX_WORKER_CLASS} \
		--log-level ${USSMPPBX_DEBUG} \
		--workers ${USSMPPBX_WORKERS} \
		--name ${USSMPPBX} \
		--reload

# Сборка UssmpPbx в Docker, используется для отладки
build-ussmppbx: ${DOCKER} ${DOCKERFILE_USSMPPBX}
	make release
	${DOCKER} build \
	--file ${DOCKERFILE_USSMPPBX} \
	--build-arg TIMEZONE=${TIMEZONE} \
	--build-arg USER_ID=${USER_ID} \
	--build-arg GROUP_ID=${USER_ID} \
	--tag ${USSMPPBX}:${RELEASE_IMAGE} ./

# Cтарт UssmpPbx в Docker, используется для отладки
start-ussmppbx: ${DOCKER} ${DOCKERFILE_USSMPPBX}
	${DOCKER} run \
	--name ${USSMPPBX} \
	--rm \
	--volume ${ENVFILE}:/usr/src/.env \
	--publish ${API_PORT}:${USSMPPBX_PORT} \
	--detach ${USSMPPBX}:${RELEASE_IMAGE}
# 	--restart=always

# Стоп UssmpPbx в Docker, используется для отладки
stop-ussmppbx: ${DOCKER} ${DOCKERFILE_USSMPPBX}
	! [ `${DOCKER} ps | grep ${USSMPPBX} | wc -l` -eq 1 ] || \
	${DOCKER} stop ${USSMPPBX}

# Удаление UssmpPbx в Docker, используется для отладки
remove-ussmppbx: ${DOCKER} ${DOCKERFILE_USSMPPBX}
	make stop-ussmppbx
	${DOCKER} rmi ${USSMPPBX}:${RELEASE_IMAGE}

# Логирование UssmpPbx в Docker, лог выводится в файл, который читается
log-ussmppbx: ${DOCKER} ${COMPOSE} ${COMPOSE_FILE} ${DOCKERFILE_USSMPPBX} 
	! [ `${DOCKER} ps | grep ${USSMPPBX} | wc -l` -eq 1 ] || \
		${DOCKER} logs --follow --tail 500 ${USSMPPBX}
#		${COMPOSE} -f ${COMPOSE_FILE} logs --follow --tail 500 ${USSMPPBX}

#=============================================
