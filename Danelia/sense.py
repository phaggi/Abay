import sqlite3


def findquestion(_question):
    """
    return sense by question
    :param _question: question
    :return: sense
    """
    sql = 'select sense from senses where id in (select sense_id from questions where question = "' + _question + '")'
    return db.execute(sql)


if __name__ == '__main__':
    db = sqlite3.connect('database.db')
    c = db.cursor()
    question = 'как тебя зовут'
    result = findquestion(question)
    print(result.fetchone()[0])
