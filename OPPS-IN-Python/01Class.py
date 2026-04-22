class student:
    def set_name(self,name):
        self.name=name

        
    def get_name(self):
        return  self.name
student1=student()  
student1.set_name("Rohit")
print(student1.get_name())   

student2=student()
student2.set_name("Rohan")
print(student2.get_name())