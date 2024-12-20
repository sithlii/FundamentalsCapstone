import sqlite3

connection = sqlite3.connect("capstone.db")
cursor = connection.cursor()

def user_profile(id):
    user_info = cursor.execute("SELECT * FROM Users WHERE user_id = ?", (id,)).fetchone()
    print(f'[1] First Name: {user_info[3]}\n[2] Last Name: {user_info[4]}\n[3] Email: {user_info[1]}\n[4] Password: *********\n[5] Phone: {user_info[5]}\nDate Hired: {user_info[6]}\nUser Type: {user_info[-1]}\n')
    return user_info

def get_comp_info(nav):
    comp_info = cursor.execute("SELECT name, description FROM Competencies WHERE competency_id = ?", (nav,)).fetchone()
    print(f'[1] Name: {comp_info[0]}\n[2] Description: {comp_info[1]}\n')
    return comp_info

def get_assess_info(nav):
    assess_info = cursor.execute("SELECT a.title, c.name FROM Assessments a JOIN Competencies c ON a.competency_id = c.competency_id WHERE assessment_id = ?", (nav,)).fetchone()
    print(f'[1] Assessment Title: {assess_info[0]}\n[2] Associated Competency: {assess_info[1]}\n')
    return assess_info

def get_assr_info(nav):
    assr_info = cursor.execute("SELECT a.title, ar.score, ar.date_taken FROM Assessment_Results ar JOIN Assessments a ON ar.assessment_id = a.assessment_id WHERE result_id = ?", (nav,)).fetchone()
    print(f'Assessment Title: {assr_info[0]}\nScore: {assr_info[1]}\nDate Taken: {assr_info[2]}\n')
    return assr_info

def gen_update(table_name, column_name, identifier, vals):
    cursor.execute(f"UPDATE {table_name} SET {column_name} = ? WHERE {identifier} = ?", vals)
    connection.commit()
    print("Edit successfully committed!")

def competency_list(cursor):
    competencies = [('Data Types', 'Labels that tell what kind of info a piece of data represents.'),
                    ('Variables', 'Variables give us a way to store and access info within a program.'),
                    ('Functions', 'Reusable blocks of code that perform specific tasks.'),
                    ('Boolean Logic', 'True or False. Yes or No.'),
                    ('Conditionals', 'You can give statements that allow your program to make decisions based on certain conditions.'),
                    ('Loops', 'Understand how to repeat a block of code multiple times.'),
                    ('Data Structures', 'You can provide a backbone for your program, managing collections of data.'),
                    ('Lists', 'Ordered collections of mutable data.'),
                    ('Dictionaries', 'You can store data in collections of key-vale pairs.'),
                    ('Working with Files', 'You can read, write, and manipulate data to and from files.'),
                    ('Exception Handling', 'You understand how to deal with unexpected errors that might occur during execution.'),
                    ('Quality Assurance (QA)', 'You can test, debug and verfiy that a program meets its requirements.'),
                    ('Object-Oriented Programming (OOP)', 'You understand how to use objects to represent data and behavior.'),
                    ('Recursion', 'You understand how to solve problems that can be broken down into smaller pieces.'),
                    ('Databases', 'You can create, manipulate, and navigate databases.')]
    query = "INSERT INTO Competencies (name, description) VALUES (?,?)"
    for element in competencies:
        ist_vals = (element[0], element[1])
        cursor.execute(query, ist_vals)
        connection.commit()