import re, string, os

def clean_text(txtFileName, index, toFile=True, verbose=False):
    """Cleans/preprocesses a .txt file to cleaner text and returns the text as a string.
    :param txtFileName: .wav file in current directory
    :returns: cleaned text as a string
    """
    with open(txtFileName, 'r', encoding='utf-8') as f:
        text = f.read()

        # Double or single line breaks are all removed to make text a "one liner"
        text = text.replace("\n", " ")

        # To adhere to utf-8
        text = text.replace("’", "'")

        # Remove everything between brackets [sic] [audience laughs] and remove double spaces afterwards
        text = re.sub(r'[\(\[].*?[\)\]]', "", text)
        text = text.replace("  ", " ")

        # All * and "" are removed
        removeList = ["*", "\""]
        for s in removeList:
            text = text.replace(s, "")

        # Pauses indicated by "--" or "—" are replaced by a comma which is most accurate
        # from subjective listening+reading experience
        toCommaList = [" --", "—"]
        for s in toCommaList:
            text = text.replace(s, ",")

        # Triple ... or double .. dots are replaced by spaces
        toSpaceList = ["...", ".."]
        for s in toSpaceList:
            text = text.replace(s, " ")

        # % sign to" percent"
        text = text.replace("%", " percent")

        # Remove citations1, such2 and seat.2
        text = re.sub(r'([a-zA-Z]+\.*)\d+', r'\1', text)

        # Change " ," to "," to make sure there are no floating commas
        text = text.replace(" ,", ",")

        if verbose:
            print(text)

        # print(txt_file_name[:-4])

        if toFile:
            with open('D:/University/Master/Automatic Speech Recognition/Web Crawler/transcripts/' + str(index) +  "_transcript.txt", "w", encoding='utf-8') as textFile:
                textFile.write(text)
        return text

def strip_punctuation_text(txtFileName, index, toFile=True, verbose=False):
    """Strips punctuation from a .txt file and returns the text as a string.
    :param txtFileName: .wav file in current directory
    :returns: stripped text as a string
    """
    with open(txtFileName, 'r', encoding='utf-8') as f:
        text = f.read()

        # All * and "" are removed
        remove_list = string.punctuation
        print(remove_list)
        for s in remove_list:
            text = text.replace(s, "")
            
        #text.replace('“', '')
        text = text.lower()

        if verbose:
            print(text)

        if toFile:
            with open('D:/University/Master/Automatic Speech Recognition/Web Crawler/removed_punctuation/' + str(index) + "_stripped.txt", "w", encoding='utf-8') as text_file:
                text_file.write(text)
        return text


# clean_text("Speech_Fed_Plaza.txt", to_file=True, verbose=True)
# strip_punctuation_text("clean_Speech_Fed_Plaza.txt", to_file=True, verbose=True)
        
def remove_extras():
    for i in range(69,461):
        print(i)
        file_name = 'D:/University/Master/Automatic Speech Recognition/Web Crawler/transcripts/' + str(i) + '_transcript.txt'
        if os.path.isfile(file_name):
            with open(file_name, encoding='utf-8') as f:
                text = f.read()
                text = text.replace("Book/CDs by Michael E. Eidenmuller, Published by McGraw-Hill", '')
                with open('D:/University/Master/Automatic Speech Recognition/Web Crawler/transcripts/' + str(i) + '_transcript.txt', "w", encoding='utf-8') as text_file:
                    text_file.write(text)
        
def convert_files():
    for i in range(461):
        print(i)
        file_name = 'D:/University/Master/Automatic Speech Recognition/Web Crawler/transcripts/' + str(i) + '_transcript.txt'
        if os.path.isfile(file_name):
            #clean_text(file_name, i, toFile=True)
            strip_punctuation_text(file_name, i, toFile=True)
            
convert_files()
            

