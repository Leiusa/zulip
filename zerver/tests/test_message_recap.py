from zerver.lib.test_classes import ZulipTestCase

class MessageRecapTests(ZulipTestCase):
    def test_message_recap_requires_login(self) -> None:
        result = self.client_post("/json/ai/message_recap", {"message_ids": []})
        self.assertEqual(result.status_code, 401)

    # Add tests for validation, response shape, mocked LLM here