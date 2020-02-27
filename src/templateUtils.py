from flask import Flask


#@app.template_filter('truncate_description')
def truncate_description(long_description: str, characters: int = 160):
    """ 
    desc: truncate long description strings to 160 char 
    usage: {{ description | truncate_description(characters=20)
    """
    if len(long_description) <= characters:
        return long_description
    small_description = long_description[:characters].split(" ")[:-1]
    return " ".join(small_description)+'…'
