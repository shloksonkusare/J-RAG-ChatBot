from src.translation.translator import Translator

translator = Translator(direction="ja-en")
result = translator.translate(["私は学生です。"])
print(result[0])
