import curse_word_filter
import toxicity

class conclusion():
    def __init__(self, message, setting):
        self.toxicity_level = toxicity.get_toxicity_probability(message.text)
        self.toxicity_level_check = False

        if self.toxicity_level>=setting.toxicity_threshold:
            self.toxicity_level_check = True 
        
        self.profanity_check = curse_word_filter.check_profanity(message.text)

        self.warning = self.profanity_check or self.toxicity_level_check
    
    def __str__(self):
        toxicity_level_check_text = "Нет"

        if self.toxicity_level_check:
            toxicity_level_check_text = "Да"  
        
        profanity = "Нет"
        if self.profanity_check:
            profanity = "Да"  
        return "Наличие мата: " + profanity +"\nНаличие грубости: " + \
            toxicity_level_check_text +"\nТоксичность: " + str(round(self.toxicity_level*100, 2)) + "%"

