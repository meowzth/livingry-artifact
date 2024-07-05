PACKAGE_NAME=pizdec
LOCAL_PACKAGE_PATH=.
REMOTE_PACKAGE_PATH=/pizdec-lib
REMOTE_HOST=otlab@192.168.1.70

.PHONY: deploy

deploy:
	@ssh $(REMOTE_HOST) "sudo rm -rf $(REMOTE_PACKAGE_PATH)"
	@ssh $(REMOTE_HOST) "sudo mkdir $(REMOTE_PACKAGE_PATH)"
	@ssh $(REMOTE_HOST) "sudo chown otlab $(REMOTE_PACKAGE_PATH)"
	@tar cvfz $(PACKAGE_NAME).tar.gz -C $(LOCAL_PACKAGE_PATH) $(PACKAGE_NAME)
	@scp $(PACKAGE_NAME).tar.gz $(REMOTE_HOST):$(REMOTE_PACKAGE_PATH)
	@ssh $(REMOTE_HOST) "tar xvfz $(REMOTE_PACKAGE_PATH)/$(PACKAGE_NAME).tar.gz -C $(REMOTE_PACKAGE_PATH)"
	@ssh $(REMOTE_HOST) "pip install $(REMOTE_PACKAGE_PATH)/$(PACKAGE_NAME) --break-system-packages"