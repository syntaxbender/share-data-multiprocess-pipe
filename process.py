#python3
from multiprocessing import Process,Pipe
import time

def process(conn):
    while True:
        test = conn.recv()
        if(test[0] == "status" and test[1] == "done"):
            break
        if(test[0] == "data"):
            conn.send(test[1])

def initialize():
    processes = []
    works_to_distrubute = range(1000)
    parent_connections = {}
    
    for i in range(4):
        parent_conn, child_conn = Pipe()    
        p = Process(target=process, name="test"+str(i), args=(child_conn,))
        p.start()
        processes.append(p)
        parent_connections["test"+str(i)] = parent_conn
    distribute_works(works_to_distrubute,parent_connections)

    for p in processes:
        p.join()
def distribute_works(works_to_distrubute,parent_connections):
    received_data = []
    for cursor in range(len(works_to_distrubute)):
        conn_num = cursor%4
        conn = parent_connections["test"+str(conn_num)]
        conn.send(["data",works_to_distrubute[cursor]])
        data = conn.recv()
        received_data.append(data)
        if(cursor == len(works_to_distrubute)-1):
            for cursor in range(4):
                conn = parent_connections["test"+str(cursor)]
                conn.send(["status","done"])
    print(received_data)
    print(len(received_data))
start = time.time()

initialize()
end = time.time()
print("The time of execution of above program is :",
      (end-start) * 10**3, "ms")
