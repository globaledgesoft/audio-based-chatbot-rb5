from tflite_runtime.interpreter import Interpreter
import numpy as np
import nltk
import random
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
nltk.download('words')
lemmatizer = WordNetLemmatizer()

class TFLiteBot:
    def __init__(self):
        self.classes = ['bye', 'food', 'greeting', 'search', 'temperature']
        self.tflite_model = Interpreter('model/my_model_new.tflite')
        self.tflite_model.allocate_tensors()
        self.input_details = self.tflite_model.get_input_details()
        self.output_details = self.tflite_model.get_output_details()
        self.input_shape = self.input_details[0]['shape']


    def encode(self, sentence, shape):
        vocab = words.words()
        encode_list = []
        encode_sentence = [0] * (shape[1])
        word_list = sentence.split()
        words_lem = [lemmatizer.lemmatize(w) for w in word_list]
        for i in range(len(vocab)):
            if vocab[i] in words_lem:
                encode_sentence[i] = 1
        encode_list.append(encode_sentence)
        return np.array(encode_list).astype("float32")

    def chat_reply(self, classes):
        greeting_resp = ['hey there', 'hi nice to see you', 'good to see you', 'hello']
        search_resp = ['Okay! I found him in there', 'I did not find her']
        bye_resp = ['goodbye', 'please take care', 'see you around', 'nice talking to you']
        food_resp = ['Your food is here', 'Going to the kitchen', 'Your food will be here in 5mins']
        temperature_resp = ['Temperature is 27 degrees centigrade', 'Its too cold', 'Its freezing', '12 degrees celsius']
        if classes == 'greeting':
            return random.choice(greeting_resp)
        elif classes == 'search':
            return random.choice(search_resp)
        elif classes == 'bye':
            return random.choice(bye_resp)
        elif classes == 'food':
            return random.choice(food_resp)
        elif classes == 'temperature':
            return random.choice(temperature_resp)
        print("\n")



    def infer(self, sentence):
        encode_sentence = self.encode(sentence, self.input_shape)
        input_data = encode_sentence.reshape(1,-1)
        self.tflite_model.set_tensor(self.input_details[0]['index'], input_data)
        self.tflite_model.invoke()
        output_data = self.tflite_model.get_tensor(self.output_details[0]['index'])
        resp = self.chat_reply(self.classes[np.argmax(output_data)])

        return resp
