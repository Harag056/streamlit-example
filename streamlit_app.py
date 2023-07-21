import streamlit as st
import snowflake.connector


st.title("Snowflake Connection App")

# Input fields for Snowflake connection parameters
# snowflake_account = st.text_input("Snowflake Account", "")
# snowflake_user = st.text_input("User", "")
# snowflake_password = st.text_input("Password", "", type="password")
# snowflake_warehouse = st.text_input("Warehouse", "")
# snowflake_database = st.text_input("Database", "")
# snowflake_schema = st.text_input("Schema", "")

snowflake_username = 'TESTUSER'
snowflake_password = 'Test@123'
snowflake_account = 'rz20203.central-india.azure.snowflakecomputing.com'
snowflake_warehouse = 'COMPUTE_WH'
snowflake_database = 'LandingAI_DB'
snowflake_schema = 'Raw'

# Function to connect to Snowflake
def connect_to_snowflake():
    conn = snowflake.connector.connect(
        user=snowflake_username,
        password=snowflake_password,
        account=snowflake_account,
        warehouse=snowflake_warehouse,
        database=snowflake_database,
        schema=snowflake_schema
    )
    return conn

# Function to execute a Snowflake query and return results
def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

# Streamlit app
def main():
    st.title("Snowflake Data Viewer")
    
    # Connect to Snowflake
    try:
        conn = connect_to_snowflake()
        st.success("Connected to Snowflake")
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {str(e)}")
        return
    
    # Query input
    query_input = st.text_area("Enter your Snowflake SQL query:")
    
    if st.button("Run Query"):
        # Execute the query and display results
        try:
            results = execute_query(conn, query_input)
            if results:
                st.table(results)
            else:
                st.info("No results to display.")
        except Exception as e:
            st.error(f"Error executing query: {str(e)}")
    
    # Close the Snowflake connection when the app is closed
    st.experimental_rerun_on_finish(connect_to_snowflake)
    conn.close()

if __name__ == "__main__":
    main()
