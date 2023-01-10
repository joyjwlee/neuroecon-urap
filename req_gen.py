# requirements generator

# open original file -- make sure you delete the first line that specifies the Python version
orig_file = open("python_package_list.txt", "r")

# combine into a single string
output = ""
for line in orig_file:
    output += line.split('=')[0] + "\n"

# print to `requirements.txt`
output_file = open("requirements.txt", "w")
output_file.write(output)

# close files
orig_file.close()
output_file.close()
