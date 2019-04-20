from TaskProcessor.ProcessorInterface import Processor


class Forwarder:
    def __init__(self):
        self.processors = []

    def add_processor(self, processor: Processor):
        self.processors.append(processor)

    def forward(self):
        raise NotImplementedError

