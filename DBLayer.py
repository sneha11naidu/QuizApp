import sqlite3

con = sqlite3.connect('Quiz.db')
cur = con.cursor()


def getListOfModules():
    cur.execute('SELECT * FROM Module')
    module_list = cur.fetchall()
    # print(module_list)
    con.commit()
    # con.close()
    return module_list

# unit testing
# my_module_list = getListOfModules()
# print(my_module_list)


def getQuestions(moduleID):
    sql_string = "SELECT  * FROM Question WHERE moduleID = " + str(moduleID) + " LIMIT 5"
    cur.execute(sql_string)
    all_questions = cur.fetchall()
    return all_questions

# unit testing
# questions = getQuestions(1)
# print(questions)


def get_potential_answers(questionID):
    """ For a given question, return the answer options"""
    cur.execute('SELECT * FROM Answer WHERE questionID=' + str(questionID))
    options = cur.fetchall()
    return options

# unit testing
# all_options = get_potential_answers(1)
# print(all_options)


def save_selected_answer(userID, moduleID, questionID, selected_answerID, isCorrect):
    """
    This method saves the answer given by the user into the database
    Arguments:
        userID: The user identifier (primary key)
        moduleID: the selected module id
        questionID: for which question are we storing the selected ans
        selected_answerID: out of 4 options, which one was selected
        isCorrect: was the selected ans correct???
    """
    sql_string = ("INSERT INTO useranswers(userID, moduleID, questionID, selectedanswerID, iscorrect) VALUES("
                  + str(userID) + ","
                  + str(moduleID) + ","
                  + str(questionID) + ","
                  + str(selected_answerID) + ","
                  + str(isCorrect) + ")")

    print(sql_string)
    cur.execute(sql_string)
    con.commit()
    return cur.lastrowid
# ====================================

# unit test
# unit testing
# save_selected_answer(1, 2, 2, 1, 1)

def calculate_score(userID, moduleID):
    # Get the total number of questions attempted in a module
    sql_string_1 = ("SELECT COUNT(*) FROM useranswers WHERE userID = "
                    + str(userID) + " AND moduleID=" + str(moduleID))

    cur.execute(sql_string_1)
    cur_result = cur.fetchall()
    total_count = cur_result[0][0]

    # Get the total number of questions that were correctly answered
    # print(sql_string)

    sql_string_2 = ("SELECT COUNT(*) FROM useranswers WHERE userID = "
                    + str(userID) + " AND moduleID=" + str(moduleID) + " AND iscorrect=1")

    cur.execute(sql_string_2)
    cur_result = cur.fetchall()
    is_correct_count = cur_result[0][0]

    print("total q:" + str(total_count) + " total correct: " + str(is_correct_count))

    return (is_correct_count, total_count)


# unit testing
total_score = calculate_score(1, 1)
print(total_score)




