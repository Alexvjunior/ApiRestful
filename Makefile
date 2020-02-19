version ?= latest
NAMEIMAGE=app

guard-%:
	@ if [ "${${*}}" = "" ]; then \
                echo "Variable '$*' not set"; \
                exit 1; \
        fi

image:
	docker build -t $(NAMEIMAGE) .

check: image
	docker run $(NAMEIMAGE)

