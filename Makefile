.PHONY: help install uninstall clean run release

# ==========================================
VENV_NAME?=venv
VENV_BIN=${VENV_NAME}/bin
VENV_ACTIVATE=. ${VENV_NAME}/bin/activate
PYTHON=${VENV_NAME}/bin/python3
PIP=${VENV_NAME}/bin/pip3
GUNICORN=${VENV_BIN}/gunicorn
export PWD=$(shell pwd)
ENVIRONMENT=.env
ENVFILE=$(PWD)/${ENVIRONMENT}

export WEBSCAN_REQUEST=$(PWD)/${WEBSCAN_REQUEST}

ifneq ("$(wildcard $(ENVFILE))","")
    include ${ENVFILE}
    export ENVFILE=$(PWD)/${ENVIRONMENT}
endif

# ==========================================
.DEFAULT: help

help:
	@echo "make install	- Installing dependencies and applications"
	@echo "make uninstall	- Deleting an applications"
	@echo "make run	- Run the applications"
	@echo "make release	- Creating a release"
	@exit 0

#=============================================
# Установка зависимостей для работы приложений
install:
	[ -d $(VENV_NAME) ] || python3 -m $(VENV_NAME) $(VENV_NAME)
	${PIP} install pip wheel -U

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
ifneq ("$(wildcard $(PWD)/$(WEBSCAN_MAKEFILE))","")
    include ${WEBSCAN_MAKEFILE}
endif

#===============================================
# Создание релиза приложения
release: clean ${WEBSCAN}
	[ -d $(RELEASE) ] || mkdir ${RELEASE}
	[ -d $(ARCHIVE) ] || mkdir ${ARCHIVE}
	find "${RELEASE}" -name '*.zip' -type f -exec mv -v -t "${ARCHIVE}" {} +
	zip -r ${RELEASE}/${WEBSCAN}-$(shell date '+%Y-%m-%d-%H-%M-%S').zip \
	${WEBSCAN} ${MAKEFILE} ${README} ${ENVIRONMENT}

#===============================================

ping: ${WEBSCAN_REQUEST} 
	${WEBSCAN_REQUEST} ping

info: ${WEBSCAN_REQUEST} 
	${WEBSCAN_REQUEST} help

enable: ${WEBSCAN_REQUEST}
	${WEBSCAN_REQUEST} enable

disable: ${WEBSCAN_REQUEST}
	${WEBSCAN_REQUEST} disable

scan: ${WEBSCAN_REQUEST}
	${WEBSCAN_REQUEST} getscan

#===============================================