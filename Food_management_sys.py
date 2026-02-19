import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as ans
import streamlit as st

df_claims = pd.read_csv("claims_data.csv")
df_food_listings = pd.read_csv("food_listings_data.csv")
df_providers = pd.read_csv("providers_data.csv")
df_receivers = pd.read_csv("receivers_data.csv")

# print(df_claims.info())
#  #   Column       Non-Null Count  Dtype
# ---  ------       --------------  -----
#  0   Claim_ID     1000 non-null   int64
#  1   Food_ID      1000 non-null   int64
#  2   Receiver_ID  1000 non-null   int64
#  3   Status       1000 non-null   object
#  4   Timestamp    1000 non-null   object
# print(df_food_listings.info())
#  #   Column         Non-Null Count  Dtype
# ---  ------         --------------  -----
#  0   Food_ID        1000 non-null   int64
#  1   Food_Name      1000 non-null   object
#  2   Quantity       1000 non-null   int64
#  3   Expiry_Date    1000 non-null   object
#  4   Provider_ID    1000 non-null   int64
#  5   Provider_Type  1000 non-null   object
#  6   Location       1000 non-null   object
#  7   Food_Type      1000 non-null   object
#  8   Meal_Type      1000 non-null   object
# print(df_providers.info())
#  #   Column       Non-Null Count  Dtype
# ---  ------       --------------  -----
#  0   Provider_ID  1000 non-null   int64
#  1   Name         1000 non-null   object
#  2   Type         1000 non-null   object
#  3   Address      1000 non-null   object
#  4   City         1000 non-null   object
#  5   Contact      1000 non-null   object
# dtypes: int64(1), object(5)
# print(df_receivers.info())
#  #   Column       Non-Null Count  Dtype
# ---  ------       --------------  -----
#  0   Receiver_ID  1000 non-null   int64
#  1   Name         1000 non-null   object
#  2   Type         1000 non-null   object
#  3   City         1000 non-null   object
#  4   Contact      1000 non-null   object
# dtypes: int64(1), object(4)

# CREATE DATABASE....

conn = sqlite3.connect("Food_wastage.db")
cursor = conn.cursor()
# CREATE TABLES....
# 1st table 
cursor.execute("""
CREATE TABLE IF NOT EXISTS provider(
               Provider_ID INTEGER PRIMARY KEY,
               Name TEXT,
               Type TEXT,
               Address TEXT,
               City TEXT,
               Contact TEXT
                  )""")
# 2ND TABLE.....
cursor.execute("""
CREATE TABLE IF NOT EXISTS receivers(
               Receiver_ID INTEGER PRIMARY KEY,
               Name TEXT,
               Type TEXT,
               City TEXT,
               Contact TEXT
               )""")
# 3RD TABLE....
cursor.execute("""
CREATE TABLE IF NOT EXISTS claims(
               Claim_ID INTEGER PRIMARY KEY,
               Food_ID INTEGER,
               Receiver_ID Integer,
               Status TEXT,
               Timestamp TEXT
               )""")
# 4TH TABLE.....
cursor.execute("""
CREATE TABLE IF NOT EXISTS food_listings (
               Food_ID INTEGER PRIMARY KEY,
               Food_Name TEXT,
               Quantity Integer,
               Expiry_Date TEXT,
               Provider_ID INTEGER,
               Provider_Type TEXT,
               Location TEXT,
               Food_Type TEXT,
               Meal_Type TEXT
               )""")

# INSERT THE DATA INTO TABLES...

# for i, row in df_providers.iterrows():
#     cursor.execute("""
#         INSERT INTO provider(Provider_ID,Name,Type,Address,City,Contact)
#         Values(?,?,?,?,?,?)
#     """,tuple(row))

# for i, row in df_food_listings.iterrows():
#     cursor.execute("""
#         INSERT INTO food_listings(Food_ID,Food_Name,Quantity,Expiry_Date,Provider_ID,Provider_Type,Location,Food_Type,Meal_Type)
#         VALUES (?,?,?,?,?,?,?,?,?)   
#     """, tuple(row))

# for i, row in df_claims.iterrows():
#      cursor.execute("""
#          INSERT INTO claims(Claim_ID,Food_ID,Receiver_ID,Status,Timestamp)
#          VALUES(?,?,?,?,?)
#     """ , tuple(row))

# for i, row in df_receivers.iterrows():
#     cursor.execute("""
#         INSERT INTO receivers(Receiver_ID,Name,Type,City,Contact)
#         VALUES (?,?,?,?,?)   
#     """, tuple(row))    

conn.commit()

# data = pd.read_sql_query("SELECT * FROM receivers;", conn)
# print(data)

# cursor.execute(query)
# result=cursor.fetchall()
# top_cities_df = pd.DataFrame(result,columns=["City","provider_count"])

# cursor.execute("DROP TABLE IF EXISTS provider")
# conn.commit()

# SQL QUERIES.....

# 1.How many food providers and receivers are there in each city?
query1 ="""
    SELECT City, COUNT(*) AS Provider_count
    FROM provider
    GROUP BY City
    ORDER BY Provider_count DESC
"""    
cursor.execute(query1)   
result1 = cursor.fetchall()  
df1 = pd.DataFrame(result1,columns=["City","Provider_count"])  

query2 ="""
    SELECT City, COUNT(*) AS Receiver_count
    FROM receivers
    GROUP BY City
    ORDER BY Receiver_count DESC
"""
cursor.execute(query2)
result2 = cursor.fetchall()
df2 = pd.DataFrame(result2,columns=["City","Receiver_count"])
# print(receiverCount_df)
# print(providerCount_df)

# 2.Which type of food provider (restaurant, grocery store, etc.) contributes the most food?
query3 = """
    SELECT Type, COUNT(*) AS prov_type_count
    FROM provider
    GROUP BY Type
    ORDER BY prov_type_count DESC
"""
cursor.execute(query3)
result3 = cursor.fetchall()
df3 = pd.DataFrame(result3,columns=["Type","prov_type_count"])
# print(prov_type_df)

# 3.What is the contact information of food providers in a specific city?
# city = input("Enter the Valid City name:")
# query4 = """
#     SELECT Name,Address,Contact
#     FROM provider
#     WHERE City = ?
# """
# cursor.execute(query4,(city,))
# rowss = cursor.fetchall()
# columns = [description[0] for description in cursor.description]
# df4 = pd.DataFrame(rowss, columns=columns)
# print(prov_details_df)

# 4.Which receivers have claimed the most food?
query5 = """
    SELECT Type,COUNT(*) AS recev_type_count
    FROM receivers
    GROUP BY Type
    ORDER BY recev_type_count DESC
"""
cursor.execute(query5)
result4 = cursor.fetchall()
df5 = pd.DataFrame(result4,columns=["Type","recev_type_count"])
# print(recev_type_df)

# 5.What is the total quantity of food available from all providers?
query6 ="""
    SELECT Provider_Type, SUM(Quantity) AS total_Quant
    FROM food_listings
    GROUP BY Provider_Type
    ORDER BY total_Quant DESC"""
cursor.execute(query6)
result5 = cursor.fetchall()
df6 = pd.DataFrame(result5,columns=["Provider_Type","total_Quant"])
# print(total_quant_df)

# 6.Which city has the highest number of food listings?
query7 = """
    SELECT Location,COUNT(*) AS total_listing
    FROM food_listings
    GROUP BY Location
    ORDER BY total_listing DESC
"""
cursor.execute(query7)
result6 = cursor.fetchall()
df7 =pd.DataFrame(result6,columns=["Location","total_listing"])
# print(total_listing_df)

# 7.What are the most commonly available food types?
query8 = """
    SELECT Food_Type,COUNT(*) AS total_count
    FROM food_listings
    GROUP BY Food_Type
    ORDER BY total_count DESC
"""
cursor.execute(query8)
result7 = cursor.fetchall()
df8 =pd.DataFrame(result7,columns=["Food_Type","total_count"])
# print(total_foodCount_df)

# 8.  How many food claims have been made for each food item?
query9 = """
   SELECT f.Food_Name, COUNT(c.Claim_ID) AS claim_count
   FROM food_listings f
   LEFT JOIN claims c
      ON f.Food_ID = c.Food_ID
   GROUP BY f.Food_Name
   ORDER BY claim_count DESC"""
cursor.execute(query9)
result8 = cursor.fetchall()
df9 =pd.DataFrame(result8,columns=["Food_Name","claim_count"])
# print(claimCount_df)

# 9. Which provider has had the highest number of successful food claims?
query10 = """
   SELECT p.Name, COUNT(c.Claim_ID) AS completed_claims
   FROM provider p
   JOIN food_listings f
      ON p.Provider_ID = f.Provider_ID
   JOIN claims c
      ON f.Food_ID = c.Food_ID
   WHERE c.Status ='Completed'
   GROUP BY p.Name
   ORDER BY completed_claims DESC
   LIMIT 20;"""
cursor.execute(query10)
result9 = cursor.fetchall()
df10 = pd.DataFrame(result9,columns=["Provider_name","completed_claims"])
# print(completed_claims_df)

# 10.What percentage of food claims are completed vs. pending vs. canceled?
query11 = """
SELECT Status,COUNT(*) AS total_claims,ROUND(COUNT(*)*100.0/(SELECT COUNT(*)FROM claims),2)AS PERCENTAGE
FROM claims
GROUP BY Status"""
cursor.execute(query11)
result10 = cursor.fetchall()
df11 = pd.DataFrame(result10,columns=["status","total_claims","Percentage"])
# print(claims_percentage_df)

# 11. What is the average quantity of food claimed per receiver?
query12="""
   SELECT r.Name, AVG(f.Quantity)AS avg_quant_perReceiver
   FROM receivers r
   JOIN claims c
      ON r.Receiver_ID = c.Receiver_ID
   JOIN food_listings f
      ON c.Food_ID = f.Food_ID
   GROUP BY r.Name
   ORDER BY avg_quant_perReceiver DESC
   LIMIT 20;"""
cursor.execute(query12)
result11 = cursor.fetchall()
df12 = pd.DataFrame(result11,columns=["Receiver_name","Food_Avg-Quantity"])


# 12. Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?
query13 = """
   SELECT f.Meal_Type, COUNT(c.Claim_ID) AS total_claims
   FROM food_listings f
   LEFT JOIN claims c
      ON f.Food_ID = c.Food_ID
   GROUP BY f.Meal_Type
   ORDER BY total_claims DESC"""
cursor.execute(query13)
result12 = cursor.fetchall()
df13 = pd.DataFrame(result12,columns=["Meal_Type","total_claims"])
# print(mealClaimed_df)

# 13.What is the total quantity of food donated by each provider?
query14 ="""
SELECT p.Name,SUM(f.Quantity) AS total_quant
FROM provider p
LEFT JOIN food_listings f
   ON p.Provider_ID = f.Provider_ID
GROUP BY p.Name
ORDER BY total_quant DESC
LIMIT 20;"""
cursor.execute(query14)
result13 = cursor.fetchall()
df14 =pd.DataFrame(result13,columns=["provider_name","total_quantity"])
# print(tot_foodBy_provider_df)

# My queries....
# 14.Number of Successful receivers per location
query15 ="""
SELECT r.City,COUNT(r.Receiver_ID) AS successful_receivers
FROM receivers r
LEFT JOIN claims c
   ON r.Receiver_ID = c.Receiver_ID
WHERE c.Status ='Completed'
GROUP BY r.City
ORDER BY successful_receivers DESC;"""
cursor.execute(query15)
result14 = cursor.fetchall()
df15 = pd.DataFrame(result14,columns=["City","Receiver_id"])

# 15.total food quant in each meal type
query16="""
SELECT Meal_Type, Food_Name, Quantity
FROM food_listings
WHERE (Meal_Type, Quantity) IN (
    SELECT Meal_Type, MAX(Quantity)
    FROM food_listings
    GROUP BY Meal_Type
);"""
cursor.execute(query16)
result15 = cursor.fetchall()
df16 = pd.DataFrame(result15,columns=["Meal_type","Food_name","Quantity"])
# print(df16)

# CREATE AN EXCEL FILE WHICH CONTAINS ALL THE DF OF QUERIES.....

# with pd.ExcelWriter("All_SQL_queries.xlsx") as writer:
#     df1.to_excel(writer, sheet_name="Providers_count_INcities", index=False)
#     df2.to_excel(writer, sheet_name="Receivers_count_INCities", index=False)
#     df3.to_excel(writer, sheet_name="Mostly_providesFood_ProvType", index=False)
#    #  df4.to_excel(writer, sheet_name="Providers_contact_info.", index=False)
#     df5.to_excel(writer, sheet_name="Mostly_ClaimedFood_Receivers", index=False)
#     df6.to_excel(writer, sheet_name="Total_quanOfFood_byProviders", index=False)
#     df7.to_excel(writer, sheet_name="City_withFood_listings", index=False)
#     df8.to_excel(writer, sheet_name="Most_Available_foodTypes", index=False)
#     df9.to_excel(writer, sheet_name="FoodItems_claims", index=False)
#     df10.to_excel(writer, sheet_name="Successful_provider's_FoodClaim", index=False)
#     df11.to_excel(writer, sheet_name="Percentage_foodClaims", index=False)
#     df12.to_excel(writer, sheet_name="AvgQuant_claim_BYreceiver", index=False)
#     df13.to_excel(writer, sheet_name="Most_Claimed_mealType", index=False)
#     df14.to_excel(writer, sheet_name="Total_donated_foodQuant", index=False)
#     df15.to_excel(writer, sheet_name="Total_successful_receiv_Cities", index=False)
    

    

conn.commit()

# ANALYSIS BY GRAPHS...

# 9. Which provider has had the highest number of successful food claims?
# top_df10 = df10.head(8)
# plt.figure(figsize=(8,5))
# plt.plot(top_df10["Provider_name"],top_df10["completed_claims"],marker = "*",linestyle="-",color="red")
# plt.xlabel("Provider_name")
# plt.ylabel("Successful_claims")
# plt.title("Top 10 Provider's successful claims numbers")
# plt.grid(True)  # optional, for readability
# plt.tight_layout()
# plt.show()

# 2.Which type of food provider (restaurant, grocery store, etc.) contributes the most food?
# top_df3 = df3.head(4)
# plt.figure(figsize=(8,5))
# plt.bar(top_df3["Type"],top_df3["prov_type_count"],color="green")
# plt.xlabel("Provider_type")
# plt.ylabel("Food_count")
# plt.title("Top Food providers count")
# plt.show()

# 4.Which receivers have claimed the most food?
# plt.figure(figsize=(8,5))
# plt.bar(df5["Type"],df5["recev_type_count"],color="yellow")
# plt.xlabel("Receiver_type")
# plt.ylabel("Cliamed_Food_count")
# plt.title("Top Food Receivers count")
# plt.show()


# # 8.  How many food claims have been made for each food item?
# plt.figure(figsize=(8,5))
# plt.bar(df9["Food_Name"],df9["claim_count"],color="pink")
# plt.xlabel("FOOD NAME")
# plt.ylabel("CLAIMED COUNT")
# plt.title("FOOD ITEMS CLAIMS")
# plt.show()

# 7.What are the most commonly available food types?
# plt.figure(figsize=(8,5))
# plt.plot(df8["Food_Type"], df8["total_count"],marker="*",markerfacecolor="red",markeredgecolor="black",color="skyblue")
# plt.title('Most available food types')
# plt.xlabel("Food Type")
# plt.ylabel("Total quantity")
# plt.grid(True)
# plt.tight_layout()
# plt.show()


queries={ 
     "Providers_count_INcities":df1,
     "Receivers_count_INCities":df2,
     "Mostly_providesFood_ProvType":df3,
     "Mostly_ClaimedFood_Receivers":df5,
     "Total_quanOfFood_byProviders":df6,
     "City_withFood_listings":df7,
     "Most_Available_foodTypes":df8,
     "FoodItems_claims":df9,
     "Successful_provider's_FoodClaim":df10,
     "Percentage_foodClaims":df11,
     "AvgQuant_claim_BYreceiver":df12,
     "Most_Claimed_mealType":df13,
     "Total_donated_foodQuant":df14,
     "Total_successful_receiv_Cities":df15,
     "total food quant in each meal type":df16
    }

graphs={
    "Top 10 Provider's successful claims numbers":"successful_providers_claims.png",
    "Top Food providers count":"Top food providers count.png",
    "Top Food Receivers count":"top receivers count.png",
    "FOOD ITEMS CLAIMS":"food itmes claims.png",
     "Most available food types": "most available food types.png"
}

query_provider= "SELECT Provider_ID, Name, Type,Address,City,Contact FROM provider;"
df_provider = pd.read_sql_query(query_provider,conn)


# # .......STREAMLIT APPLICATION.....

menu = st.sidebar.radio("NAVIGATION",["Project Introduction","SQL queries and Visualization","View Tables","CRUD","Provider Contact Details","User Introduction"])

#.....PROJECT INTRO....

if menu == "Project Introduction":
    st.title("Local Food Wastage Management System**🍽️**")
    st.subheader("**INTRODUCTION📝**")
    st.write("""
      The basic concept of this project is to collect the leftover food from donors such as
      Supermarkets,Grocery Stores,Restaurants,Catering Services etc and distribute to the needy
      peoples through Shelters,NGOs,Charities etc.
     """)
   
    st.subheader("ABOUT FOOD WASTAGE🍎🚫:")
    st.image("foodwastefb.webp",caption="Food Wastage image",use_container_width=True)
    st.write("""
      Food wastage is a significant and very serious global issue.Approximately one-third of all food
      produced is lost or wasted annually.We can contribute to provide the wastage food for needed peoples
      so that, the food will not waste and the needed people can get the food on time.they don't need to suffer
      from hunger.We can see the importance and need of food in peoples of GAZA. they are suffering from hunger
      day by day.So,we developed a Food Management system to minimze the food waste and facilitating the redistribution
      of surplus food.This project will make a significant positive impact on both the environment and the lives of those
      facing food insecurity.
       """)
    st.subheader("WORKING PRINCIPLE⚙️")
    st.write("""
      This project includes Four different tables of Providers,Receivers,Claims and Food Listings.""")
    st.subheader("PROVIDER TABLE")
    st.write("""
      **FEATURES:**
             
         Provider_id, Name, Type, City, Contact, Address""")
    st.subheader("RECEIVER TABLE")
    st.write("""
      **FEATURES:**
             
         Receiver_id, Name, Type, City, Contact""")
    st.subheader("CLAIMS TABLE")
    st.write("""
      **FEATURES:**
             
         Claim_id, Food_id, Receiver_id, Timestamp, Status""")
    st.subheader("FOOD LISTING TABLE")
    st.write("""
      **FEATURES:**
             
       Food_id, Food name, Quantity, Expiry date, Provider_id, Type, Location, Food_type, Meal_type   
             
       **In this project we use SQL, python and streamlit**
       """)
    st.subheader("CORE OBJECTIVES🧩")
    st.write("""
             
      - Filter food donations based on location, provider, and food type.
      - Contact food providers and receivers directly through the app.
      - Implement CRUD operations for updating, adding, and removing records.
      - All the 15 queries along with their outputs.""")
    st.image("objectives fms.jpg",caption="FOOD WASTE MANAGEMENT SYSTEM",use_container_width=True)
    st.subheader("ADVANTAGES")
    st.write("""
      - Provide platform between providers and receivers.
      - Centralize database management.
      - No paper work requirement.""")
    
elif menu == "View Tables":
    st.title("View Database Tables🔎")
    tables = ["provider","receivers","claims","food_listings"]
    selected_table=st.selectbox("Select a table to view:",tables)
    df_table = pd.read_sql_query(f"SELECT * FROM {selected_table}",conn)
    st.dataframe(df_table)

elif menu=="SQL queries and Visualization":
    st.title("📈SQL QUERIES AND VISUALIZATION")
    st.image("visualization.webp",width=150)
    st.subheader("**Queries**")
    query_name=st.selectbox("Select a query to view",list(queries.keys()))
    st.subheader(query_name)
    st.dataframe(queries[query_name])

    st.subheader("**Graphs**")
    select_graph=st.selectbox("Select a graph to view",list(graphs.keys()))
    st.image(graphs[select_graph],use_container_width=True)

   
elif menu=="CRUD":
    st.title("CRUD➕📖✏️🗑️")
    st.subheader("CREATE, READ, UPDATE, DELETE")
    all_tables=["provider","receivers","claims","food_listings"]
    select_table=st.selectbox("Choose a Table",all_tables)
    if select_table == "provider":
        st.subheader("Provider Table🅿️")
        provider_menu=st.selectbox("Choose an option",["Create","Read","Update","Delete"])
        if provider_menu=="Create":
            st.subheader("Add New Record✔️")
            Name=st.text_input("Enter Name")
            Type=st.text_input("Enter Type")
            Address=st.text_input("Enter Address")
            City=st.text_input("Enter City")
            Contact=st.text_input("Enter Contact")
            if st.button("Create"):
                sql1="INSERT INTO provider(Name,Type,Address,City,Contact) VALUES(?,?,?,?,?)"
                val1=(Name,Type,Address,City,Contact)
                cursor.execute(sql1,val1)
                conn.commit()
                st.success("Record created successfully🙂!!!")

        elif provider_menu=="Read":
            st.subheader("Read Records📖")
            sql2 ="SELECT * FROM provider"
            cursor.execute(sql2)
            result_1 = cursor.fetchall()
            for raw in result_1:
                st.write(raw)

        elif provider_menu=="Update":
            st.subheader("Update Records🔄")
            Provider_ID = st.number_input("Enter ID")
            Name=st.text_input("Enter New Name")
            Type=st.text_input("Enter New Type")
            Address=st.text_input("Enter New Address")
            City=st.text_input("Enter New City")
            Contact=st.text_input("Enter New Contact")
            if st.button("Update"):
                sql3 = "UPDATE provider SET Name=?, Type=?, Address=?, City=?,Contact=? WHERE Provider_ID =?"
                val3 = (Name,Type,Address,City,Contact,Provider_ID)
                cursor.execute(sql3,val3)
                conn.commit()
                st.success("Record Updated Successfully👍!!!")

        elif provider_menu=="Delete":
            st.subheader("Delete Records🚮")
            Provider_ID=st.number_input("Enter ID")
            if st.button("Delete"):
                sql4 ="DELETE FROM provider WHERE Provider_ID =?"
                val4 =(Provider_ID,)
                cursor.execute(sql4,val4)
                conn.commit()
                st.success("Record Deleted Successfully!!!!☺️")
    elif select_table == "receivers":
        st.subheader("Receiver Table®️")
        receiver_menu = st.selectbox("Choose an option",["Create","Read","Update","Delete"])
        if receiver_menu=="Create":
            st.subheader("Create a new Record✔️")
            Name =st.text_input("Enter Name")
            Type =st.text_input("Enter Type")
            City=st.text_input("Enter City")
            Contact=st.text_input("Enter Contact")
            if st.button("Create"):
                r_sql1 ="INSERT INTO receivers(Name,Type,City,Contact) VALUES(?,?,?,?)"
                r_val1 = (Name,Type,City,Contact)
                cursor.execute(r_sql1,r_val1)
                conn.commit()
                st.success("Record Created Successfully!!!✅")

        elif receiver_menu=="Read":
            st.subheader("Read Records📖")
            r_sql2 ="SELECT * FROM receivers"
            cursor.execute(r_sql2)
            result_r1 = cursor.fetchall()
            for raw in result_r1:
                st.write(raw)

        elif receiver_menu=="Update":
            st.subheader("Update Record🔄")
            Receiver_ID = st.number_input("Enter ID")
            Name=st.text_input("Enter New Name")
            Type=st.text_input("Enter New Type")
            City=st.text_input("Enter New City")
            Contact=st.text_input("Enter New Contact")
            if st.button("Update"):
                r_sql3 = "UPDATE receivers SET Name=?, Type=?, City=?,Contact=? WHERE Receiver_ID =?"
                r_val3 = (Name,Type,City,Contact,Receiver_ID)
                cursor.execute(r_sql3,r_val3)
                conn.commit()
                st.success("Record Updated Successfully👍!!!")

        elif receiver_menu =="Delete":
            st.subheader("Delete Record🚮")
            Receiver_ID = st.number_input("Enetr ID")
            if st.button("Delete"):
                r_sql4 = "DELETE FROM receivers WHERE Receiver_ID=?"
                r_val4 = (Receiver_ID,)
                cursor.execute(r_sql4,r_val4)
                conn.commit()
                st.success("Record Deleted Successfully!!!!☺️")

    elif select_table == "claims":
        st.subheader("Claims Table🅲")
        claims_menu=st.selectbox("Choose an option",["Create","Read","Update","Delete"])
        if claims_menu=="Create":
            st.subheader("Create New Record✔️")
            Food_ID =st.text_input("Enter Food_ID")
            Receiver_ID = st.text_input("Enetr Receiver_ID")
            Status = st.text_input("Enter Status")
            Timestamp = st.text_input("Enter Timestamp")
            if st.button("Create"):
                c_sql1 = "INSERT INTO claims(Food_ID,Receiver_ID,Status,Timestamp) VALUES(?,?,?,?)"
                c_val1 = (Food_ID,Receiver_ID,Status,Timestamp)
                cursor.execute(c_sql1,c_val1)
                conn.commit()
                st.success("Record Created Successfully!!!👍")
        elif claims_menu=="Read":
                st.subheader("Read Records📝")
                c_sql2 = "SELECT * FROM claims"
                cursor.execute(c_sql2)
                c_result=cursor.fetchall()
                for row in c_result:
                    st.write(row)
               
        elif claims_menu =="Update":
                st.subheader("Update Record🔄")
                Claim_ID=st.number_input("Enter Claim_ID")
                Food_ID =st.text_input("Enter Food_ID")
                Receiver_ID = st.text_input("Enetr Receiver_ID")
                Status = st.text_input("Enter Status")
                Timestamp = st.text_input("Enter Timestamp")
                if st.button("Update"):
                    c_sql3 = "UPDATE claims SET Food_ID=?,Receiver_ID=?,Status=?,Timestamp=? WHERE Claim_ID =?"
                    c_val3 = (Food_ID,Receiver_ID,Status,Timestamp,Claim_ID)
                    cursor.execute(c_sql3,c_val3)
                    conn.commit()
                    st.success("Record Updated Successfully!!!👍")

        elif claims_menu=="Delete":
                st.subheader("Delete Record🚮")
                Claim_ID = st.number_input("Enter Claim_ID")
                if st.button("Delete"):
                    c_sql4 = "DELETE FROM claims WHERE Claim_ID =?"
                    c_val4 = (Claim_ID,)
                    cursor.execute(c_sql4,c_val4)
                    conn.commit()
                    st.success("Record Deleted Successfully!!!☺️")

    elif select_table == "food_listings":
        st.subheader("Food Listing Table📋")
        fl_menu=st.selectbox("Choose an option",["Create","Read","Update","Delete"])
        if fl_menu=="Create":
            st.subheader("Create a record✔️")
            Food_Name= st.text_input("Enter Food_Name")
            Quantity =st.text_input("Enter Quantity")
            Expiry_Date = st.text_input("Enter Expiry_Date")
            Provider_ID = st.text_input("Enter Provider_ID")
            Provider_Type = st.text_input("Enter Provider_Type")
            Location=st.text_input("Enter Location")
            Food_Type=st.text_input("Enter Food_Type")
            Meal_Type=st.text_input("Enter Meal_Type")
            if st.button("Create"):
                fl_sql1 = "INSERT INTO food_listings(Food_Name,Quantity,Expiry_Date,Provider_ID,Provider_Type,Location,Food_Type,Meal_Type) VALUES(?,?,?,?,?,?,?,?)"
                fl_val1 = (Food_Name,Quantity,Expiry_Date,Provider_ID,Provider_Type,Location,Food_Type,Meal_Type)
                cursor.execute(fl_sql1,fl_val1)
                conn.commit()
                st.success("Record Created Successfully!!!👍")

        elif fl_menu== "Read":
            st.subheader("Read Records📋")
            fl_sql2 = "SELECT * FROM food_listings"
            cursor.execute(fl_sql2)
            fl_result=cursor.fetchall()
            for row in fl_result:   
                st.write(row)

        elif fl_menu== "Update":
            st.subheader("Update Record🔄")
            Food_ID = st.number_input("Enter Food_ID")
            Food_Name= st.text_input("Enter Food_Name")
            Quantity =st.text_input("Enter Quantity")
            Expiry_Date = st.text_input("Enter Expiry_Date")
            Provider_ID = st.text_input("Enter Provider_ID")
            Provider_Type = st.text_input("Enter Provider_Type")
            Location=st.text_input("Enter Location")
            Food_Type=st.text_input("Enter Food_Type")
            Meal_Type=st.text_input("Enter Meal_Type")
            if st.button("Update"):
                fl_sql3 = "UPDATE food_listings SET Food_Name=?,Quantity=?,Expiry_Date=?,Provider_ID=?, Provider_Type=?,Location=?,Food_Type=?,Meal_Type=? WHERE Food_ID =?"
                fl_val3 =(Food_Name,Quantity,Expiry_Date,Provider_ID,Provider_Type,Location,Food_Type,Meal_Type,Food_ID)
                cursor.execute(fl_sql3,fl_val3)
                conn.commit()
                st.success("Record Updated Successfully!!!👍")

        elif fl_menu=="Delete":
            st.subheader("Delete Record🚮")
            Food_ID = st.number_input("Enter Food_ID")
            if st.button("Delete"):
                fl_sql4 = "DELETE FROM food_listings WHERE Food_ID =?"
                fl_val4 = (Food_ID,)
                cursor.execute(fl_sql4,fl_val4)
                conn.commit()
                st.success("Record Deleted Successfully!!!👍")

elif menu =="Provider Contact Details":
    st.title("Direct Contact to Provider📞")
    st.image("direct contact.jpg",width=150)
    st.dataframe(df_provider)
    search = st.text_input("Search Provider by Name/City🔍")
    if search:
        filtered = df_provider[
            df_provider["Name"].str.contains(search, case=False) |
            df_provider["City"].str.contains(search, case=False)
        ] 
        st.dataframe(filtered)
    selected_provider=st.selectbox("Select a provider to contact",df_provider["Name"])
    provider_details = df_provider[df_provider["Name"] == selected_provider].iloc[0]

    st.write(f"📍Location: {provider_details["City"]}")
    st.write(f"📱Contact: {provider_details['Contact']}")

elif menu=="User Introduction":
    st.title("About the creator:")  
    st.image("Shireen-designstyle-pastel-m.png",use_container_width=True) 
    st.write("""
   **👩‍💻Name:** Shireen Khan
             
   **🔞Age:** 22
             
   **🎓Status:** Student of Mca 3rd sem. + Intern
             
   **🏫University:** Amity University,Noida
             
   **👩‍💻Internship:** Labmantix company
             
   **📚Field:** AI and ML
             
   **📍Location:** Rajasthan,India""")
    
# END OF PROJECT.....







