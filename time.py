from datetime import datetime

def operation():
    counter = 0
    tbeg = datetime.utcnow()
    for _ in range(10**8):
        counter += 1
    td = datetime.utcnow() - tbeg
    print float(td.microseconds) / 1000000.0
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6)/10.0**6

def timer(n):
    stack = []
    for _ in range(n):        
        stack.append(operation()) #  units of musec/increment
    print sum(stack) / len(stack)

if __name__ == "__main__":
    timer(10)