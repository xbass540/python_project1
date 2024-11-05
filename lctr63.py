contents = ["sentence 1", "sentence 2", "sentence 3"]

filenames = ["doc.txt", "report.txt", "presentation.txt"]

for content, filename in zip(contents,filenames):
    file = open(f"files/{filename}", 'w')
    file.write(content)