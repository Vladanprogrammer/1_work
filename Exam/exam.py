class ListIntersection:
    def __init__(self, list1, list2):
        self.list1 = list1
        self.list2 = list2
        self.student_name = "Ім'я Прізвище"
        self.group = "ГРУПА"
        self._common_elements = None

    def find_intersection(self):
        self._common_elements = list(set(self.list1) & set(self.list2))

    @property
    def common_elements(self):
        if self._common_elements is None:
            self.find_intersection()
        return self._common_elements    

    def process_data(self):
        """Обробляє вхідні дані: нормалізує рядки і знаходить перетин."""
        def _normalize(x):
            if isinstance(x, str):
                return x.strip().lower()
            return x

        self.list1 = [_normalize(x) for x in self.list1]
        self.list2 = [_normalize(x) for x in self.list2]
        self.find_intersection()
        try:
            self._common_elements.sort()
        except Exception:
            pass

    @property
    def result(self):
        return f"Common elements: {self.common_elements}"

    def __str__(self):
        return f"Студент: {self.student_name}, Група: {self.group}"


if __name__ == "__main__":
    samples = [
        (['apple', 'banana', 'Cherry', '  apple '], ['banana', 'cherry', 'date', 'Apple'], "Іван Іванов", "CS-01"),
        ([1, 2, 3, 4], [3, 4, 5, 6], "Марія Петрівна", "CS-02"),
        (['A', 'B', 'C'], ['b', 'c', 'd'], "Олег Студент", "CS-03"),
    ]

    for a, b, name, group in samples:
        li = ListIntersection(a, b)
        li.student_name = name
        li.group = group
        li.process_data()
        print(li)
        print(li.result)
        print("Raw common elements:", li.common_elements)
        print("-" * 40)
    