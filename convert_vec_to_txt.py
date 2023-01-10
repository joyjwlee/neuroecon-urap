import os, gensim

# unzip all of the text files
def convert(dim):
    # create directory if not made yet
    vec_text_directory = os.path.join(os.path.dirname(__file__), f"vectors_{dim}_txt")
    if not os.path.exists(vec_text_directory):
        os.makedirs(vec_text_directory)

    # loop through all of the models (vectors) of dimension `dim`
    vec_directory = os.path.join(os.path.dirname(__file__), f"vectors_{dim}")
    for item in os.listdir(vec_directory):
        # input and output paths
        model_input_path = os.path.join(vec_directory, item)
        model_output_path = os.path.join(vec_text_directory, item[:-6])
        # convert to text
        exec(f"model = gensim.models.KeyedVectors.load('{model_input_path}')")
        exec(f"model.wv.save_word2vec_format('{model_output_path}.txt')")
        print("converted ", item[:-6])
        
    print("done converting!")

# convert models for 50 dimension embeddings
convert(50)
