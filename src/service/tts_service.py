from boto3 import Session
from contextlib import closing
import os
import sys
from tempfile import gettempdir
from typing import Any


class TTSService:
    session: Session
    polly: Any

    def __init__(self):
        self.session = Session(profile_name='walefy')
        self.polly = self.session.client('polly')
    
    def generate_audio(self, text: str, title: str):
        response = self.polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Thiago', Engine='neural')

        if 'AudioStream' in response:
            with closing(response['AudioStream']) as stream:
                directory = gettempdir()
                output = os.path.join(directory, f'{title}.mp3')

                try:
                    with open(output, 'wb') as file:
                        file.write(stream.read())
                except IOError as error:
                    print(error)
                    sys.exit(-1)

        return os.path.join(directory, f'{title}.mp3')
