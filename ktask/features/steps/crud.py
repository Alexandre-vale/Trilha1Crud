from behave import when, then

from ktask.tests.unit.test_handler import SAMPLE_EVENT


@when("The '{method}' event was triggered")
def _(self, method: str):
    if method == "GET":
        self.event_sample = SAMPLE_EVENT
    # self.event_sample = apigw_post_event()


@then("the event httpMethod should be equal to '{method}'")
def _(self, method: str):
    assert self.event_sample["httpMethod"] == "GET"
