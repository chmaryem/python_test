

def execute_query(connection, user_input):
    try:
       
        return connection.execute(query, (user_input,))
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
                                        