UNAME_S := $(shell uname -s)
ifneq ($(UNAME_S),Darwin)
# Any OS branch
nproc=$(shell nproc | awk '{if($$1>8){print 8}else{print $$1}}')
else
# Darwin branch
nproc := $(shell sysctl -n hw.physicalcpu)
endif

DOCKER_IMAGE ?= "azshoo/alaska"

pull:
	-docker pull $(DOCKER_IMAGE)

kill:
#	-docker kill $(docker ps -q --filter ancestor=$(DOCKER_IMAGE))
	$(eval $@_CID := $(shell docker ps -q --filter ancestor=$(DOCKER_IMAGE)))
	-docker kill $($@_CID)

rm:
	$(eval $@_CID := $(shell docker ps -aqf ancestor=$(DOCKER_IMAGE)))
	@echo $($@_CID)
	-docker rm $($@_CID)

docker-run: kill rm pull
	docker run -t -i --rm \
	-p 8080:8091 $(DOCKER_IMAGE)

run-tests:
	pytest -s --alluredir=$(CURDIR)/report

run-tests-info:
	pytest -s -m "info" --alluredir=$(CURDIR)/report

run-tests-create:
	pytest -s -m "create" --alluredir=$(CURDIR)/report

run-tests-delete:
	pytest -s -m "create" --alluredir=$(CURDIR)/delete

clean:
	rm -rf $(CURDIR)/report/*.json
	rm -rf $(CURDIR)/report/*.txt

.PHONY: pull kill rm docker-run run-tests run-tests-info run-tests-create run-tests-delete clean