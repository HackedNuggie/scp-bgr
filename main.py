from scp import SCP
from time import sleep
import json
from flask import Flask, redirect, render_template, request, url_for
from random import randrange

# \u2588 is the ████ characters
def create_scps(num) -> None:
    for x in range(895,2000):
        try:
            scp = SCP.create_scp(x)
            with open("persistent/scp.json","a") as f:
                json.dump(scp.json(),f)
                f.write(",\n")
            print(x)
            if scp.site is None:
                with open ("persistent/failed.txt","a") as f:
                    f.write(f"{x} no description\n")
        except Exception as e:
            with open("persistent/failed.txt","a") as f:
                f.write(f"{x}: {e}\n")
            print(f"{x} failed")
        #sleep(0.1)
    print("done")

def test_scp(num):
    scp = SCP.create_scp(num)
    print(scp)

if __name__ == '__main__':
    app = Flask(__name__)
    @app.route("/scps")
    def scps():
        with open("persistent/scp.json","r") as f:
            scps = json.load(f)
            print(scps)
    
    
    @app.route("/scps/") # <int:num>")
    def scp(num = 682):
        # num -= 100
        
        print(num)
        with open("persistent/scp.json","r") as f:
            scps = json.load(f)
        x = True
        while x == True:
            num = randrange(0,len(scps))-100
            #print(scps[num]["image"])
            if scps[num]["image"]:
                x = False
        return render_template("index.html",scp=scps[num])
    app.run(host='0.0.0.0', port=8080, debug=True)