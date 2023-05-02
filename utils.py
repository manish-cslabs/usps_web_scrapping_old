def save_content_in_file(content, filename,
                            directory_name="scrap_data"):
    import os
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)
    file_path = directory_name + "/" + filename
    
    with open(file_path, 'w') as f:
        f.write(content)



