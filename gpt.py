import g4f


class Gpt:
    def __init__(self):
        self.model = "llama2-7b"
        self.error_message = 'GPT is unable to give a proper reply :( Please try again.'
        self.message_storage = []
        self.allowed_attempts_to_prompt = 5

    def create_a_message(self, prompt, role='user'):
        self.message_storage.append({"role": f"{role}", "content": f"{prompt}"})
        print(self.message_storage)

    def ask_gpt(self, prompt):
        self.create_a_message(prompt)
        return self.run_gpt()

    def run_gpt(self):
        current_attempt = 0
        while self.allowed_attempts_to_prompt > current_attempt:
            try:
                response = g4f.ChatCompletion.create(model=self.model, messages=self.message_storage)
                if len(response) == 0:
                    current_attempt += 1
                    continue
                self.create_a_message(prompt=response, role='assistant')
                return response
            except Exception as error:
                print(error)
                current_attempt += 1
        return self.error_message

    def __call__(self, prompt):
        return self.ask_gpt(prompt)


def main():
    test = Gpt()
    print(test.ask_gpt('Hello!'))
    print(test('what are you?'))


if __name__ == "__main__":
    main()
