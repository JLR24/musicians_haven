# # # # # # # # # # # # # # # # 
# Jack Ricketts
# 15/03/2023
# Custom Paginator code
# # # # # # # # # # # # # # # # 

class Paginator():
    def __init__(self, list, count, start = 1):
        '''Custom pagination function'''
        self.list = list
        self.count = count
        self.current = start


    def get(self):
        last = self.current  * self.count - 1
        first = last - self.count + 1
        if self.current < 0:
            return []
        if len(self.list) > first:
            items = []
            if len(self.list) > last: # Sufficient items
                for i in range(first, last + 1):
                    items.append(self.list[i])
            else:
                for i in range(first, len(self.list)):
                    items.append(self.list[i])
            return items
        else:
            return []
        

    def getPage(self, page):
        last = page  * self.count - 1
        first = last - self.count + 1
        if page <= 0:
            return []
        if len(self.list) > first:
            items = []
            if len(self.list) > last: # Sufficient items
                for i in range(first, last + 1):
                    items.append(self.list[i])
            else:
                for i in range(first, len(self.list)):
                    items.append(self.list[i])
            self.current = page
            return items
        else:
            return []
        
        
    def hasNext(self, page):
        try:
            x = self.list[page * self.count]
            return True
        except:
            return False
    
    def hasPrev(self, page):
        if page < 2:
            return False
        return True
    
    def getNext(self):
        self.current += 1
        return self.Get()
    
    def getPrev(self):
        self.current -= 1
        return self.Get()
    
    def jump(self, page):
        self.current = page
        return self.Get()