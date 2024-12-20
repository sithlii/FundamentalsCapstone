
def get_edit_input(nav, prompt):
    response = input(f"\n{prompt} ")
    vals = (response, nav)
    return vals

def print_user_select(info):
    print(f"\n{'ID':<4} {'Name'}")
    proc_ids = []
    for row in info:
        proc_ids.append(row[0])
        print(f'{row[0]:<4} {row[2]} {row[3]}')
    return proc_ids

def print_compass_ids(info, compass):
    ids = []
    print(f'{"ID":<4} {compass} Name')
    for row in info:
        ids.append(row[0])
        print(f'{row[0]:<4} {row[1]}')
    return ids

def print_assr_ids(info):
    ids = []
    print(f'\n{"ID":<4} {"Title":<30} {"Score":<5} {"Date Taken"} ')
    for row in info:
        ids.append(row[0])
        print(f'{row[0]:<4} {row[1]:<30} {row[2]:<5} {row[3]}')
    return ids