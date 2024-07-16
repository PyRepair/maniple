from abc import abstractmethod
from dataclasses import dataclass
from typing import Literal, Optional, List, Tuple
from maniple.utils.misc import print_in_red
import json, hashlib, datetime
import concurrent.futures

PlatformType = Literal["OpenAI", "DeepInfra", "Ollama"]
ModelType = Literal["llama3:8b", "llama:70b", "gpt-3.5-turbo-0125", "meta-llama/Meta-Llama-3-8B-Instruct"]

class LLMResponse:
    original_response = ''
    fix_patch = ''



class LLMConnection:
    def __init__(self, 
                 platform: PlatformType,
                 model: ModelType,
                 api_key: str = None,
                 endpoint_url: str = None,
                 trial = 1,
                 temperature = 1.0,
                 seed = 42,
                 max_concurrent_requests = 4,
                 max_generation_count = 3,
                 log_file = 'llm_connection.log'):
        
        if platform == "OpenAI":
            from openai import OpenAI
            self.__client = OpenAI(api_key=api_key)
            self.__client.chat.completions.create()
        elif platform == "DeepInfra":
            from openai import OpenAI
            self.__client = OpenAI(base_url=endpoint_url, api_key=api_key)
        elif platform == "Ollama":
            import ollama
            self.__client = ollama
        else:
            raise ValueError(f"Invalid platform: {platform}")
        
        self.__platform: PlatformType = platform

        self.__model: ModelType = model
        self.__trial = trial
        self.__temperature = temperature
        self.__seed = seed
        self.__max_generation_count = max_generation_count
        
        self.__thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent_requests)
        self.__log_file = open(log_file, 'a')

    def __chat__ollama(self, prompt: str, label: str) -> Tuple[str, str]:
        request = {
            'model': self.__model,
            'messages': [{'role': 'user', 'content': prompt}],
            'options': {
                'seed': self.__seed,
                'temperature': self.__temperature,
            }
        }

        message = ''
        for i in range(self.__max_generation_count):
            try:
                response = self.__client.chat(
                    model=request['model'], 
                    messages=request['messages'],
                    options=request['options']
                )
                message = response['message']['content']
                self.__log(request, response, f"{label},trial={i+1}")

            except Exception as e:
                print_in_red('error: ', e)
                self.__log(request, dict(), f"{label},trial={i+1},exception={e}")
                continue
                # if isinstance(e, openai.RateLimitError):
                #     print(f"Rate Limit Exceeded. Waiting for 10 seconds...")
                #     time.sleep(10)

            result = self.process_response(message) 
            if result is not None:
                return (message, result)
            
        return (message, '')
    
    def __chat__openai(self, prompt: str):
        return None
    
    def __chat_huggingface(self, prompt: str, label: str) -> Tuple[str, str]:
        request = {
            'model': self.__model,
            'messages': [{'role': 'user', 'content': prompt}],
            'options': {
                'seed': self.__seed,
                'temperature': self.__temperature,
            }
        }

        message = ''
        for i in range(self.__max_generation_count):
            try:
                chat_completion = self.__client.chat.completions.create(
                    model=request['model'],
                    messages=request['messages'],
                    seed=request['options']['seed'],
                    temperature=request['options']['temperature'],
                    stream=False
                )

                response = chat_completion.to_dict()
                message = chat_completion.choices[0].message.content
                self.__log(request, response, f"{label},trial={i+1}")
            
            except Exception as e:
                print_in_red('error: ', e)
                self.__log(request, dict(), f"{label},trial={i+1},exception={e}")

            result = self.process_response(message) 
            if result is not None:
                return (message, result)
            
        return (message, '')
    
    @abstractmethod
    def process_response(self, response: str) -> Optional[str]:
        pass
    
    def chat(self, prompt: str, label='') -> List[str]:
        results = []
        futures = []

        if self.__platform == 'Ollama':
            task_func = self.__chat__ollama
        elif self.__platform == 'OpenAI':
            task_func = self.__chat__openai
        else:
            task_func = self.__chat_huggingface

        for _ in range(self.__trial):
            future = self.__thread_pool.submit(task_func, prompt, label)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f'API Request Exception: {exc}')

        return results
    
    def __log(self, request: dict, response: dict, label = ''):
        record = dict()
        record['label'] = label
        record['timestamp'] = str(datetime.datetime.now())
        record['request'] = request
        record['response'] = response

        record_dump = json.dumps(record)
        record_hash = hashlib.md5(record_dump.encode("utf-8")).hexdigest()

        log_record = f"{record_dump}#{record_hash}\n"
        self.__log_file.write(log_record)

    def close(self):
        self.__log_file.close()
