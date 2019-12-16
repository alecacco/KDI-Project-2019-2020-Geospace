import json
import utm
import sys,os


def do_get_coordinate(input_json,output_csv):
    path = os.path.join(os.path.expanduser('~'), input_json)
    tj = json.load(open(path))
    #tj = json.load(open(input_json))#path))
    f = open(output_csv+".csv","w+")
    f.write("name,startlat,startlon,endlat,endlon,points\n")
    for sentiero in tj["objects"]["sentieri_tratte"]["geometries"]:
        coords = []
        for arc_i in range(len(sentiero["arcs"])):
            arc = tj["arcs"][arc_i]
            positions = []
            acc=[0,0]
            for i in range(len(arc)):
                position = (
                    (acc[0] + arc[i][0]) * tj["transform"]["scale"][0] + tj["transform"]["translate"][0],
                    (acc[1] + arc[i][1]) * tj["transform"]["scale"][1] + tj["transform"]["translate"][1]
                )
                acc[0]+=arc[i][0]
                acc[1]+=arc[i][1]
                positions.append(position)
            coords += [utm.to_latlon(pos[0],pos[1],32,"U") for pos in positions]
            """
            if len(coords)==0:
                coords.append(utm.to_latlon(positions[0][0],positions[0][1],32,"U"))
            coords.append(utm.to_latlon(positions[-1][0],positions[-1][1],32,"U"))
            """

        f.write(
            str("\""+sentiero["properties"]["numero"])+"_0"+"\""+","
            +"\""+str(coords[0][0])+"\""+","
            +"\""+str(coords[0][1])+"\""+","
            +"\""+str(coords[-1][0])+"\""+","
            +"\""+str(coords[-1][1])+"\""+","
            +"\"LINESTRING("+",".join([str(c[0])+" "+str(c[1]) for c in coords])+"\""+")\n"
        )
        f.write(
            str("\""+sentiero["properties"]["numero"])+"_1"+"\""+","
            +"\""+str(coords[-1][0])+"\""+","
            +"\""+str(coords[-1][1])+"\""+","
            +"\""+str(coords[0][0])+"\""+","
            +"\""+str(coords[0][1])+"\""+","
            +"\"LINESTRING("+",".join([str(c[0])+" "+str(c[1]) for c in list(reversed(coords))])+"\""+")\n"
        )

    return f


def rm_main():
    return do_get_coordinate("topojson.json","sentieri_coordinates")
