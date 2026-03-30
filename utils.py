

def execute_query(connection, user_input):
    try:
       query = "SELECT * FROM your_table WHERE your_column = ?"
       with connection.execute(query, (user_input,)) as cursor:
              return cursor.fetchall()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
                                        