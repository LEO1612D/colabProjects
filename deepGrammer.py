from deepgram import Deepgram
import asyncio
import language_tool_python
import json

# Basic Setup
## Put your api key here
DEEPGRAM_API_KEY = 'YOUR_API_KEY'

# Example URL
## Put any audio url
FILE = 'https://static.deepgram.com/examples/interview_speech-analytics.wav'


async def main():
    # Initialize the Deepgram SDK
    deepgram = Deepgram(DEEPGRAM_API_KEY)

    # Check whether requested file is local or remote, and prepare source
    if FILE.startswith('http'):
        # file is remote
        # Set the source
        source = {
        'url': FILE
        }
    else:
        # file is local
        # Open the audio file
        audio = open(FILE, 'rb')

        # Set the source
        source = {
        'buffer': audio,
        'mimetype': MIMETYPE
        }

    # Send the audio to Deepgram and get the response
    response = await asyncio.create_task(
        deepgram.transcription.prerecorded(
        source,
        {
            'punctuate': True
        }
        )
    )

    # Write the response to the console
    # print(json.dumps(response, indent=4))
    # Write only the transcript to the console
    return response["results"]["channels"][0]["alternatives"][0]["transcript"]

def checkGrammer(data):

    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(data)
    corrected = language_tool_python.utils.correct(data, matches)
    tool.close()
    formatAndPrint(data,matches,corrected)


def formatAndPrint(data='',matches=[],corrected=''):
    print('***'*30)
    print('Original Text')
    print('***'*30)
    print(data)


    print('***'*30)
    print('Grammer mistakes & Improvements')
    print('***'*30)
    for match in matches:
        incorrect_text = match.sentence.replace(match.matchedText, '\033[44;33m{}\033[m'.format(match.matchedText))
        rule_text = '\033[3;31;40m{}\033[m'.format(match.message)
        suggestion = '\033[4;32;40m{}\033[m'.format(match.replacements[0])
        print(f"{rule_text} => {incorrect_text}")
        print(f"Suggestion : {suggestion}")

    # Corrected ----------
    print('***'*30)
    print('CORRECTED TEXT')
    print('***'*30)
    print('\033[3;33;40m{}\033[m'.format(corrected))
    print('---'*30)


try:
  # If running in a Jupyter notebook, Jupyter is already running an event loop, so run main with this line instead:
  #await main()

  # For Testing with valid DeepGram API key
  result = asyncio.run(main())

  # For Testing without deepgram uncomment this -------
  # result = "another big problem in the speech analytics space. When customers first bring the software on, is that they they are blown away by the fact that an engine can monitor hundreds of Kpis. Right? Everything from my new compliance issues to, you know, human human interaction, empathy measurements to upsell aptitude to closing aptitude. They're hundreds literally of Kpis that one could look at. And the speech analytics companies have typically gone to the customer and really bang that trump. We'll get all of these things that we're gonna help you keep an eye on. The reality, however, is that a company even a contact center manager, they can't keep track in their brain even if they have a report in front of. Of that many Kpis. Mh. And frankly, it's overwhelming. So what successful companies do is they bite off no more than they can chew at any given time. The reality is is you can only train a call center agent on a maximum of three skills at any given day. Right? And by focusing on focusing on problem areas, for a week for a month depending on how bad things are. And then once you've mastered that skill to take a baseline of of your performance and move on to the next worst skill. Right, is the way that companies succeed using this product?"
  checkGrammer(result)

except Exception as e:
  exception_type, exception_object, exception_traceback = sys.exc_info()
  line_number = exception_traceback.tb_lineno
  print(f'line {line_number}: {exception_type} - {e}')
