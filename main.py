class InvalidPointError(Exception):
    pass


class InvalidShapeError(Exception):
    pass


class Point:
    def __init__(self, x, y):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise InvalidPointError("Координаты точки должны быть числами")
        self.x = x  # Координата x
        self.y = y  # Координата y


class Square:
    def __init__(self, identifier, center, side_length):
        if not isinstance(center, Point):
            raise InvalidShapeError("Центр квадрата должен быть объектом класса Point")
        if not isinstance(side_length, (int, float)) or side_length <= 0:
            raise InvalidShapeError("Длина стороны квадрата должна быть положительным числом")
        self.identifier = identifier  # Идентификатор квадрата
        self.center = center  # Центр квадрата (точка)
        self.side_length = side_length  # Длина стороны квадрата

    def move(self, dx, dy):
        if not isinstance(dx, (int, float)) or not isinstance(dy, (int, float)):
            raise InvalidShapeError("Смещение должно быть числом")
        # Перемещение центра квадрата
        self.center.x += dx
        self.center.y += dy

    def is_intersect(self, other):
        if not isinstance(other, Pentagon):
            raise ValueError("Проверка пересечения поддерживается только между объектами Square и Pentagon")

        # Проверяем пересечение каждой стороны квадрата с каждой стороной пятиугольника
        for i in range(4):
            p1 = self.get_vertex(i)
            p2 = self.get_vertex((i + 1) % 4)

            for j in range(5):
                q1 = other.vertices[j]
                q2 = other.vertices[(j + 1) % 5]

                if self.do_intersect(p1, p2, q1, q2):  # Проверяем пересечение отрезков
                    return True

        return False

    def get_vertex(self, i):
        # Вычисляем координаты вершины квадрата
        if i == 0:
            return Point(self.center.x - self.side_length / 2, self.center.y - self.side_length / 2)
        elif i == 1:
            return Point(self.center.x + self.side_length / 2, self.center.y - self.side_length / 2)
        elif i == 2:
            return Point(self.center.x + self.side_length / 2, self.center.y + self.side_length / 2)
        elif i == 3:
            return Point(self.center.x - self.side_length / 2, self.center.y + self.side_length / 2)

    @staticmethod
    def do_intersect(p1, q1, p2, q2):
        def orientation(p, q, r):
            val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
            if val == 0:
                return 0
            return 1 if val > 0 else 2

        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and Square.on_segment(p1, p2, q1):
            return True

        if o2 == 0 and Square.on_segment(p1, q2, q1):
            return True

        if o3 == 0 and Square.on_segment(p2, p1, q2):
            return True

        if o4 == 0 and Square.on_segment(p2, q1, q2):
            return True

        return False

    @staticmethod
    def on_segment(p, q, r):
        return min(p.x, q.x) <= r.x <= max(p.x, q.x) and min(p.y, q.y) <= r.y <= max(p.y, q.y)

    def __str__(self):
        vertices_str = ""
        for i in range(4):
            vertex = self.get_vertex(i)
            vertices_str += f"({vertex.x}, {vertex.y})"
            if i < 3:
                vertices_str += ", "
        return f"Square: {vertices_str}"


class Pentagon:
    def __init__(self, identifier, vertices):
        for vertex in vertices:
            if not isinstance(vertex, Point):
                raise InvalidShapeError("Вершины пятиугольника должны быть объектами класса Point")
        if len(vertices) != 5:
            raise InvalidShapeError("Пятиугольник должен иметь 5 вершин")

        self.identifier = identifier  # Идентификатор пятиугольника
        self.vertices = vertices  # Список вершин пятиугольника

    def move(self, dx, dy):
        if not isinstance(dx, (int, float)) or not isinstance(dy, (int, float)):
            raise InvalidShapeError("Смещение должно быть числом")
        # Перемещение каждой вершины пятиугольника
        for vertex in self.vertices:
            vertex.x += dx
            vertex.y += dy

    def is_intersect(self, other):
        if not isinstance(other, Square):
            raise ValueError("Проверка пересечения поддерживается только между объектами Pentagon и Square")

        # Проверяем пересечение каждой стороны пятиугольника с каждой стороной квадрата
        for i in range(5):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % 5]

            for j in range(4):
                q1 = other.get_vertex(j)
                q2 = other.get_vertex((j + 1) % 4)

                if Square.do_intersect(q1, q2, p1, p2):  # Проверяем пересечение отрезков
                    return True

        return False

    def __str__(self):
        vertices_str = ""
        for i in range(5):
            vertex = self.vertices[i]
            vertices_str += f"({vertex.x}, {vertex.y})"
            if i < 4:
                vertices_str += ", "
        return f"Pentagon: {vertices_str}"


try:
    square_center = Point(2, 2)
    square = Square("square1", square_center, 4)

    pentagon_vertices = [Point(0, 0), Point(3, 0), Point(5, 2), Point(2, 4), Point(1, 2)]
    pentagon = Pentagon("pentagon1", pentagon_vertices)

    print("Квадрат до перемещения:")
    print(square)
    print("Пятиугольник до перемещения:")
    print(pentagon)

    # Перемещение объектов
    square.move(1, 1)
    pentagon.move(2, 2)

    print("\nКвадрат после перемещения:")
    print(square)
    print("Пятиугольник после перемещения:")
    print(pentagon)

    if square.is_intersect(pentagon):
        print("\nКвадрат пересекается с пятиугольником.")
    else:
        print("\nКвадрат не пересекается с пятиугольником.")

except (InvalidPointError, InvalidShapeError, ValueError) as e:
    print(f"Произошла ошибка: {e}")
