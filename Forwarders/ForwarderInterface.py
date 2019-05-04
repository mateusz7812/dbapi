from Processors.ProcessorInterface import Processor


class Forwarder:
    def __init__(self, response_generator):
        self.response_generator = response_generator()
        self.processors = []

    def add_processor(self, processor):
        self.processors.append(processor)

    def forward(self, response):
        raise NotImplementedError

