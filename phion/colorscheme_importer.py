from phion import ColorScheme
import os

# GOGH Format - https://github.com/Gogh-Co/Gogh/blob/master/themes/

def import_gogh_template(file):
    with open(file, 'r') as f:
        data = f.readlines()

        lst_data = {}

        for line in data:
            if line.startswith('#') or line.startswith("\n"):
                continue
            line = line.replace('\n','').replace('export','').replace('COLOR_','color').split('   ')[0].replace(' ','').replace('color0','color').lower()
            if '="#' not in line:
                continue
            color_var = line.split('=')[0]
            color_val = line.split('"')[1]

            lst_data[color_var] = color_val
        
        _new_colorscheme = ColorScheme(os.path.basename(file).split(".")[0].replace('-','_'), lst_data)
        return _new_colorscheme

def write_to_file(colorscheme, file):
    with open(file, 'a') as f:
        f.write(f"    {colorscheme.name} = ColorScheme('{colorscheme.name}', {colorscheme.colors})\n")

for file in os.listdir("phion/themes/"):
    cs = import_gogh_template(f'phion/themes/{file}')
    write_to_file(cs, 'phion/enums/colorschemes.py')