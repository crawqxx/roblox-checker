def calculate_beauty(nick):
    good_letters = {'w', 'e', 'r', 'u', 'i', 'o', 'p', 'a', 's', 'z', 'x', 'c', 'v', 'n', 'm'}
    
    parts = nick.split('_')
    
    bad_letters_penalty = 0
    for char in nick:
        if char != '_' and char not in good_letters:
            bad_letters_penalty += 1
    
    max_repeat_score = 0
    for part in parts:
        if not part:
            continue
        char_counts = {}
        for char in part:
            char_counts[char] = char_counts.get(char, 0) + 1
        if char_counts:
            current_max = max(char_counts.values())
            if current_max > max_repeat_score:
                max_repeat_score = current_max
    
    length_penalty = 0
    for part in parts:
        if len(part) <= 2:
            length_penalty += (3 - len(part)) 
    
    underscore_penalty = 0
    if len(parts) > 1:
        left, right = parts[0], parts[1]
        if (left and left[-1] not in good_letters) or (right and right[0] not in good_letters):
            underscore_penalty += 1
    
    beauty_score = (max_repeat_score * 2) - (bad_letters_penalty * 3) - (length_penalty * 1) - (underscore_penalty * 2)
    return beauty_score

def sort_nicks_by_beauty(input_filename, output_filename):
    with open(input_filename, 'r') as f:
        nicks = [line.strip() for line in f if line.strip()]
    
    sorted_nicks = sorted(nicks, key=lambda x: -calculate_beauty(x))
    
    with open(output_filename, 'w') as f:
        for nick in sorted_nicks:
            f.write(nick + '\n')

sort_nicks_by_beauty('available.txt', 'avenchanced.txt')