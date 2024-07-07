from typing import Literal
from pathlib import Path
from maniple.llm.LLMConnection import LLMConnection
import json

class ManipleDataAdaptor(LLMConnection):
    def __init__(self, data_dir: str, dataset: Literal['BGP314', 'BGP32']):
        super().__init__(
            platform='Ollama',
            model='llama3:8b',
            api_key=None,
            endpoint_url=None,
            trial=1,
            max_concurrent_requests=4,
            max_generation_count=3,
            log_file='llm_connection.log'
        )

        template_file = Path(data_dir) / 'prompt_template.json'
        self.__template = json.loads(template_file.read_text())

        bitvectors_file = Path(data_dir) / 'stratas.json'
        self.__bitvectors = json.loads(bitvectors_file.read_text())

    def __get_bug_data(self, bug_id: str) -> str:
        pass
    
    def process_response(self, response: str) -> str | None:
        return response


if __name__ == "__main__":
    connection = ManipleDataAdaptor()
    connection.chat('test_bugid')
    connection.close()
