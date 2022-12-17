from subprocess import Popen, PIPE
from sentistrength_adapter.wrapper.sentiment import Sentiment

KILL_TIMEOUT = 0.5

JAR_PATH = "./jars/SentiStrength.jar"
SENTIDATA_PATH = './data/'

BINARY = "binary"
TRINARY = "trinary"
SCALE = "scale"


class SentistrengthWrapper():
    """Wrapper class for the Sentistrength JAR."""

    def __init__(self, sentidata_path: str = SENTIDATA_PATH,
                 classification: str = TRINARY, jar_path: str = JAR_PATH):
        self.__sentidata_path = sentidata_path
        self.__classification = classification
        self.__jar_path = jar_path
        self.__proc = None

    def __enter__(self) -> 'SentistrengthWrapper':
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()

    def connect(self):
        """Connects with Sentistrength JVM."""
        args = ['java', '-jar', self.__jar_path, 'cmd',
                self.__classification, 'sentidata', self.__sentidata_path]
        self.__proc = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)

    def disconnect(self):
        """Disconnects from Sentistrength JVM."""
        if self.__proc.poll() is None:
            self.__proc.terminate()
            try:
                self.__proc.wait(KILL_TIMEOUT)
            except:
                self.__proc.kill()
            self.__proc = None

    def get_sentiment(self, text: str) -> 'Sentiment':
        """Communicates with Sentistrength to evaluate the 
        sentiment of the provided sentence."""
        if self.__proc is None:
            raise Exception(
                "Not connected to Sentistrength instance. Have you called 'connect()'?")
        cleaned_text = self.__clean_text(text)
        result = self.__communicate(cleaned_text)
        sentiment = self.__build_sentiment(cleaned_text, result)
        return sentiment

    def __clean_text(self, text: str) -> str:
        """Cleans the text in preparation for communication."""
        cleaned_text = text.replace("\r", ' ').replace("\n", ' ')
        return cleaned_text

    def __communicate(self, text: str) -> str:
        """Inputs text into Sentistrength and outputs the result."""
        encoded = f'{text}\n'.encode("utf-8")
        self.__proc.stdin.write(encoded)
        self.__proc.stdin.flush()
        result = self.__proc.stdout.readline().decode("utf-8")
        return result

    def __build_sentiment(self, text: str, result: str) -> Sentiment:
        """Factory method for building sentiment objects."""
        (positivity, negativity, classification) = [
            int(e) for e in result.strip().split(" ")]
        return Sentiment(text, positivity, negativity, classification)
