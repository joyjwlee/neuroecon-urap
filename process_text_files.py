import os, zipfile, sys, string

#########################################
################ METHODS ################
#########################################

# unzip all of the text files
def unzip_text_files():
    dir_list = ["coha-db", "coha-text", "coha-wlp"]
    extension = ".zip"

    for dir_name in dir_list:
        print("unzipping ", dir_name)

        # get the directory
        dir_name = os.path.join(os.path.dirname(__file__), dir_name)
        os.chdir(dir_name) # change directory from working dir to dir with files

        for item in os.listdir(dir_name): # loop through items in dir
            if item.endswith(extension): # check for ".zip" extension
                file_name = os.path.abspath(item) # get full path of files
                print("unzipping ", file_name)
                zip_ref = zipfile.ZipFile(file_name) # create zipfile object
                zip_ref.extractall(dir_name) # extract file to dir
                zip_ref.close() # close file
                os.remove(file_name) # delete zipped file

    print("done unzipping")

# rename all of the text files
"""
- for the purposes of training, files will be 0-indexed
- e.g. 1820-2010 will map to 0-19; 1930-2010 will map to 0-8
"""
def rename_text_files():
    # genre and their start year
    genre_start_year = {}
    genre_start_year["acad"] = 1820
    genre_start_year["fic"]  = 1820
    genre_start_year["mag"]  = 1820
    genre_start_year["news"] = 1860
    genre_start_year["tvm"]  = 1930

    # go into coha-text
    text_directory = os.path.join(os.path.dirname(__file__), "coha-text")
    os.chdir(text_directory) # change directory from working dir to dir with files

    # loop through all of the text files and rename them
    for item in os.listdir(text_directory):
        words = item.split("_")
        print(words)
        file_rename = words[1] + "_" + str((int(words[2][0:4]) - genre_start_year[words[1]]) // 10) + ".txt"
        os.rename(item, file_rename)
        print(file_rename)

# clean all of the text files
def clean_text_files():
    # go into coha-text
    text_directory = os.path.join(os.path.dirname(__file__), "coha-text")
    os.chdir(text_directory) # change directory from working dir to dir with files

    # list of stop words
    stop_words = {"ourselves", "hers", "between", "yourself", "but", "again", "there", "about", 
                "once", "during", "out", "very", "having", "with", "they", "own", "an", "be", 
                "some", "for", "do", "its", "yours", "such", "into", "of", "most", "itself", 
                "other", "off", "is", "s", "am", "or", "who", "as", "from", "him", "each", "the", 
                "themselves", "until", "below", "are", "we", "these", "your", "his", "through", 
                "don", "nor", "me", "were", "her", "more", "himself", "this", "down", "should", 
                "our", "their", "while", "above", "both", "up", "to", "ours", "had", "she", "all", 
                "no", "when", "at", "any", "before", "them", "same", "and", "been", "have", "in", 
                "will", "on", "does", "yourselves", "then", "that", "because", "what", "over", 
                "why", "so", "can", "did", "not", "now", "under", "he", "you", "herself", "has", 
                "just", "where", "too", "only", "myself", "which", "those", "i", "after", "few", 
                "whom", "t", "being", "if", "theirs", "my", "against", "a", "by", "doing", "it", 
                "how", "further", "was", "here", "than"}
    gender_words = {"he","him","his","himself", "she", "her", "hers", "herself"}
    for word in gender_words:
        stop_words.remove(word)

    # loop through all of the text files and clean them
    for item in os.listdir(text_directory):
        # just mac things
        if (item == ".DS_Store"):
            continue

        # open the text file
        input_file = open(item, "r")

        # loop through the text file
        cleaned_content = ""
        count = 0
        while True:
            line = input_file.readline()
            if not line:
                break

            sys.stdout.write("\rReading sentence #{}".format(count))
            sys.stdout.flush()
            count += 1

            tokens = line.split()
            tokens = [w.lower() for w in tokens]
            
            table = str.maketrans("", "", string.punctuation)
            stripped = [w.translate(table) for w in tokens]

            words = [word for word in stripped if word.isalpha()]
            words = [w for w in words if not w in stop_words]

            output_str = " "
            output_str = output_str.join(words)
            cleaned_content += output_str + "\n"
        input_file.close()

        # delete everything in the text file
        open(item, "w").close()

        # open it again to write cleaned content
        input_file = open(item, "w")
        input_file.write(cleaned_content)
        input_file.close()

        print("\tfinished", item)

# create concatenated (merged) text files for each genre
def generate_concatenated():
    # directory
    text_directory = os.path.join(os.path.dirname(__file__), "coha-text")

    # genre and number of decades
    genre_num_decades = [   ["acad", 20],
                            ["fic", 20], 
                            ["mag", 20], 
                            ["news", 16], 
                            ["tvm", 9]]

    # loop through each genres
    for item in genre_num_decades:
        # get genre and number of decades
        genre = item[0]
        num_decades = int(item[1])

        # get contents -- loop through each decade
        contents = ""
        for idx in range(num_decades):
            # read in data from text file and add
            temp = ""
            with open(f"{text_directory}/{genre}_{idx}.txt") as fp:
                temp = fp.read()
            contents += " "
            contents += temp
        # once done looping, write file
        with open(f"{text_directory}/{genre}.txt", "w") as fp:
            fp.write(contents)
        print(f"merged text files for {genre}")

# make one line versions of the cleaned text files (this is for DWE, will create a new directory)
def generate_one_liners():
    # safely create "coha-text-oneline" directory
    os.chdir(os.path.dirname(__file__))
    if not os.path.exists("coha-one-line"):
        os.makedirs("coha-one-line")

    # create text and one liner directories
    text_directory = os.path.join(os.path.dirname(__file__), "coha-text")
    one_line_directory = os.path.join(os.path.dirname(__file__), "coha-one-line")

    # loop through each
    for item in os.listdir(text_directory):
        # just mac things
        if (item == ".DS_Store"):
            continue

        # set up filepaths and open files
        input_filepath = f"{text_directory}/{item}"
        output_filepath = f"{one_line_directory}/{item}"
        input_file = open(input_filepath, 'r')
        output_file = open(output_filepath, 'w')

        # loop through lines
        text = ""
        for line in input_file:
            stripped_line = line.rstrip()
            text += stripped_line + " "

        # write and close        
        output_file.write(text)
        input_file.close()
        output_file.close()

        print("finished concatenating\t", item)

#########################################
############# METHOD CALLS ##############
#########################################

# get the raw text files
unzip_text_files()
# make the text files 0-based indexing
rename_text_files()
# clean the text files
clean_text_files()
# create a concatenation for each of the genres
generate_concatenated()
# finally create one liners (concatenated) versions for all of the text files
generate_one_liners()
