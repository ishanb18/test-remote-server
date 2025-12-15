import sqlite3
from fastmcp import FastMCP
import os

DB_path = os.path.join(os.path.dirname(__file__),"expenses.db")
Categories_path = os.path.join(os.path.dirname(__file__),"categories.json")

mcp = FastMCP("ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_path) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS expenses(id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT NOT NULL,
                  amount REAL NOT NULL,
                  category TEXT NOT NULL,
                  subcategory TEXT DEFAULT '',
                  note TEXT Default '')
                  """)
                  
init_db()

@mcp.tool
def add_expenses(date,amount,category,subcategory = "",note = ""):
    with sqlite3.connect(DB_path) as c:
        curr = c.execute(" INSERT INTO expenses(date,amount,category,subcategory,note) VALUES (?,?,?,?,?)",
                  (date,amount,category,subcategory,note)
                  )
        return {"status":"ok","id":curr.lastrowid}
    

@mcp.tool
def list_expenses(start_date,end_date):
    with sqlite3.connect(DB_path) as c:
        curr = c.execute("SELECT id,date,category,subcategory,note FROM expenses WHERE date BETWEEN ? and ? order by id ASC",(start_date,end_date))

        cols = [d[0] for d in curr.description]
        return [dict(zip(cols,r)) for r in curr.fetchall()]
    

@mcp.tool
def summarize(start_date,end_date,category = None):
    with sqlite3.connect(DB_path) as c:
        query = {"""
                 SELECT category,SUM(amount) AS Total_Amount
                 FROM date BETWEEN ? AND ?
                 """}
        params = [start_date,end_date]
        
        if category:
            query+="and category = ?"
            params.append(category)

        query+= "GROUP BY category ORDER BY category ASC"

        curr = c.execute(query,params)

        cols =[d[0] for d in curr.description]
        return [dict(zip(cols,r)) for r in curr.fetchall]
    
@mcp.resource("expense://categories",mime_type="application/json")
def categories():
    with open(Categories_path,"r",encoding="utf-8") as f:
        return f.read()
        
if __name__ == "__main__":
    mcp.run(transport = "http",host = "0.0.0.0",port = 8000)

