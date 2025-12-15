"""from fastmcp import FastMCP
import random
import json

mcp = FastMCP("remote server")
@mcp.tool
def add_numbers(a:int,b:int)->int:
    "add two numbers a and b"

    return a+b

@mcp.tool
def random_number(min_val:int =1,max_val:int=100)->int:
    "generate random number in the given range between min_val and max_val"
    
    return random.randint(min_val,max_val)

@mcp.resource("info://server")
def server_info()->str:
    "get information about this server"
    info = {
        "name":"simple Calculator server",
        "version":"1.0.0",
        "tools":["add","random_number"],
        "author":"ishan bansal"
    }
    return json.dumps(info,indent=2)



if __name__ == "__main__":
    mcp.run(transport = "http",host="0.0.0.0",port = 8000)"""