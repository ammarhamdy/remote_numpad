from tkinter import Label
from values.dimen import typing_delay_time
from time import sleep
from threading import Thread


class Typewriter:

    def __init__(self, sentence):
        self.sentence = sentence

    def _typing_sentence(self, label: Label):
        """
        typing sentence character by character waiting between each character typing
        applying taken color to text then clear text
        """
        sleep(typing_delay_time * 2)
        for char in self.sentence:
            label["text"] = label["text"] + char
            sleep(typing_delay_time)
        sleep(typing_delay_time * 2)

    @staticmethod
    def get_required_typing_millis(sentence):
        return len(sentence) * typing_delay_time + typing_delay_time * 5

    def start_typing(self, label: Label):
        Thread(
            target=self._typing_sentence,
            args=(label,),
            daemon=True
        ).start()




