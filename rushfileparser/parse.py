def parse_rush_file(file_path):
    parsed_data = {
        'notation': [],
        'plain_text': [],
        'code': [],
        'token': []
    }

    with open(file_path, 'r') as file:
        current_type = None
        current_data = ''

        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace

            # Check if the line starts with <RTYPE>
            if line.startswith('<RTYPE'):
                # Check for variations of RTYPE and update current type and data
                if 'type=' in line:
                    current_type = line.split('type="', 1)[1].split('"', 1)[0]
                else:
                    current_type = line

                if current_type == '<RTYPE notation>':
                    parsed_data['notation'].append(current_data)
                elif current_type == '<RTYPE plain_text>':
                    parsed_data['plain_text'].append(current_data)
                elif current_type.startswith('<RTYPE code'):
                    code_type = current_type.split('type="', 1)[1].split('"', 1)[0]
                    parsed_data['code'].append((code_type, current_data))
                elif current_type == '<RTYPE token>':
                    token_data = ''  # Initialize the token data
                    for line in file:
                        line = line.strip()  # Remove leading/trailing whitespace
                        if line == '--end--':
                            break  # Exit loop when reaching '--end--'
                        token_data += line + '\n'  # Accumulate token data

                    parsed_data['token'].append(token_data.strip())  # Store the token data

                    current_data = ''  # Reset current_data for next iteration
                    continue  # Skip further processing for token

                current_data = ''  # Reset current_data
            else:
                current_data += line  # Accumulate the data

        # Add the last data to the parsed_data
        if current_type and current_data:
            if current_type == '<RTYPE notation>':
                parsed_data['notation'].append(current_data)
            elif current_type == '<RTYPE plain_text>':
                parsed_data['plain_text'].append(current_data)
            elif current_type.startswith('<RTYPE code'):
                code_type = current_type.split('type="', 1)[1].split('"', 1)[0]
                parsed_data['code'].append((code_type, current_data))

    return parsed_data
