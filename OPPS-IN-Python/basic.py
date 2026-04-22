class rectangle:
     def _init_ (self,height,width):
        print(f"The height of rectangle{self.height} And the width of rectangle{self.width}")
        self.height=height
        self.width=width



     def area(self):
       return self.height*self.width
    
     def  perimeter(self):
        return 2*(self.height+self.width)
             

r1=rectangle()#call  the class
