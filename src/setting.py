import json

class settings():
    def load_settings(self, file_path):
        with open(file_path, 'r') as file:
            settings = json.load(file)
        return settings
    def __init__(self):
        settings_file = 'src/settings.json'
        settings = self.load_settings(settings_file)
        
        self.logger_chat = settings['logger_chat']
        self.special_chat = settings['special_chat']
        self.token = settings['token']
        self.toxicity_threshold = settings['toxicity_threshold']





if __name__ == "__main__":
    my_settings = settings()
    
    print(f"Logger Chat ID: {my_settings.logger_chat}")
    print(f"Special Chat ID: {my_settings.special_chat}")
    print(f"Token: {my_settings.token}")
    print(f"Toxicity Threshold: {my_settings.toxicity_threshold}")
