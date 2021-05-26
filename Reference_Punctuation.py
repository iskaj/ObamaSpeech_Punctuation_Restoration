import string
# from WAV_To_Transcript import speech_to_text, mp3_to_wav
# from Preprocess_Text import clean_text, strip_punctuation_text
import numpy as np
import time
from Levenshtein import ratio
from tqdm import tqdm
import os




# Get transcript from ASR system
# audioFile = mp3_to_wav(fileName + ".mp3")
# speech_to_text(audioFile, to_file=True)

# Clean actual speech text
# clean_text(fileName + ".txt")

# Give filename like "test_speech" without any additions
def file_name_to_asr_and_transcript(fileName):
    asrFileName = "asr_output/" + fileName + "_asr_output.txt"
    transcriptFileName = "transcripts/" + fileName + "_transcript.txt"
    return asrFileName, transcriptFileName

# Returns the strings of the asr output and transcript
def get_asr_and_transcript(asrFileName, transcriptFileName):
    text_asr, text_transcript = "", ""
    with open(asrFileName, 'r', encoding='utf-8') as f1:
        text_asr = f1.read()
        with open(transcriptFileName, 'r', encoding='utf-8') as f2:
            text_transcript = f2.read()
    return text_asr.lower(), text_transcript.lower()

# Create reference punctuation mapping
#if edit distance gets lower by placing it, do so
def ref_punc_mapping(fileName, toFile=True):
    asrFileName, transcriptFileName = file_name_to_asr_and_transcript(fileName)
    textAsr, textTranscript = get_asr_and_transcript(asrFileName, transcriptFileName)
    # origAsrText = textAsr
    tokens = [',', '.', '?']
    spaceIndeces = []
    for i in range(len(textAsr)):
        if textAsr[i] == " ":
            spaceIndeces.append(i)
    # print(spaceIndeces)
    changeCount = 0
    runRatio = True
    for spaceIndex in tqdm(spaceIndeces, position=0, leave=True):
        # print("curSpace: ", spaceIndex + changeCount)
        for token in tokens:
            newTextAsr = textAsr[0:spaceIndex + changeCount] + token + textAsr[spaceIndex + changeCount:]
            # print("TTR: ", textTranscript)
            # print("OTA: ", textAsr)
            # print("NTA: ", newTextAsr)
            if(runRatio):
                levOriginal = ratio(textAsr, textTranscript)
            runRatio = False
            # print("LO: ", levOriginal)
            levNew = ratio(newTextAsr, textTranscript)
            # print("LN: ", levNew)
            if levNew > levOriginal:  # The edit improves Levenshtein
                # print("-------- EDIT --------")
                textAsr = newTextAsr
                runRatio = True
                changeCount += 1
                break
    # print("TRANS TEXT: ", textTranscript)
    # print("ASR INIT TEXT: ", origAsrText)
    # print("FINAL TEXT: ", textAsr)
    if toFile:
        with open("reference_punc/" + fileName + "_reference_punc.txt", "w") as text_file:
            text_file.write(textAsr)
    return textAsr



for i in range(1, 4):
    print(i)
    fileName = str(i)
    transcript_file_name = "transcripts/" + fileName + "_transcript.txt"
    asr_file_name = "asr_output/" + fileName + "_asr_output.txt"
    if os.path.isfile(transcript_file_name) == os.path.isfile(asr_file_name) and os.path.isfile(transcript_file_name):
        start_time = time.time()
        refPunc = ref_punc_mapping(str(i), toFile=True)
        print("--- %s seconds ---" % (time.time() - start_time))


#
# # asrFileName, transcriptFileName = file_name_to_asr_and_transcript(fileName)
# # textAsr, textTransc = get_asr_and_transcript(asrFileName, transcriptFileName)
#
# # textAsr = "Thank you welly much Mr precedent Ladies and Gentlemen I am strong."
# # textTransc = "Thank you very much, Mr. President. Ladies and Gentlemen, I am strong."
#
# refPunc = ref_punc_mapping(fileName, toFile=True)

# print("--- %s seconds ---" % (time.time() - start_time))
