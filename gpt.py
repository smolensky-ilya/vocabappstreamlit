import g4f


class Gpt:
    def __init__(self):
        self.model = "llama2-7b"
        self.error_message = 'GPT is unable to give a proper reply :( Please try again.'
        self.message_storage = []
        self.allowed_attempts_to_prompt = 5

    def create_a_message(self, prompt, role='user'):
        self.message_storage.append({"role": f"{role}", "content": f"{prompt}"})

    def ask_gpt(self, prompt, history=True):
        if history:
            self.create_a_message(prompt)
            return self.run_gpt()
        else:
            return self.run_gpt(prompt)

    def run_gpt(self, prompt=None):
        current_attempt = 0
        while self.allowed_attempts_to_prompt > current_attempt:
            try:
                response = g4f.ChatCompletion.create(model=self.model, messages=self.message_storage if
                                                     prompt is None else [{"role": "user", "content": f"{prompt}"}])
                if len(response) == 0:
                    current_attempt += 1
                    continue
                self.create_a_message(prompt=response, role='assistant')
                return response
            except Exception as error:
                print(error)
                current_attempt += 1
        return self.error_message


def main():
    pass


if __name__ == "__main__":
    main()
