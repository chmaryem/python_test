

def execute_query(connection, user_input):
    try:
        query = "SELECT * FROM your_table WHERE your_column = %s"  # Replace with your actual query
       
        return connection.execute(query, (user_input,))
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
                                        