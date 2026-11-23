import functools


def validate_book_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        title = kwargs.get('title')
        year = kwargs.get('year')
        
        if len(args) >= 2:
            title = args[1]
        if len(args) >= 3:
            year = args[2]
            
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Назва книги не може бути порожньою")
            
        if not isinstance(year, int) or year < 1000:
            raise ValueError("Рік видання має бути цілим числом >= 1000")
            
        return func(*args, **kwargs)
    return wrapper
