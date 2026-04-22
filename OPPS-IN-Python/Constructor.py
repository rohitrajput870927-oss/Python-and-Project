class rectangle:
    def _init_(self,height,width):
        print(f"The height of rectangle{height} And the width of rectangle{width}")
        self.height=height
        self.width=width

    def _demention_(self,height,width):
        self.height=height
        self.width=width
            
    def area(self):
        return self.height*self.width
    def perimeter(self):
        return 2*(self.height+self.width)    
    
r1=rectangle(4,5)
   
    