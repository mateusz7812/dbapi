from BranchInterfaces import BaseBranch
from Branchs import TaskHandler


class BranchHandlerTest:
    def __init__(self, branchs: []):
        self.branchHandler = TaskHandler(branchs)

    def test_process(self, data):
        result = self.branchHandler.process_request(data)
        return result


class test_base_branch(BranchHandlerTest):
    class TestBranch(BaseBranch):
        name = "test"

        def process_request(self, task):
            return task

    def __init__(self, data):
        super().__init__([self.TestBranch])
        result = self.test_process(["test", data])
        assert result == data


def run_test():
    test_base_branch("some data")

if __name__ == "__main__":
    run_test()
