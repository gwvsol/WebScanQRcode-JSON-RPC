.PHONY: help install install-dev uninstall check clean run release

# ==========================================
VENV_NAME?=venv
VENV_BIN=${VENV_NAME}/bin
VENV_ACTIVATE=. ${VENV_NAME}/bin/activate
PYTHON=${VENV_NAME}/bin/python3
PIP=${VENV_NAME}/bin/pip3
PYCODESTYLE=${VENV_NAME}/bin/pycodestyle
PYFLAKES=${VENV_NAME}/bin/pyflakes
GUNICORN=${VENV_BIN}/gunicorn
DOCKER=$(shell which docker)
COMPOSE=$(shell which docker-compose)
ANSIBLE=$(shell which ansible-playbook)
export PWD=$(shell pwd)
export TIMEZONE=$(shell timedatectl status | awk '$$1 == "Time" && $$2 == "zone:" { print $$3 }')
export USER_ID=$(shell id -u `whoami`)
ENVIRONMENT=.env
ENVFILE=$(PWD)/${ENVIRONMENT}

ifneq ("$(wildcard $(ENVFILE))","")
    include ${ENVFILE}
    export ENVFILE=$(PWD)/${ENVIRONMENT}
endif

# ==========================================
.DEFAULT: help

help:
	@echo "make install	- Installing dependencies and applications"
	@echo "make install-dev - Installing dependencies for code validation"
	@echo "make uninstall	- Deleting an applications"
	@echo "make run	- Run the applications"
	@echo "make check	- Checking the code"
	@echo "make clean	- Cleaning up garbage"
	@echo "make release	- Creating a release"
	@exit 0

#=============================================
# Установка зависимостей для работы приложений
install:
	[ -d $(VENV_NAME) ] || python3 -m $(VENV_NAME) $(VENV_NAME)
	${PIP} install pip wheel -U

# Установка зависимостей для проверки кода
install-dev:
	[ -d $(VENV_NAME) ] || python3 -m $(VENV_NAME) $(VENV_NAME)
	${PIP} install pip wheel -U
	${PIP} install -r ${DEPENDENCESDEV}

# Активация виртуального окружения для работы приложений
venv: ${VENV_NAME}/bin/activate
$(VENV_NAME)/bin/activate: ${SETUP}
	[ -d $(VENV_NAME) ] || python3 -m $(VENV_NAME) $(VENV_NAME)
	${PIP} install pip wheel -U
#	${PIP} install -e .
	${VENV_ACTIVATE}

# Очистка мусора
clean:
	rm -fr build
	rm -fr .eggs
	rm -fr *.egg-info
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '__pycache__' -exec rm -fr {} +

# Удаление виртуального окружения
uninstall:
	make clean
	rm -fr ${VENV_NAME}

#===============================================
# Работа с UssmpPbx
ifneq ("$(wildcard $(PWD)/$(USSMPPBX_MAKEFILE))","")
    include ${USSMPPBX_MAKEFILE}
endif

#===============================================
# Проверка кода
check: ${PYCODESTYLE} ${PYFLAKES} ${USSMPPBX} ${SETUP}
	@echo "==================================="
	${PYCODESTYLE} ${USSMPPBX} ${SETUP_USSMPPBX}
	${PYFLAKES} ${USSMPPBX} ${SETUP_USSMPPBX}
	@echo "=============== OK! ==============="

#===============================================
# Создание релиза приложения
release: clean ${USSMPPBX}
	[ -d $(RELEASE) ] || mkdir ${RELEASE}
	[ -d $(ARCHIVE) ] || mkdir ${ARCHIVE}
	find "${RELEASE}" -name '*.zip' -type f -exec mv -v -t "${ARCHIVE}" {} +
	zip -r ${RELEASE}/${USSMPPBX}-$(shell date '+%Y-%m-%d-%H-%M-%S').zip \
	${USSMPPBX} ${MAKEFILE} ${README} ${ENVIRONMENT} ${DEPENDENCESDEV} \
	${COMPOSEFILE} ${HOSTS} ${PLAYBOOK} ${VARSFILES} ${CERTIFICATE}

#===============================================
# Сборка сервисов с использованием Docker Compose
build: ${DOCKER} ${COMPOSE} ${COMPOSEFILE} 
	make release
	${COMPOSE} -f ${COMPOSEFILE} build

# Старт сервисов с использованием Docker Compose
start: ${DOCKER} ${COMPOSE} ${COMPOSEFILE}
	${COMPOSE} -f ${COMPOSEFILE} up -d

# Остановка сервисов с использованием Docker Compose
stop: ${DOCKER} ${COMPOSE} ${COMPOSEFILE}
	${COMPOSE} -f ${COMPOSEFILE} down

# Логирование сервисов с использованием Docker Compose
log: ${DOCKER} ${COMPOSE} ${COMPOSEFILE}
	${COMPOSE} -f ${COMPOSEFILE} logs --follow --tail 500

# Рестарт сервисов с использованием Docker Compose
restart: ${DOCKER} ${COMPOSE} ${COMPOSEFILE}
	make stop
	sleep 3
	make start

# Удаление сервисов (для удаления Docker Compose не используется)
remove: ${DOCKER} ${COMPOSE} ${COMPOSEFILE}
	make stop
	make remove-ussmppbx

#===============================================
# ansible-playbook -i hosts.yml playbook.yml -t start

# Подготовка к установке приложения используя Ansible
prepare-host: ${HOSTS} ${ANSIBLE}
	${ANSIBLE} -i ${HOSTS} ${PLAYBOOK} -t prepare

# Устанавливаем приложение используя Ansible
install-host: ${HOSTS} ${ANSIBLE}
	make release
	${ANSIBLE} -i ${HOSTS} ${PLAYBOOK} -t install

# Запускаем приложение используя Ansible
start-host: ${HOSTS} ${ANSIBLE}
	${ANSIBLE} -i ${HOSTS} ${PLAYBOOK} -t start

# Останавливаем приложение используя Ansible
stop-host: ${HOSTS} ${ANSIBLE}
	${ANSIBLE} -i ${HOSTS} ${PLAYBOOK} -t stop

# Рестарт приложения используя Ansible
restart-host: ${HOSTS} ${ANSIBLE}
	${ANSIBLE} -i ${HOSTS} ${PLAYBOOK} -t restart

# Удаление приложения используя Ansible
remove-host: ${HOSTS} ${ANSIBLE}
	${ANSIBLE} -i ${HOSTS} ${PLAYBOOK} -t remove

#===============================================