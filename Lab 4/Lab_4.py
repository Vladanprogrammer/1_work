class MyName:
    """Опис класу / Документація
    """
    total_names = 0  # Class Variable

    def __init__(self, name=None) -> None:
        """Ініціалізація класу
        """
        if name is not None:
            if not name.isalpha():
                raise ValueError("Ім'я може містити лише літери!")
            self.name = name.capitalize()
        else:
            self.name = self.anonymous_user().name

        MyName.total_names += 1  # modify class variable
        self.my_id = self.total_names
        

    @property
    def full_name(self) -> str:
        """Class property
        Повертає рядок формату: User #<id>: <name> (<email>)
        """
        return f"User #{self.my_id}: {self.name} ({self.my_email})"

    @property
    def whoami(self) -> str: 
        """Class property
        return: повертаємо імя 
        """
        return f"My name is {self.name}"
    
    @property
    def my_email(self) -> str:
        """Class property
        return: повертаємо емейл
        """
        return self.create_email()
    
    def create_email(self, domain: str = "itcollege.lviv.ua") -> str:
        """Instance method
        Формує email з можливістю змінити домен після '@'

        :param domain: доменна частина email (рядок після '@')
        """
        return f"{self.name}@{domain}"

    def save_to_file(self, filename: str = "users.txt") -> None:
        """Instance method
        Зберігає інформацію про користувача у файл.

        :param filename: назва файлу, у який додається запис
        """
        with open(filename, "a", encoding="utf-8") as f:
            f.write(self.full_name + "\n")
    
    @classmethod
    def anonymous_user(cls):
        """Classs method
        """
        return cls("Anonymous")
    
    @staticmethod
    def say_hello(message="Hello to everyone!") -> str:
        """Static method
        """
        return f"You say: {message}"


print("Розпочинаємо створювати обєкти!")

names = ("Bohdan", "Marta", None)
all_names = {name: MyName(name) for name in names}

for name, me in all_names.items():
    print(f"""{">*<"*20}
This is object: {me} 
This is object attribute: {me.name} / {me.my_id}
This is {type(MyName.whoami)}: {me.whoami} / {me.my_email}
This is {type(me.create_email)} call: {me.create_email()}
This is static {type(MyName.say_hello)} with defaults: {me.say_hello()} 
This is class variable {type(MyName.total_names)}: from class {MyName.total_names} / from object {me.total_names}
{"<*>"*20}""")

print(f"We are done. We create {me.total_names} names! ??? Why {MyName.total_names}?")