import csv  

count = [0]

cache = []

def add_cache(action:list):
    cloneList = action[:]
    cache.append(cloneList)
    count[0] += 1
    if count[0] == 10:
        write_to_csv(cache)

def add_cache_no_queue(action):
    cache.append(action)
    write_to_csv(cache)
    
def write_to_csv(cache:list):
    with open('payment_history.csv', 'a', encoding='UTF8',newline='') as f:
        writer = csv.writer(f)

        for i in range (len(cache)):
            
            # write the data
            writer.writerow(cache[i])
    count[0] = 0
    cache.clear()