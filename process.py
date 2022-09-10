from multiprocessing import Process,Pipe
import time
class ProcessManager:
    parent_connections = {}
    works_to_distrubute = []
    processes = []
    process_namespace = "proc-geny"
    process_count = 4
    received_data = {}
    def __init__(self):
        parent_connections = {}
        works_to_distrubute = []
        processes = []
        process_namespace = "proc-geny"
        process_count = 4
        received_data = {}
    def child_process(self,conn,proc_name):
        while True:
            message = conn.recv()
            if message[0] == "status" and message[1] == "done":
                break
            elif message[0] == "func" and message[1]:
                if message[2]:
                    callback = message[1](message[2])
                else:
                    callback = message[1]()
                conn.send([proc_name,callback])
            else:
                raise Exception("Process parse error")
    def process(self,works_to_distrubute): #works_to_distrubute = [["func obj","arguments"], ... ]
        for i in range(self.process_count):
            parent_conn, child_conn = Pipe()    
            p = Process(target=self.child_process, name=self.process_namespace+str(i), args=(child_conn,self.process_namespace+str(i)))
            p.start()
            self.processes.append(p)
            self.parent_connections[self.process_namespace+str(i)] = parent_conn
        self.distribute_works(works_to_distrubute)
        for p in self.processes:
            p.join()
        return self.received_data
    def distribute_works(self,works_to_distrubute):
        for cursor in range(len(works_to_distrubute)):
            conn_num = cursor%self.process_count
            conn = self.parent_connections[self.process_namespace+str(conn_num)]
            conn.send(["func",*works_to_distrubute[cursor]])
            data = conn.recv()
            self.received_data[data[0]] = data[1]
            if(cursor == len(works_to_distrubute)-1):
                for cursor in range(self.process_count):
                    conn = self.parent_connections[self.process_namespace+str(cursor)]
                    conn.send(["status","done"])

def alo(za):
    return za
start = time.time()
process_manager = ProcessManager()
oleybe = process_manager.process([[alo,"asd"],[alo,"qwe"]])

print(oleybe)

end = time.time()
print("The time of execution of above program is :",
    (end-start) * 10**3, "ms")
