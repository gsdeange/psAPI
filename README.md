# psAPI
RESTful API that returns the results of Linux ps command

**Dependencies:**
  - FastAPI
  - Uvicorn[standard]
  - textfsm
  - pandas

**Setup instructions:**
  1. Make sure all dependencies/python packages are installed correctly using pip install <package>
      - pip install fastapi
      - pip install uvicorn
      - pip install textfsm
      - pip install pandas

  2. Now run the uvicorn server and the API using the command
  
            uvicorn host:app -- reload
            
     You should see text saying "Uvicorn running on http://127.0.0.1:800"
     and "Application startup complete"
     
  3. Now psAPI is up and running!



**Use Instructions:**

  Browser use:
  
    Go to browser and type "http://127.0.0.1:8000/"
    
    You will now see all of the returned processes in JSON format
    
   Swagger UI:
   
      Go to browser and type "http://127.0.0.1:8000/docs"
      
      You will now see a Swagger UI with 3 different options for use
        - Default
        - Filtering
        - Sorting

Note: To use each of the features, click the 'GET' box and then 'try it out' on the right hand side of the expanded box
      
**Filtering:**

We can function the process data using a query string inputted by the user. Sorting is also available aftering filtering the data

Required:
  
   q: query string to filter the data
      
        Format example: PID == 6 & User == "root"
        
        Basic boolean operations are supported, you must use double quotes for name queries ie. User == "<name>"
        
        Supported Fields:
          - User
          - Group
          - PID
          - CPU
          - MEM
          - RSS
          - STAT
          - Weekday
          - Month
          - Day
          - Time
          - Year
          - Elapsed
          - Command
         
       
    
          
  
  
    
