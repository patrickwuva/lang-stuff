from dataclasses import dataclass

@dataclass
class Word:
    word: str
    size: int
    

    @classmethod
    def from_string(cls, word:str):
        return cls(word=word, size=len(word))
    
    def get_chars(self):
        return list(self.word)
    
