def choice(array_selected):
    now = datetime.now()
    random.seed( now )
    num_choice_face=random.randint(0,TOTAL_CUTS)
    if num_choice_face in array_selected:
        choice(array_selected)
    else:
        array_selected.append(num_choice_face)
    return array_selected, num_choice_face
