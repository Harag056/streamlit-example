import streamlit as st
import snowflake.connector


st.title("Snowflake Connection App")

# Input fields for Snowflake connection parameters
snowflake_account = st.text_input("Snowflake Account", "")
snowflake_user = st.text_input("User", "")
snowflake_password = st.text_input("Password", "", type="password")
snowflake_warehouse = st.text_input("Warehouse", "")
snowflake_database = st.text_input("Database", "")
snowflake_schema = st.text_input("Schema", "")

if st.button("Connect"):
    # Connect to Snowflake
    #try:
    """
    connection = snowflake.connector.connect(
        account=snowflake_account,
        user=snowflake_user,
        password=snowflake_password,
        warehouse=snowflake_warehouse,
        database=snowflake_database,
        schema=snowflake_schema
    )
    """
    print(snowflake_account)
    snowflake_user
    """
    cursor = connection.cursor()

    # Execute a sample query
    cursor.execute("SELECT CURRENT_TIMESTAMP() as CurrentTime;")
    result = cursor.fetchone()

    st.success(f"Connected to Snowflake! Current timestamp: {result[0]}")
    connection.close()
    """
   # except Exception as e:
     #   st.error(f"Error: {e}")
     #   connection.close()

