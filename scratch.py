def parse_line(str_array):
    para = ''
    start = 0
    for character in str_array:
        if character == '=':
            start = 1
        else:
            if start == 0:
                continue
            elif character == '-':
                break
            else:
                para += character
    return para


with open('p') as file:
    for line in map(str.strip, file):
        if line.startswith('pixel_num'):
            print('pixel number is ', parse_line(line))
        elif line.startswith('model'):
            print('Model is ', parse_line(line))
        elif line.startswith('spectrometer_type'):
            print('Spectrometer type is ', parse_line(line))
        else:
            continue
