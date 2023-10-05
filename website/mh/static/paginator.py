# # # # # # # # # # # # # # # # 
# Jack Ricketts
# 15/03/2023
# Paginator code
# # # # # # # # # # # # # # # # 

class Paginator():
    def __init__(self, list, count, start = 1):
        '''Custom pagination function'''
        self.list = list
        self.count = count
        self.current = start


    def Get(self):
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
        

    def GetPage(self, page):
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
        
        
    def HasNext(self, page):
        try:
            x = self.list[page * self.count]
            return True
        except:
            return False
    
    def HasPrev(self, page):
        if page < 2:
            return False
        return True
    
    def GetNext(self):
        self.current += 1
        return self.Get()
    
    def GetPrev(self):
        self.current -= 1
        return self.Get()
    
    def Jump(self, page):
        self.current = page
        return self.Get()