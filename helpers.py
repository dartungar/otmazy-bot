

def with_words(func):
    def template_context_wrapper():
        func()
    return template_context_wrapper

