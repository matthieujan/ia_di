def print_dict(dict):
    for element in dict:
        print(element)
        for sub_element in dict.get(element):
            print(sub_element + " : " + str(dict.get(element).get(sub_element)))
