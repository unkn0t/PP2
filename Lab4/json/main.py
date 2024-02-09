import json

def main():
    print("=======================================================================================")
    print("DN                                                 Description           Speed    MTU") 
    print("-------------------------------------------------- --------------------  ------  ------")
    
    with open("json/sample-data.json", "r") as sample_data:
        data = json.loads(sample_data.read())
        imdata = data["imdata"]

        for im in imdata:
            attrs = im["l1PhysIf"]["attributes"]
            dn = attrs["dn"]
            descr = attrs["descr"]
            speed = attrs["speed"]
            mtu = attrs["mtu"]
            print(f"{dn:50} {descr:20} {speed:9} {mtu:6}")

main()
