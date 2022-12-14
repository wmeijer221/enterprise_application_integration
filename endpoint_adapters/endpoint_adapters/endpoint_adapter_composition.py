from os import getenv

import logging

from endpoint_adapters.title_publisher import TitlePublisher
from endpoint_adapters.adapters import APIAdapter
from endpoint_adapters.utils.import_helper import get_instance_of_type_from

ENDPOINT_TYPE_KEY = "ENDPOINT_TYPE"


class EndpointAdapterComposition:
    def __init__(self):
        self.adapter = self.__build_api_adapter()
        self.title_publisher = TitlePublisher(self.adapter)
        self.title_publisher.start()

    def publish(self, message):
        # TODO: publish message to channel (https://trello.com/c/hD3RPjNq/17-implement-generic-api-adapter-behaviour).
        logging.info("Sending message: %s", message)

    def __build_api_adapter(self) -> APIAdapter:
        """
        Factory method that loads an API adapter based
        on the set environment variable.
        """
        endpoint_type = getenv(ENDPOINT_TYPE_KEY).lower()
        logging.info(f"Starting API Adapter of type: {endpoint_type}.")
        module_path = f"endpoint_adapters.adapters.{endpoint_type}_adapter"
        try:
            adapter = get_instance_of_type_from(
                module_type=APIAdapter, module_path=module_path, publish=self.publish
            )
        except Exception:
            logging.critical(f"Failed to start API adapter of type: {endpoint_type}.")
            raise
        return adapter
